<#
Simple script PowerShell pour initialiser git, committer et pousser vers un remote GitHub.
Usage:
  powershell -ExecutionPolicy Bypass -File .\deploy_to_github_fixed.ps1 -RemoteUrl "https://github.com/username/repo.git"
#>
param(
    [string]$RemoteUrl
)

function ExitWith {
    param([string]$msg)
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

Set-Location -Path $PSScriptRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    ExitWith "Git n'est pas installé ou introuvable dans le PATH. Installez Git depuis https://git-scm.com/downloads"
}

$inside = $false
try {
    $result = git rev-parse --is-inside-work-tree 2>$null
    if ($result -eq 'true') { $inside = $true }
} catch {
    $inside = $false
}

if (-not $inside) {
    git init
    if ($LASTEXITCODE -ne 0) { ExitWith "Impossible d'initialiser le dépôt git." }
    Write-Host "Dépôt git initialisé." -ForegroundColor Green
}

git add .
if ($LASTEXITCODE -ne 0) { ExitWith "git add a échoué." }

$changes = git status --porcelain
if ($changes) {
    git commit -m "Prepare project for Render deployment"
    if ($LASTEXITCODE -ne 0) { ExitWith "git commit a échoué." }
    Write-Host "Modifications committées." -ForegroundColor Green
} else {
    Write-Host "Aucun changement à committer." -ForegroundColor Yellow
}

if (-not $RemoteUrl) {
    ExitWith "Aucune URL de remote fournie. Utilisez -RemoteUrl 'https://github.com/username/repo.git'"
}

git remote remove origin 2>$null | Out-Null

git remote add origin $RemoteUrl
if ($LASTEXITCODE -ne 0) { ExitWith "Ajout du remote a échoué." }

git branch -M main
if ($LASTEXITCODE -ne 0) { ExitWith "git branch -M main a échoué." }

git push -u origin main
if ($LASTEXITCODE -ne 0) { ExitWith "Push vers le remote a échoué." }

Write-Host "Push effectué vers $RemoteUrl" -ForegroundColor Green
Write-Host "
Étapes suivantes : créer un service Render, configurer les variables et exécuter migrate/collectstatic." -ForegroundColor Cyan
