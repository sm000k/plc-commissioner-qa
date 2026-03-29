<#
.SYNOPSIS
    Generuje dokument .docx (PLC Commissioner Q&A) z pliku Markdown.

.DESCRIPTION
    Parsuje plik Markdown z Q&A i tworzy sformatowany dokument Word.
    Format wejścia:
      # TYTUŁ
      ### podtytuł
      ---
      ## 1. NAZWA SEKCJI
      ### 1. Pytanie?
      Treść odpowiedzi.
      - Punkt 1
      - Punkt 2
      > Źródło: ...

.PARAMETER InputFile
    Ścieżka do pliku Markdown (.md) z treścią Q&A.

.PARAMETER OutputFile
    Ścieżka docelowa dla wygenerowanego pliku .docx.
    Domyślnie: PLC_Commissioner_QA_v{Version}.docx w bieżącym katalogu.

.PARAMETER Version
    Numer wersji dokumentu (wstawiony do nagłówka tytułowego).

.EXAMPLE
    .\New-QADocument.ps1 -InputFile docs\qa_draft_v7.md -Version 7

.EXAMPLE
    .\New-QADocument.ps1 -InputFile docs\qa_draft_v7.md -OutputFile "C:\output\QA_v7.docx" -Version 7
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path $_ -PathType Leaf })]
    [string]$InputFile,

    [string]$OutputFile = "",

    [int]$Version = 7
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Ścieżki ──────────────────────────────────────────────────────────────────
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$InputFullPath = Resolve-Path $InputFile

if ($OutputFile -eq "") {
    $OutputFile = Join-Path $WorkspaceRoot "PLC_Commissioner_QA_v${Version}.docx"
}
$OutputFullPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputFile)

Write-Host "Wejście : $InputFullPath" -ForegroundColor Cyan
Write-Host "Wyjście : $OutputFullPath" -ForegroundColor Cyan

# ── Uruchom Word ─────────────────────────────────────────────────────────────
try {
    $Word = New-Object -ComObject Word.Application
} catch {
    Write-Error "Nie można uruchomić Microsoft Word. Sprawdź czy Word jest zainstalowany."
    exit 1
}
$Word.Visible = $false
$Word.DisplayAlerts = 0  # wdAlertsNone

$Doc = $Word.Documents.Add()
$Doc.PageSetup.TopMargin    = $Word.CentimetersToPoints(2.0)
$Doc.PageSetup.BottomMargin = $Word.CentimetersToPoints(2.0)
$Doc.PageSetup.LeftMargin   = $Word.CentimetersToPoints(2.5)
$Doc.PageSetup.RightMargin  = $Word.CentimetersToPoints(2.0)

# ── Mapa styli: klucz EN -> polska nazwa w Word PL ───────────────────────────
$script:styleMap = @{
    "Normal"      = "Normalny"
    "Heading 1"   = "Nagłówek 1"
    "Heading 2"   = "Nagłówek 2"
    "Heading 3"   = "Nagłówek 3"
    "Title"       = "Tytuł"
    "List Bullet" = "Lista punktowana"
}

function Resolve-Style {
    param($Doc, $StyleKey)
    $name = if ($script:styleMap.ContainsKey($StyleKey)) { $script:styleMap[$StyleKey] } else { $StyleKey }
    try {
        return $Doc.Styles($name)
    } catch {
        Write-Warning "Styl '$name' niedostepny — uzywam Normalny"
        return $Doc.Styles("Normalny")
    }
}

# ── Style ─────────────────────────────────────────────────────────────────────
function Set-WordStyle {
    param($Doc, $StyleName, $FontName, $FontSize, [bool]$Bold, $SpaceBefore, $SpaceAfter, $ColorIndex)
    try {
        $style = Resolve-Style $Doc $StyleName
        $style.Font.Name      = $FontName
        $style.Font.Size      = $FontSize
        $style.Font.Bold      = $Bold
        $style.ParagraphFormat.SpaceBefore = $SpaceBefore
        $style.ParagraphFormat.SpaceAfter  = $SpaceAfter
        if ($null -ne $ColorIndex) { $style.Font.ColorIndex = $ColorIndex }
    } catch {
        Write-Warning "Styl '$StyleName' — blad formatowania: $_"
    }
}

# wdColorDarkBlue = 9, wdColorBlack = 1
Set-WordStyle $Doc "Heading 1" "Calibri" 14 $true  12 6  9
Set-WordStyle $Doc "Heading 2" "Calibri" 12 $true   8 4  1
Set-WordStyle $Doc "Normal"    "Calibri" 11 $false  2 2  1

# ── Helper: dodaj akapit z tekstem i stylem ───────────────────────────────────
function Add-Paragraph {
    param($Doc, [string]$Text, $Style = "Normal", [bool]$Bold = $false)

    $resolvedStyle = Resolve-Style $Doc $Style

    # Usuń pierwszą pustą linię w nowym dokumencie (Word zawsze zaczyna z jednym akapitem)
    if ($script:isFirstParagraph) {
        $range = $Doc.Content
        $range.Style = $resolvedStyle
        $range.Text  = $Text
        if ($Bold) { $range.Bold = $true }
        $script:isFirstParagraph = $false
        return $range
    }

    $range = $Doc.Content
    $range.Collapse(0)  # wdCollapseEnd = 0
    $range.InsertParagraphAfter()
    $range.Collapse(0)
    $range.Style = $resolvedStyle
    $range.Text  = $Text
    if ($Bold) { $range.Bold = $true }
    return $range
}

