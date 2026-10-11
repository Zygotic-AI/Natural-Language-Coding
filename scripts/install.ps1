# Thin entrypoint. Policy lives in goals/hub_install/execute.ps1.
$ErrorActionPreference = 'Stop'
$Here = $MyInvocation.MyCommand.Path
if ($Here) {
  $Root = Split-Path -Parent (Split-Path -Parent $Here)
  $Execute = Join-Path $Root 'goals\hub_install\execute.ps1'
  if (Test-Path -LiteralPath $Execute) {
    & $Execute @args
    if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    exit 0
  }
}

$NlcRepoSlug = if ($env:NLC_REPO_SLUG) { $env:NLC_REPO_SLUG } else { 'Zygotic-AI/Natural-Language-Coding' }
$NlcRef = if ($env:NLC_REF) { $env:NLC_REF } else { 'main' }
$NlcRawBase = if ($env:NLC_RAW_BASE) { $env:NLC_RAW_BASE } else { "https://raw.githubusercontent.com/$NlcRepoSlug/$NlcRef" }

$Tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("nlc-install-" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $Tmp -Force | Out-Null

if ($NlcRawBase -like 'file://*') {
  $LocalRoot = $NlcRawBase.Substring(7)
  $ExecuteLocal = Join-Path $LocalRoot 'goals\hub_install\execute.ps1'
  & $ExecuteLocal @args
  if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  exit 0
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error 'Piped install requires git to fetch the hub.'
}
$CloneUrl = "https://github.com/$NlcRepoSlug.git"
$RepoDir = Join-Path $Tmp 'repo'
git clone --depth 1 --branch $NlcRef $CloneUrl $RepoDir
$ExecuteRemote = Join-Path $RepoDir 'goals\hub_install\execute.ps1'
& $ExecuteRemote @args
if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
