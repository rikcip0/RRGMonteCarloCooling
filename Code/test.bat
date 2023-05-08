@echo off
setlocal

set program="singleCool.exe"
set N=%1
set Tp=%2
set T=%3
set nSamples=%4
set h=%5

set "max_processes=10"       &:: maximum number of processes to run together   
set "delay=2"       &::at least 2 to avoid that two simulations have the same seed

set "counter=0"
set "completed_processes=0"

:loop
if %counter% equ %nSamples% (
    goto check_completion
)

tasklist /FI "IMAGENAME eq singleCool.exe" 2>NUL | find /c /i "singleCool.exe" > temp.txt
set /p "active_processes=" < temp.txt
del temp.txt

if %active_processes% lss %max_processes% (
    start /B "" "%program%" %N% %Tp% %T% %counter% %h%
    set /a "counter+=1"
    echo Started process %counter%
)

ping -n %delay% 127.0.0.1 >NUL
goto loop

:check_completion
tasklist /FI "IMAGENAME eq singleCool.exe" 2>NUL | find /c /i "singleCool.exe" > temp.txt
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