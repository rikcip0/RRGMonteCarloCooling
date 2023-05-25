@echo off
setlocal

set program=%1
set N=%2
set Tp=%3
set T=%4
set nSamples=%5
set h=%6
set deltaT=%7
set nanneal=%8

set "max_processes=10"       &:: maximum number of processes to run together   
set "delay=2"       &::at least 2 to avoid that two simulations have the same seed

set "counter=0"
set "completed_processes=0"

:loop
if %counter% equ %nSamples% (
    goto check_completion
)

tasklist /FI "IMAGENAME eq %program%" 2>NUL | find /c /i "%program%" > temp.txt
set /p "active_processes=" < temp.txt
del temp.txt

if %active_processes% lss %max_processes% (
    if "%program%"=="singleQuench.exe" (
    start /B "" "%program%" %N% %Tp% %T% %counter% %h%
    set /a "counter+=1"
    echo Started process %counter%
    ) else if "%program%"=="singleAnneal.exe" (
    start /B "" "%program%" %N% %Tp% %T% %counter% %h% %deltaT% %nanneal%
    set /a "counter+=1"
    echo Started process %counter%
    echo .
    ) 
)

ping -n %delay% 127.0.0.1 >NUL
goto loop

:check_completion
tasklist /FI "IMAGENAME eq %program%" 2>NUL | find /c /i "%program%" > temp.txt
set /p "active_processes=" < temp.txt
del temp.txt

if %active_processes% equ 0 (
    goto end
)

ping -n %delay% 127.0.0.1 >NUL
goto check_completion

:end
echo All processes have completed.

endlocal