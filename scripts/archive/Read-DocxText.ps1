<#
.SYNOPSIS
    Wyciąga czysty tekst z pliku .docx do analizy przez Copilot.

.DESCRIPTION
    Rozpakowuje .docx (ZIP) i ekstrahuje tekst z word/document.xml,
    usuwając tagi XML. Zachowuje podział na akapity.
    Używane w Fazie 1 workflowu generowania Q&A.

.PARAMETER Path
    Ścieżka do pliku .docx.

.PARAMETER OutputFile
    Ścieżka do pliku wyjściowego .txt.
    Domyślnie: [nazwa_pliku].txt w docs/

.EXAMPLE
    .\Read-DocxText.ps1 -Path "..\PLC_Commissioner_QA_v6.docx"

.EXAMPLE
    .\Read-DocxText.ps1 -Path "..\PLC_Commissioner_QA_v6.docx" -OutputFile "docs\qa_v6_text.txt"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path $_ -PathType Leaf })]
    [string]$Path,

    [string]$OutputFile = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$docxPath = Resolve-Path $Path
$workspaceRoot = Split-Path -Parent $PSScriptRoot

# Domyślna ścieżka wyjściowa
if ($OutputFile -eq "") {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($docxPath)
    $docsDir  = Join-Path $workspaceRoot "docs"
    if (-not (Test-Path $docsDir)) { New-Item -ItemType Directory -Path $docsDir | Out-Null }
    $OutputFile = Join-Path $docsDir "${baseName}_text.txt"
}

$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputFile)

Write-Host "Czytam: $docxPath" -ForegroundColor Cyan

# Rozpakuj .docx do katalogu tymczasowego
$tempDir = Join-Path $env:TEMP "docx_extract_$(Get-Random)"
try {
    Expand-Archive -Path $docxPath -DestinationPath $tempDir -Force

    $xmlFile = Join-Path $tempDir "word\document.xml"
    if (-not (Test-Path $xmlFile)) {
        Write-Error "Plik word/document.xml nie istnieje w archiwum: $docxPath"
        return
    }

    # Załaduj XML i wyciągnij tekst akapitami
    [xml]$xml = Get-Content $xmlFile -Encoding UTF8 -Raw

    # Namespace manager dla Word XML
    $nsm = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $nsm.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

    # Pobierz wszystkie akapity (<w:p>)
    $paragraphs = $xml.SelectNodes("//w:p", $nsm)
    $lines = [System.Collections.Generic.List[string]]::new()

    foreach ($para in $paragraphs) {
        # Pobierz styl akapitu
        $styleNode = $para.SelectSingleNode("w:pPr/w:pStyle", $nsm)
        $styleName = if ($null -ne $styleNode) { $styleNode.GetAttribute("val", "http://schemas.openxmlformats.org/wordprocessingml/2006/main") } else { "" }

        # Sprawdź pogrubienie akapitu (fallback gdy brak stylów)
        $boldNode = $para.SelectSingleNode(".//w:b", $nsm)
        $isBold   = $null -ne $boldNode

        # Zbierz tekst z wszystkich <w:t> w tym akapicie
        $textNodes = $para.SelectNodes(".//w:t", $nsm)
        $paraText  = ($textNodes | ForEach-Object { $_.InnerText }) -join ""

        if ($paraText.Trim() -ne "") {
            # Wykrywanie nagłówków: styl Word lub heurystyka tekstowa
            $prefix = switch -Regex ($styleName) {
                "^Heading1$|^berschrift1$|\d+nagłówek1" { "## " }
                "^Heading2$|^berschrift2$|\d+nagłówek2" { "### " }
                "^Title$"                                { "# " }
                default                                  { "" }
            }

            # Heurystyka gdy styl = Normal ale tekst wygląda jak sekcja
            # np. "1. PODSTAWY PLC I AUTOMATYKI" lub "19. TIA PORTAL — ZAAWANSOWANE"
            if ($prefix -eq "" -and $paraText -match '^\d{1,2}\. [A-ZĘÓĄŚŁŻŹĆŃ][A-ZĘÓĄŚŁŻŹĆŃIUEA /\-—]{5,}$') {
                $prefix = "## "
            }
            # Pytanie: "1. Co to jest PLC i czym różni się?"
            elseif ($prefix -eq "" -and $paraText -match '^\d{1,2}\. .{10,}\?$' -and $paraText.Length -lt 200) {
                $prefix = "### "
            }

            $lines.Add("${prefix}${paraText}")
        } else {
            $lines.Add("")  # Zachowaj puste wiersze
        }
    }

    # Zapisz do pliku
    $lines | Set-Content -Path $outputPath -Encoding UTF8
    Write-Host "✓ Tekst zapisany: $outputPath" -ForegroundColor Green
    Write-Host "  Liczba wierszy : $($lines.Count)"
    Write-Host "  Rozmiar        : $([Math]::Round((Get-Item $outputPath).Length / 1KB, 1)) KB"

    # Wypisz pierwsze 20 wierszy jako podgląd
    Write-Host "`n--- Podgląd (pierwsze 20 wierszy) ---" -ForegroundColor Yellow
    $lines | Select-Object -First 20 | ForEach-Object { Write-Host $_ }

} finally {
    # Sprzątanie
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
