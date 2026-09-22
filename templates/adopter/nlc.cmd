@echo off
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
if defined NLC_HUB (set "HUB=%NLC_HUB%") else (set "HUB=%USERPROFILE%\.local\share\nlc\hub")
if not exist "%HUB%\tools\nlc.py" (
  echo NLC:NOT_MET install hub first or set NLC_HUB
  exit /b 1
)
python "%HUB%\tools\nlc.py" --project "%ROOT%" %*
