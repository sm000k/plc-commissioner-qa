<#
.SYNOPSIS
    Audyt projektu: wykrywa śmieci, nieużywane pliki, nieaktualne referencje.
.DESCRIPTION
    Sprawdza:
    1. desktop.ini śledzone w git
    2. Stare drafty qa_draft_v*.md w docs/ (powinny być w archive/)
    3. Pliki w docs/ niereferencjonowane przez pipeline
    4. Skrypty jednorazowe w scripts/ (nie w archive/)
    5. Zgodność README.md z aktualną wersją
    6. Zgodność copilot-instructions.md z aktualną wersją
.EXAMPLE
    .\scripts\audit_project.ps1          # tylko raport
    .\scripts\audit_project.ps1 -Fix     # raport + automatyczna naprawa
#>
param(
    [switch]$Fix
)

$ErrorActionPreference = 'Continue'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root

$issues = @()
$fixed  = @()

function Add-Issue {
    param([string]$Category, [string]$File, [string]$Message, [string]$FixAction)
    $script:issues += [PSCustomObject]@{
        Category  = $Category
        File      = $File
        Message   = $Message
        FixAction = $FixAction
    }
}

Write-Host "=== AUDYT PROJEKTU ===" -ForegroundColor Cyan
Write-Host ""

# ─────────────────────────────────────────────
# 1. desktop.ini tracked in git
# ─────────────────────────────────────────────
Write-Host "[1/6] Sprawdzanie desktop.ini w git..." -ForegroundColor Yellow
$desktopIni = git ls-files --cached | Select-String "desktop\.ini"
foreach ($f in $desktopIni) {
    Add-Issue "GIT_HYGIENE" $f.Line "desktop.ini śledzony w git" "git rm --cached"
}

if ($Fix -and $desktopIni.Count -gt 0) {
    $paths = $desktopIni | ForEach-Object { $_.Line }
    git rm --cached @paths 2>$null
    # Ensure .gitignore has desktop.ini
    $gitignore = Get-Content .gitignore -Raw
    if ($gitignore -notmatch 'desktop\.ini') {
        Add-Content .gitignore "`ndesktop.ini"
    }
    $fixed += "Usunięto $($desktopIni.Count) desktop.ini z git tracking"
}

# ─────────────────────────────────────────────
# 2. Old drafts in docs/ (should be in archive/)
# ─────────────────────────────────────────────
Write-Host "[2/6] Szukanie starych draftów w docs/..." -ForegroundColor Yellow
# Find current draft version from LATEST.md header
$currentDraft = $null
$headerLine = Get-Content docs/chapters/00_header.md -First 1
if ($headerLine -match 'v(\d+)') {
    $currentVersion = [int]$Matches[1]
}

Get-ChildItem docs/qa_draft_v*.md | ForEach-Object {
    if ($_.Name -match 'qa_draft_v(\d+)') {
        $ver = [int]$Matches[1]
        if ($ver -lt $currentVersion) {
            Add-Issue "OLD_DRAFT" $_.Name "Stary draft v$ver (aktywny: v$currentVersion)" "Move-Item -> archive/"
            if ($Fix) {
                Move-Item $_.FullName "archive/$($_.Name)" -Force
                git add -u "docs/$($_.Name)" 2>$null
                git add "archive/$($_.Name)" 2>$null
                $fixed += "Przeniesiono $($_.Name) → archive/"
            }
        }
    }
}

# ─────────────────────────────────────────────
# 3. Unused files in docs/
# ─────────────────────────────────────────────
Write-Host "[3/6] Sprawdzanie nieużywanych plików w docs/..." -ForegroundColor Yellow

# Files that ARE used (whitelist)
$usedFiles = @(
    'LATEST.md', 'index.md', "qa_draft_v$currentVersion.md",
    'sections_manifest.json', 'QA_LOG.md', 'REFERENCE.md',
    '_config.yml',
    'knowledge_base_controlbyte.md', 'knowledge_base_delta_v11.md'
)

Get-ChildItem docs/ -File | Where-Object {
    $_.Name -notin $usedFiles -and
    $_.Extension -notin @('.ini') -and
    $_.Name -ne 'desktop.ini'
} | ForEach-Object {
    # Check if referenced in LATEST.md, copilot-instructions, or any script
    $name = $_.Name
    $referenced = $false

    # Check in key files
    $checkFiles = @(
        'docs/LATEST.md',
        '.github/copilot-instructions.md',
        'scripts/publish.ps1',
        'scripts/merge_chapters.py',
        'scripts/build_toc.py',
        'scripts/build_manifest.py'
    )
    foreach ($cf in $checkFiles) {
        if (Test-Path $cf) {
            if ((Get-Content $cf -Raw) -match [regex]::Escape($name)) {
                $referenced = $true
                break
            }
        }
    }

    if (-not $referenced) {
        Add-Issue "UNUSED_FILE" "docs/$name" "Plik niereferencjonowany przez pipeline ani instrukcje" "Sprawdź ręcznie"
    }
}

# ─────────────────────────────────────────────
# 4. One-time scripts not in archive/
# ─────────────────────────────────────────────
Write-Host "[4/6] Sprawdzanie jednorazowych skryptów..." -ForegroundColor Yellow

# Scripts used in pipeline
$pipelineScripts = @(
    'publish.ps1', 'merge_chapters.py', 'build_toc.py', 'build_manifest.py',
    'split_chapters.py', 'validate_qa.py', 'egzaminator.py',
    'extract_pdfs.py', 'split_knowledge_base.py',
    'Get-YouTubeTranscripts.py', 'Build-KnowledgeBase.py', 'Merge-KnowledgeBase.py',
    '_build_selection.py', 'build_toc.py', 'audit_project.ps1'
)

