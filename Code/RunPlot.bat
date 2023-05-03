@echo off

set N=%1
set Tp=%2
set T=%3
set nSample=%4
set h=%5

make compile

cool %N% %Tp% %T% %nSample% %h%

start PlotEnergy.py %N%
start PlotMag.py %N%

..\Utilities\SendResults.py

pause