# target: dependencies... se target è stato fatto dopo l'ultima modifica di dependencies non lo rifa.
compileMultiple:
	gcc RRGQuenching.c -o multipleCool.exe
	@echo Program compiled in multipleCool
	@echo .

compileSingle:
	gcc -DSINGLESTORY RRGQuenching.c -o singleCool.exe
	@echo Program compiled in singleCool
	@echo .

cleanAll: 
	del singleCool.exe
	del multipleCool.exe
	@echo singleCool executable deleted
	@echo multipleCool executable deleted

cleanSingle: 
	del singleCool.exe
	@echo singleCool executable deleted

cleanMultiple: 
	del multipleCool.exe
	@echo multipleCool executable deleted