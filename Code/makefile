# target: dependencies... se target è stato fatto dopo l'ultima modifica di dependencies non lo rifa.
compile:
	gcc RRGQuenching.c -o cool.exe
	echo "Program compiled in cool"

run:
	make compile
	Ann 100 0. 0.5 30 0.8
	gnuplot -e "p 'McStories.txt' u 1:2:4 palette" -persist
	pause

run2:
	make compile
	Ann 200 0. 0.5 30 0.8
	gnuplot -e "p 'McStories.txt' u 1:2:4 palette" -persist
	pause

clean: 
	del cool.exe
	pause