$script:isFirstParagraph = $true

# ── Parsuj Markdown i buduj dokument ─────────────────────────────────────────
$lines = Get-Content -Path $InputFullPath -Encoding UTF8

$inAnswer   = $false
$bufferText = ""

function Flush-Buffer {
    param($Doc)
    if ($script:bufferText.Trim() -ne "") {
        Add-Paragraph $Doc $script:bufferText.Trim() "Normal" | Out-Null
        $script:bufferText = ""
    }
}

foreach ($rawLine in $lines) {
    $line = $rawLine.TrimEnd()

    # ── Tytuł dokumentu (# TYTUŁ)
    if ($line -match '^# (.+)$') {
        Flush-Buffer $Doc
        $text = $Matches[1].Trim()
        $para = Add-Paragraph $Doc $text "Title"
        if ($null -ne $para) {
            $para.ParagraphFormat.Alignment = 1  # wdAlignParagraphCenter
        }
        continue
    }

    # ── Nagłówek sekcji (## 1. SEKCJA)
    if ($line -match '^## (.+)$') {
        Flush-Buffer $Doc
        $text = $Matches[1].Trim()
        Add-Paragraph $Doc $text "Heading 1" | Out-Null
        continue
    }

    # ── Pytanie (### 1. Pytanie?)
    if ($line -match '^### (.+)$') {
        Flush-Buffer $Doc
        $text = $Matches[1].Trim()
        Add-Paragraph $Doc $text "Heading 2" | Out-Null
        continue
    }

    # ── Separator (---)
    if ($line -match '^---+$') {
        Flush-Buffer $Doc
        try {
            $range = $Doc.Content
            $range.Collapse(0)
            $range.InsertParagraphAfter()
            $range.Collapse(0)
            $range.Borders.Item(-1).LineStyle = 1  # wdBorderTop=-1, wdLineStyleSingle=1
            $range.Borders.Item(-1).LineWidth = 2
            $range.Text = " "
        } catch {
            Add-Paragraph $Doc "─────────────────────────────────────" "Normal" | Out-Null
        }
        continue
    }

    # ── Punkt listy (- tekst lub * tekst)
    if ($line -match '^[\-\*] (.+)$') {
        Flush-Buffer $Doc
        $text = $Matches[1].Trim()
        Add-Paragraph $Doc ("• " + $text) "List Bullet" | Out-Null
        continue
    }

    # ── Cytat/źródło (> Źródło: ...)
    if ($line -match '^> (.+)$') {
        Flush-Buffer $Doc
        $text = $Matches[1].Trim()
        $para = Add-Paragraph $Doc $text "Normal" | Out-Null
        # kursywa dla źródła — znajdź ostatnio dodany akapit
        $lastPara = $Doc.Paragraphs.Last
        if ($null -ne $lastPara) {
            $lastPara.Range.Italic = $true
            $lastPara.Range.Font.ColorIndex = 7  # wdColorGray50
        }
        continue
    }

    # ── Pusta linia — flush bufora jako osobny akapit
    if ($line.Trim() -eq "") {
        Flush-Buffer $Doc
        continue
    }

    # ── Zwykły tekst — akumuluj w buforze (wieloliniowe zdania)
    if ($bufferText -ne "") {
        $bufferText += " " + $line.Trim()
    } else {
        $bufferText = $line.Trim()
    }
}

# Flush reszty
Flush-Buffer $Doc

# ── Numeracja stron ───────────────────────────────────────────────────────────
try {
    $footer = $Doc.Sections(1).Footers(1)  # wdHeaderFooterPrimary = 1
    $footer.LinkToPrevious = $false
    $footer.Range.ParagraphFormat.Alignment = 1  # center
    $footer.Range.Fields.Add($footer.Range, -33, $true) | Out-Null  # wdFieldPage = 33
} catch {
    Write-Warning "Nie udalo sie dodac numeracji stron: $_"
}

# ── Zapisz plik ───────────────────────────────────────────────────────────────
Write-Host "Zapisuję: $OutputFullPath" -ForegroundColor Green
$Doc.SaveAs([ref]$OutputFullPath, [ref]16)  # wdFormatDocumentDefault = 16
$Doc.Close($false)
$Word.Quit()

# Zwolnij COM
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Word) | Out-Null
Remove-Variable Word

Write-Host "✓ Dokument wygenerowany: $OutputFullPath" -ForegroundColor Green
Write-Host "  Rozmiar: $([Math]::Round((Get-Item $OutputFullPath).Length / 1KB, 1)) KB"

# ── Zaktualizuj QA_LOG.md ─────────────────────────────────────────────────────
$logFile = Join-Path $WorkspaceRoot "docs\QA_LOG.md"
if (Test-Path $logFile) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    $logEntry = @"

## v$Version — $date
- Plik: `PLC_Commissioner_QA_v${Version}.docx`
- Wygenerowano z: `$InputFile`
- Rozmiar: $([Math]::Round((Get-Item $OutputFullPath).Length / 1KB, 1)) KB

"@
    Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
    Write-Host "✓ Zaktualizowano QA_LOG.md" -ForegroundColor Green
}
