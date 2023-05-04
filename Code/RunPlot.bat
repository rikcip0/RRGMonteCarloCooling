@echo off

set N=%1
set Tp=%2
set T=%3
set nSample=%4
set h=%5

make compile

cool %N% %Tp% %T% %nSample% %h%

PlotEnergy.py %N% %Tp% %T% %nSample% %h% 10000
PlotMag.py

..\Utilities\SendResults.py

pause