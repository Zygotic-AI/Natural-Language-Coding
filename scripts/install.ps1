# Natural Language Coding — install portable skills (Windows PowerShell 5.1+ / PowerShell 7+).
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# ADR 0013 — requirements preflight
$ScriptDirEarly = Split-Path -Parent $MyInvocation.MyCommand.Path
$PlanitMarkerEarly = Join-Path $ScriptDirEarly '..\.agents\skills\planit\SKILL.md'
$ReqMissing = [System.Collections.Generic.List[string]]::new()
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) {
    $ReqMissing.Add('python (or py launcher)')
}
if (-not (Test-Path -LiteralPath $PlanitMarkerEarly)) {
    if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue) -and -not (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue)) {
        $ReqMissing.Add('curl or Invoke-WebRequest')
    }
}
if ($ReqMissing.Count -gt 0) {
    Write-Host 'Install cannot continue — missing required tools.' -ForegroundColor Red
    foreach ($m in $ReqMissing) { Write-Host "  What's wrong: missing $m" }
    Write-Host '  Fix: install the tools above, or clone this repo and run install.ps1'
    exit 1
}

$NlcRepoSlug = if ($env:NLC_REPO_SLUG) { $env:NLC_REPO_SLUG } else { 'Zygotic-AI/Natural-Language-Coding' }
$NlcRawBase = if ($env:NLC_RAW_BASE) { $env:NLC_RAW_BASE } else { "https://raw.githubusercontent.com/$NlcRepoSlug/main" }
$InstallRoot = if ($env:NLC_INSTALL_ROOT) { $env:NLC_INSTALL_ROOT } else { Join-Path $env:USERPROFILE '.local\share\nlc' }
$Py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$AgentsSkills = Join-Path $env:USERPROFILE '.agents\skills'
$CursorSkills = Join-Path $env:USERPROFILE '.cursor\skills'
$CursorSkillsRepo = @('bbp-confirmer', 'bbp-proposer', 'bbp-recorder', 'bbp-reviewer', 'interview', 'planit', 'verify')

Write-Host 'Natural Language Coding — install'
Write-Host "  target: $InstallRoot"
Write-Host "  skills: $AgentsSkills"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LocalHub = Join-Path $ScriptDir '..'
$PlanitMarker = Join-Path $LocalHub '.agents\skills\planit\SKILL.md'
$SrcRoot = $null
$TempDir = $null

function Invoke-NlcFetchHub {
    param([string[]]$ExtraArgs)
    $Va = @()
    if ($Py -eq 'py') { $Va += '-3' }
    $Va += $FetchScript
    $Va += $ExtraArgs
    & $Py @Va
    if ($LASTEXITCODE -ne 0) { throw 'nlc-fetch-hub failed' }
}

New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null
New-Item -ItemType Directory -Path $AgentsSkills -Force | Out-Null

