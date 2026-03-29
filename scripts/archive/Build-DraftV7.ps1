
# Build-DraftV7.ps1
# Transformuje qa_v6_raw.txt -> qa_draft_v7.md:
#   - Usuwa sekcje 17 (Elektrotechnika) i ŚCIĄGA
#   - Przemianowuje: 18->17, 19->18
#   - Dodaje naglowek i append slownik_v7.md jako sekcja 19

param(
    [string]$InputFile  = "docs\qa_v6_raw.txt",
    [string]$SlownikFile = "docs\slownik_v7.md",
    [string]$OutputFile = "docs\qa_draft_v7.md"
)

$root = Split-Path $PSScriptRoot
Set-Location $root

$raw = Get-Content $InputFile -Raw -Encoding UTF8

# --- Usun sekcje 17 Elektrotechnika (od " 17." do " 18.") ---
$s17 = $raw.IndexOf("17. ELEKTROTECHNIKA")
$s18 = $raw.IndexOf("18. REALNE")
if ($s17 -lt 0 -or $s18 -lt 0) {
    Write-Warning "Nie znaleziono sekcji 17 lub 18 — sprawdz plik wejsciowy"
    exit 1
}
$before = $raw.Substring(0, $s17)
$after  = $raw.Substring($s18)

# --- Przemianuj sekcje 18->17, 19->18 ---
$after = $after -replace "18\. REALNE SCENARIUSZE", "17. REALNE SCENARIUSZE"
$after = $after -replace "19\. TIA PORTAL", "18. TIA PORTAL"

# --- Usun SCIGARA / jednozdaniowe definicje na koncu ---
$cutMarkers = @("ŚCIĄGA —", "SCIGARA —", "Każde pojęcie musisz")
$cutPos = -1
foreach ($marker in $cutMarkers) {
    $pos = $after.IndexOf($marker)
    if ($pos -ge 0 -and ($cutPos -lt 0 -or $pos -lt $cutPos)) {
        $cutPos = $pos
    }
}
if ($cutPos -ge 0) {
    $after = $after.Substring(0, $cutPos).TrimEnd()
}

# --- Naglowek dokumentu ---
$header = @"
# KOMPENDIUM Q&A
### PLC Programmer / Commissioner / Automatyk
### Siemens TIA Portal · Safety PLC · ET200 · Napedy SINAMICS · Robot ABB · SICAR
### Pytania + odpowiedzi zweryfikowane pod katem rozmow kwalifikacyjnych.
### Zrodla: Siemens Application Example 21064024 (E-Stop SIL3 V7.0.1), Wiring Examples 39198632, SIMATIC Safety Integrated dokumentacja.
---

"@

# --- Lacz i zapisz podstawe ---
$base = $header + $before + $after

# --- Dolacz slownik ---
if (Test-Path $SlownikFile) {
    $slownik = Get-Content $SlownikFile -Raw -Encoding UTF8
    $base = $base.TrimEnd() + "`n`n---`n`n" + $slownik.TrimStart()
} else {
    Write-Warning "Brak pliku slownika: $SlownikFile"
}

# --- Zapisz ---
Set-Content $OutputFile -Value $base -Encoding UTF8
$lines = (Get-Content $OutputFile).Count
Write-Host "OK: $OutputFile ($lines linii)"
