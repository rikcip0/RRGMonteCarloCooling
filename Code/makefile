# target: dependencies... se target è stato fatto dopo l'ultima modifica di dependencies non lo rifa.
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