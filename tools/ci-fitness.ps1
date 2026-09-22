# Natural Language Coding — hub compile fitness (Windows native). ADR 0013.
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
$Tools = Split-Path -Parent $MyInvocation.MyCommand.Path
$Missing = @()
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) {
    $Missing += 'python (or py launcher)'
}
if ($Missing.Count -gt 0) {
    Write-Error ("REQUIREMENTS:NOT_MET`n" + (($Missing | ForEach-Object { "  missing: $_" }) -join "`n"))
}
$Py = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $Py = 'python' }
else { $Py = 'py' }
$Args = @()
if ($Py -eq 'py') { $Args += '-3' }
$ReqArgs = $Args + @(Join-Path $Tools 'nlc_requirements.py') + @('hub_prove')
& $Py @ReqArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$Args += (Join-Path $Tools 'ci_fitness.py')
& $Py @Args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
