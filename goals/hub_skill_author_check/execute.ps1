# Published-skill author checklist (same list before release and after install).
#
# Input: optional --root <skills-tree>. Default: <repo>\.agents\skills.
# Output: child SKILL_AUTHOR:MET|NOT_MET lines; this script exits with the child.
# Failure mode: exit 0 = MET; non-zero = NOT_MET (missing CLI or checklist fail).
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$SkillsRoot = Join-Path $Root '.agents\skills'
if ($args.Count -ge 2 -and $args[0] -eq '--root') {
    $SkillsRoot = [string]$args[1]
}
elseif ($args.Count -eq 1 -and $args[0] -eq '--root') {
    [Console]::Error.WriteLine('SKILL_AUTHOR:NOT_MET --root needs a path')
    exit 2
}

$Cli = Join-Path $Root 'tools\nlc-skill-author-check.py'
if (-not (Test-Path -LiteralPath $Cli)) {
    [Console]::Error.WriteLine('SKILL_AUTHOR:NOT_MET missing tools/nlc-skill-author-check.py')
    exit 1
}

$Py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$Va = @()
if ($Py -eq 'py') { $Va += '-3' }
$Va += $Cli
$Va += '--root'
$Va += $SkillsRoot
& $Py @Va
exit $LASTEXITCODE
