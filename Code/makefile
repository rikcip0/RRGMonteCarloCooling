# target: dependencies... se target è stato fatto dopo l'ultima modifica di dependencies non lo rifa.
.PHONY: help

help:
	@echo List of possible targets:
	@echo   archiveRun - Move run data, info and plots from ThisRun to Archive
	@echo   send - Send an email to RC with plots and results from ThisRun

compileMultipleQuench:
	gcc RRGQuenching.c -o multipleQuench.exe
	@echo Program compiled in multipleQuench
	@echo .

compileSingleQuench:
	gcc -DSINGLESTORY RRGQuenching.c -o singleQuench.exe
	@echo Program compiled in singleQuench
	@echo .


compileMultipleAnneal:
	gcc -DANNEAL RRGQuenching.c -o multipleAnneal.exe
	@echo Program compiled in multipleAnneal
	@echo .

compileSingleAnneal:
	gcc -DANNEAL -DSINGLESTORY RRGQuenching.c -o singleAnneal.exe
	@echo Program compiled in singleAnneal
	@echo .

archiveRun:
	python ..\Utilities\MoveRunToArchive.py

send:
	python ..\Utilities\SendResults.py

cleanAll: 
	del singleQuench.exe
	del multipleQuench.exe
	del singleAnneal.exe
	del multipleAnneal.exe
	@echo singleCool executables deleted
	@echo multipleCool executables deleted

cleanSingle: 
	del singleCool.exe
	@echo singleCool executable deleted

cleanMultiple: 
	del multipleCool.exe
	@echo multipleCool executable deleted