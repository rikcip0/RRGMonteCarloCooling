@echo off
setlocal enabledelayedexpansion

set "folder=C:\percorso\alla\cartella"
cd /d "%folder%"

for %%F in (*_*.*) do (
    set "filename=%%~nF"
    set "extension=%%~xF"
    
    for /f "tokens=1* delims=_" %%A in ("!filename!") do (
        set "newname=%%A!extension!"
        ren "%%F" "!newname!"
    )
)

echo File rinominati con successo.