Get-ChildItem scripts/ -File | Where-Object {
    $_.Name -notin $pipelineScripts -and
    $_.Name -ne 'desktop.ini'
} | ForEach-Object {
    Add-Issue "ORPHAN_SCRIPT" "scripts/$($_.Name)" "Skrypt nie w pipeline — rozważ przeniesienie do scripts/archive/" "Move-Item -> scripts/archive/"
    if ($Fix) {
        Move-Item $_.FullName "scripts/archive/$($_.Name)" -Force
        git add -u "scripts/$($_.Name)" 2>$null
        git add "scripts/archive/$($_.Name)" 2>$null
        $fixed += "Przeniesiono scripts/$($_.Name) → scripts/archive/"
    }
}

# ─────────────────────────────────────────────
# 5. README.md version check
# ─────────────────────────────────────────────
Write-Host "[5/6] Sprawdzanie aktualności README.md..." -ForegroundColor Yellow

if (Test-Path README.md) {
    $readmeContent = Get-Content README.md -Raw

    # Get actual question count from manifest
    if (Test-Path docs/sections_manifest.json) {
        $manifest = Get-Content docs/sections_manifest.json -Raw | ConvertFrom-Json
        $actualQuestions = $manifest.total_questions
        $actualSections = ($manifest.sections | Get-Member -MemberType NoteProperty).Count - 1  # minus header
    }

    # Check version in README
    if ($readmeContent -match 'v(\d+\.\d+).*?(\d+)\s*pyta..*?(\d+)\s*sekcj') {
        $readmeVersion = $Matches[1]
        $readmeQuestions = [int]$Matches[2]
        $readmeSections = [int]$Matches[3]

        # Get version from header
        $headerContent = Get-Content docs/chapters/00_header.md -Raw
        if ($headerContent -match 'v([\d.]+)\s*\|\s*Data:.*?\|\s*Pytania:\s*(\d+)') {
            $actualVersion = $Matches[1]
            $actualQ = [int]$Matches[2]
        }

        if ($readmeVersion -ne $actualVersion -or $readmeQuestions -ne $actualQ) {
            Add-Issue "OUTDATED_README" "README.md" "README: v$readmeVersion/$readmeQuestions Q — aktualny: v$actualVersion/$actualQ Q" "Zaktualizuj README.md"
        }
    }
}

# ─────────────────────────────────────────────
# 6. copilot-instructions.md version check
# ─────────────────────────────────────────────
Write-Host "[6/6] Sprawdzanie copilot-instructions.md..." -ForegroundColor Yellow

if (Test-Path '.github/copilot-instructions.md') {
    $ciContent = Get-Content '.github/copilot-instructions.md' -Raw
    $headerContent = Get-Content docs/chapters/00_header.md -Raw

    if ($headerContent -match 'v([\d.]+)\s*\|\s*Data:.*?\|\s*Pytania:\s*(\d+)') {
        $actualVersion = $Matches[1]
        $actualQ = [int]$Matches[2]
    }

    if ($ciContent -match '(\d+)\s*pyta.,\s*(\d+)\s*sekcj') {
        $ciQuestions = [int]$Matches[1]
        $ciSections = [int]$Matches[2]

        if ($ciQuestions -ne $actualQ) {
            Add-Issue "OUTDATED_CI" ".github/copilot-instructions.md" "copilot-instructions: $ciQuestions pytań — aktualny: $actualQ" "Zaktualizuj sekcję 'Aktywny dokument Q&A'"
        }
    }
}

# ─────────────────────────────────────────────
# RAPORT
# ─────────────────────────────────────────────
Write-Host ""
Write-Host "=== RAPORT ===" -ForegroundColor Cyan

if ($issues.Count -eq 0) {
    Write-Host "✅ Brak problemów — projekt jest czysty!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Znaleziono $($issues.Count) problemów:" -ForegroundColor Yellow
    Write-Host ""

    $grouped = $issues | Group-Object Category
    foreach ($group in $grouped) {
        $icon = switch ($group.Name) {
            'GIT_HYGIENE'    { '🗑️' }
            'OLD_DRAFT'      { '📦' }
            'UNUSED_FILE'    { '❓' }
            'ORPHAN_SCRIPT'  { '📜' }
            'OUTDATED_README'{ '📝' }
            'OUTDATED_CI'    { '⚙️' }
            default          { '•' }
        }
        Write-Host "$icon $($group.Name) ($($group.Count)):" -ForegroundColor White
        foreach ($item in $group.Group) {
            Write-Host "   $($item.File) — $($item.Message)" -ForegroundColor Gray
            if (-not $Fix) {
                Write-Host "     → $($item.FixAction)" -ForegroundColor DarkGray
            }
        }
        Write-Host ""
    }
}

if ($Fix -and $fixed.Count -gt 0) {
    Write-Host "✅ Naprawiono automatycznie:" -ForegroundColor Green
    foreach ($f in $fixed) {
        Write-Host "   • $f" -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "Uruchom: git commit -m 'Auto-cleanup by audit_project.ps1'" -ForegroundColor Cyan
}

if (-not $Fix -and $issues.Count -gt 0) {
    Write-Host "Uruchom z -Fix aby naprawić automatycznie:" -ForegroundColor Cyan
    Write-Host "  .\scripts\audit_project.ps1 -Fix" -ForegroundColor White
}

Pop-Location

# Return exit code for CI
if ($issues.Count -gt 0 -and -not $Fix) { exit 1 } else { exit 0 }
