<#
.SYNOPSIS
    Pełny pipeline: build_toc → merge_chapters → LATEST → build_manifest → index.md → git push.
.DESCRIPTION
    1. python build_toc.py        — generuje TOC w 00_header.md z chapter files
    2. python merge_chapters.py   — scala chapters → qa_draft_v12.md
    3. Kopiuje draft → LATEST.md
    4. python build_manifest.py   — aktualizuje sections_manifest.json
    5. Kopiuje LATEST.md → index.md (GitHub Pages)
    6. git add + commit + push
.EXAMPLE
    .\scripts\publish.ps1
    .\scripts\publish.ps1 -Message "Dodano sekcję 21"
    .\scripts\publish.ps1 -NoPush   # cały pipeline bez git push
#>
param(
    [string]$Message = "Update kompendium Q&A site",
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root

try {
    # --- 1. Build TOC ---
    Write-Host "[1/6] Generowanie TOC z chapter files..." -ForegroundColor Cyan
    python scripts/build_toc.py
    if ($LASTEXITCODE -ne 0) { throw "build_toc.py failed" }

    # --- 2. Merge chapters ---
    Write-Host "`n[2/6] Scalanie chapters..." -ForegroundColor Cyan
    python scripts/merge_chapters.py
    if ($LASTEXITCODE -ne 0) { throw "merge_chapters.py failed" }

    # --- 3. Copy to LATEST.md ---
    Write-Host "`n[3/6] Kopiowanie draft -> LATEST.md..." -ForegroundColor Cyan
    Copy-Item docs/qa_draft_v12.md docs/LATEST.md -Force
    Write-Host "   -> docs/LATEST.md" -ForegroundColor Green

    # --- 4. Build manifest ---
    Write-Host "`n[4/6] Budowanie manifestu..." -ForegroundColor Cyan
    python scripts/build_manifest.py
    if ($LASTEXITCODE -ne 0) { throw "build_manifest.py failed" }

    # --- 5. Copy to index.md (GitHub Pages) ---
    Write-Host "`n[5/6] Kopiowanie LATEST.md -> index.md..." -ForegroundColor Cyan
    Copy-Item docs/LATEST.md docs/index.md -Force
    $lines = (Get-Content docs/index.md).Count
    Write-Host "   -> docs/index.md ($lines linii)" -ForegroundColor Green

    # --- 6. Git commit + push ---
    Write-Host "`n[6/6] Git commit..." -ForegroundColor Cyan
    git add docs/
    $status = git diff --cached --stat
    if (-not $status) {
        Write-Host "   -> Brak zmian do commitu." -ForegroundColor Yellow
        return
    }
    git commit -m $Message

    if ($NoPush) {
        Write-Host "Push pominięty (-NoPush)" -ForegroundColor Yellow
    } else {
        Write-Host "Push na GitHub..." -ForegroundColor Cyan
        git push origin master
        Write-Host "`nGotowe! Strona zaktualizuje się za ~30s:" -ForegroundColor Green
        Write-Host "https://sm000k.github.io/plc-commissioner-qa/" -ForegroundColor White
    }

    # --- Quick audit (non-blocking, co 3 dni) ---
    $auditScript = Join-Path $PSScriptRoot "audit_project.ps1"
    $auditStamp  = Join-Path $root ".last_audit"
    $runAudit = $true
    if (Test-Path $auditStamp) {
        $lastRun = (Get-Item $auditStamp).LastWriteTime
        if (((Get-Date) - $lastRun).TotalDays -lt 3) { $runAudit = $false }
    }
    if ($runAudit -and (Test-Path $auditScript)) {
        Write-Host "`n[audit] Sprawdzanie higieny projektu..." -ForegroundColor DarkGray
        & $auditScript 2>$null
        [IO.File]::WriteAllText($auditStamp, (Get-Date).ToString("o"))
    }
} finally {
    Pop-Location
}