if (Test-Path -LiteralPath $PlanitMarker) {
    $SrcRoot = (Resolve-Path $LocalHub).Path
    Write-Host "  source: local repo $SrcRoot"
    $FetchScript = Join-Path $SrcRoot 'tools\nlc-fetch-hub.py'
    Invoke-NlcFetchHub @('--install-root', $InstallRoot, '--from-path', $SrcRoot)
    $SrcRoot = Join-Path $InstallRoot 'hub'
}
else {
    $TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ('nlc-install-' + [guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    $ToolDir = Join-Path $TempDir 'nlc-tools'
    New-Item -ItemType Directory -Path $ToolDir -Force | Out-Null
    $files = @('nlc-fetch-hub.py', 'nlc_distribution.py', 'nlc_requirements.py')
    foreach ($f in $files) {
        $url = "$NlcRawBase/tools/$f"
        $dest = Join-Path $ToolDir $f
        if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
            & curl.exe -fsSL $url -o $dest
        }
        else {
            Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
        }
    }
    $FetchScript = Join-Path $ToolDir 'nlc-fetch-hub.py'
    $fetchArgs = @('--install-root', $InstallRoot, '--repo', $NlcRepoSlug)
    if ($env:NLC_VERSION) {
        $fetchArgs += @('--version', $env:NLC_VERSION)
    }
    elseif ($env:NLC_REF) {
        $ver = $env:NLC_REF -replace '^v', ''
        $fetchArgs += @('--version', $ver)
    }
    Write-Host '  source: release tarball (latest semver unless NLC_VERSION/NLC_REF set)'
    Invoke-NlcFetchHub -ExtraArgs $fetchArgs
    $SrcRoot = Join-Path $InstallRoot 'hub'
}

$SkillsSrc = Join-Path $SrcRoot '.agents\skills'
if (-not (Test-Path -LiteralPath $SkillsSrc)) {
    Write-Error "missing $SkillsSrc"
}
Copy-Item -Path (Join-Path $SkillsSrc '*') -Destination $AgentsSkills -Recurse -Force

$HubDest = $SrcRoot

$CursorHome = Join-Path $env:USERPROFILE '.cursor'
if (Test-Path -LiteralPath $CursorHome) {
    New-Item -ItemType Directory -Path $CursorSkills -Force | Out-Null
    foreach ($skill in $CursorSkillsRepo) {
        $FromCursor = Join-Path $SrcRoot (Join-Path '.cursor\skills' $skill)
        $FromAgents = Join-Path $SkillsSrc $skill
        $From = if (Test-Path -LiteralPath $FromCursor) { $FromCursor } elseif (Test-Path -LiteralPath $FromAgents) { $FromAgents } else { $null }
        if ($From) {
            $Dest = Join-Path $CursorSkills $skill
            if (Test-Path -LiteralPath $Dest) {
                Remove-Item -LiteralPath $Dest -Recurse -Force
            }
            Copy-Item -LiteralPath $From -Destination $Dest -Recurse -Force
        }
    }
    Write-Host '  cursor: copied repo-local BBP + planit skills'
}

if (-not $env:NLC_SKIP_VERIFY) {
    $Verify = Join-Path $HubDest 'tools\nlc-install-verify.py'
    if (Test-Path -LiteralPath $Verify) {
        Write-Host '  verify: hub file hashes'
        $Py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
        $Va = @()
        if ($Py -eq 'py') { $Va += '-3' }
        $Va += $Verify
        $Va += $HubDest
        & $Py @Va
        if ($LASTEXITCODE -ne 0) {
            Write-Host 'Install could not verify the compiler file fingerprints.' -ForegroundColor Red
            Write-Host "  What's wrong: hub files do not match published fingerprints"
            Write-Host '  Fix: re-run install from a clean checkout, or repair the hub tree.'
            Write-Host '  Optional: NLC_SKIP_VERIFY=1 only if you accept running an unverified hub.'
            [Console]::Error.WriteLine('INSTALL:NOT_MET hub verify failed')
            exit 1
        }
    }
}

if ($TempDir -and (Test-Path -LiteralPath $TempDir)) {
    Remove-Item -LiteralPath $TempDir -Recurse -Force
}

$CurrentFile = Join-Path $InstallRoot 'current'
if (Test-Path -LiteralPath $CurrentFile) {
    Write-Host "  hub version: $((Get-Content -LiteralPath $CurrentFile -Raw).Trim())"
}

$HubTools = Join-Path $HubDest 'tools'
Write-Host ''
Write-Host 'Done.'
Write-Host ''
Write-Host "Hub copy (tools, charter): $HubDest"
Write-Host "Portable skills: $AgentsSkills"
Write-Host ''
Write-Host 'Next:'
Write-Host '  Run ./nlc in your app repo (or nlc on PATH). See docs\nlc\MENU.md under hub.'
Write-Host ''
Write-Host "Greenfield scaffold: python $($HubTools)\nlc-init.py $env:USERPROFILE\projects\my-app --name MyApp"
Write-Host ''
$UserBin = Join-Path $env:USERPROFILE '.local\bin'
New-Item -ItemType Directory -Path $UserBin -Force | Out-Null
$NlcCmdSrc = Join-Path $HubDest 'templates\adopter\nlc.cmd'
if (Test-Path -LiteralPath $NlcCmdSrc) {
    Copy-Item -LiteralPath $NlcCmdSrc -Destination (Join-Path $UserBin 'nlc.cmd') -Force
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if ($userPath -notlike "*$UserBin*") {
        [Environment]::SetEnvironmentVariable('Path', "$userPath;$UserBin", 'User')
        Write-Host "  PATH: added $UserBin (new shells)"
    }
    Write-Host "  command: $(Join-Path $UserBin 'nlc.cmd')"
}
Write-Host 'Verify (in app repo):'
Write-Host '  ./nlc verify'
Write-Host '  ./nlc verify-deep'
