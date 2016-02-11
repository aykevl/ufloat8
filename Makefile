
# disable implicit rules
.SUFFIXES:

test: test-python test-c

test-python:
	python3 ./ufloat8.py

test-c:
	gcc --std=c11 -Wall -Werror -o ./test test.c ufloat8.c && ./test
