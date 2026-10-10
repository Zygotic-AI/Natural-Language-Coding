# Thin entrypoint. Policy lives in goals/hub_install/execute.ps1.
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
& (Join-Path $Root 'goals\hub_install\execute.ps1') @args
if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
