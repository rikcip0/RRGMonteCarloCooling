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

echo %program% %N% %Tp% %T% %nSample% %h% %deltaT% %nanneal%
call Launcher %program% %N% %Tp% %T% %nSample% %h% %deltaT% %nanneal%

..\Utilities\SendResults.py

:end

pause