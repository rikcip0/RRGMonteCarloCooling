@echo off
setlocal

set simType=%1
set N=%2
set Tp=%3
set T=%4
set nSample=%5
set h=%6
set deltaT=%7
set nanneal=%8

if "%simType%"=="quench" (
    set program=singleQuench.exe
    make compileSingleQuench
) else if "%simType%"=="anneal" (
    set program=singleAnneal.exe
    make compileSingleAnneal
) else (
    echo The first parameter is the simulation type. It can be "quench" or "anneal".
    goto end
)

echo Simulations will be launched using the executable %program%.

set "McStoriesPath=..\Data\ThisRun\McStories"

if not exist "%McStoriesPath%" (
    echo La cartella non esiste. La sto creando...
    mkdir "%McStoriesPath%"
    if errorlevel 1 (
        echo Errore durante la creazione della cartella.
    ) else (
        echo Cartella creata con successo.
    )
) else (
    echo La cartella esiste già.
)

WriteInfo.py Simulation %nSample%

echo %program% %N% %Tp% %T% %nSample% %h% %deltaT% %nanneal%
call Launcher %program% %N% %Tp% %T% %nSample% %h% %deltaT% %nanneal%

WriteInfo.py Analysis %nSample%
Analysis.py
..\Utilities\SendResults.py

:end

pause