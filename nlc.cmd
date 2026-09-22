@echo off
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
if defined NLC_HUB (set "HUB=%NLC_HUB%") else (set "HUB=%USERPROFILE%\.local\share\nlc\hub")
python "%HUB%\tools\nlc.py" --project "%ROOT%" %*
