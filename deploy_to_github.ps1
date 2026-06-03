<#
Script: deploy_to_github.ps1
Usage:
  - To create a repo with GitHub CLI (recommended):
      powershell -ExecutionPolicy Bypass -File deploy_to_github.ps1 -CreateWithGH
  - To push to an existing remote URL:
      powershell -ExecutionPolicy Bypass -File deploy_to_github.ps1 -RemoteUrl "https://github.com/username/repo.git"

What it does:
  - checks for git
  - initializes repo if needed
  - creates commit
  - if -CreateWithGH is set and `gh` exists, creates a GitHub repo and pushes
  - else pushes to provided remote URL

Note: This script runs locally and requires your credentials (gh or git remote)
#>
param(
    [switch]$CreateWithGH,
    [string]$RemoteUrl
)

function ExitWith {
    param([string]$msg)
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

# Ensure we're in script folder (project root)
Set-Location -Path $PSScriptRoot

# Check git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    ExitWith "Git n'est pas installé ou introuvable dans le PATH. Installez Git et réessayez."
}

# Initialize if needed
$inside = $false
try {
    $result = git rev-parse --is-inside-work-tree 2>$null
    if ($result -eq 'true') { $inside = $true }
} catch {
    $inside = $false
}

if (-not $inside) {
    git init
    if ($LASTEXITCODE -ne 0) { ExitWith "Impossible d'initialiser le dépôt git" }
    Write-Host "Dépôt git initialisé." -ForegroundColor Green
}

# Add and commit
git add .
if ($LASTEXITCODE -ne 0) { ExitWith "git add a échoué" }

# Commit if there are changes
$changes = git status --porcelain
if ($changes) {
    git commit -m "Prepare project for Render deployment"
    if ($LASTEXITCODE -ne 0) { ExitWith "git commit a échoué" }
    Write-Host "Modifications committées." -ForegroundColor Green
} else {
    Write-Host "Aucun changement à committer." -ForegroundColor Yellow
}

# Push logic
if ($CreateWithGH) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        ExitWith "GitHub CLI 'gh' introuvable. Installez-la ou utilisez -RemoteUrl."
    }
    $folder = Split-Path -Leaf $PSScriptRoot
    gh repo create $folder --private --source=. --remote=origin --push
    if ($LASTEXITCODE -ne 0) { ExitWith "Création/push avec gh a échoué" }
    Write-Host "Repo créé et poussé avec gh." -ForegroundColor Green
} elseif ($RemoteUrl) {
    git remote remove origin 2>$null | Out-Null
    git remote add origin $RemoteUrl
    if ($LASTEXITCODE -ne 0) { ExitWith "Ajout du remote a échoué" }
    git branch -M main
    if ($LASTEXITCODE -ne 0) { ExitWith "git branch -M main a échoué" }
    git push -u origin main
    if ($LASTEXITCODE -ne 0) { ExitWith "Push vers le remote a échoué" }
    Write-Host "Push effectué vers $RemoteUrl" -ForegroundColor Green
} else {
    Write-Host "Aucun remote fourni. Si vous voulez que le script crée le repo GitHub, relancez avec -CreateWithGH (require gh CLI)." -ForegroundColor Yellow
}

Write-Host "`nÉtapes suivantes suggérées:" -ForegroundColor Cyan
Write-Host "1) Créer un service Web sur Render et connecter ce repo." -ForegroundColor Cyan
Write-Host "2) Dans Render, ajouter les variables d'environnement: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=your-app.onrender.com" -ForegroundColor Cyan
Write-Host "3) Exécuter en Shell Render: python manage.py migrate && python manage.py collectstatic --noinput" -ForegroundColor Cyan
