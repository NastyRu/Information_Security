key := -std=c++17 -Wall -Werror

%.o: %.cpp *.h
	g++ $(key) -c $<

install.out: shifr.o mac_adress.o install.o
	g++ $(key) -o $@ $^

main.out: shifr.o mac_adress.o main.o
	g++ $(key) -o $@ $^

clean:
	rm *.o *.out
