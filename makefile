
FIR_test: FIR_test.c
	gcc FIR_test.c -o FIR_test

c_ints: c_ints.c
	gcc c_ints.c -o c_ints

IIR_test: IIR_test.c
	gcc IIR_test.c -o IIR_test

local_IIR_test: local_IIR_test.c
	gcc local_IIR_test.c -o local_IIR_test


clean:
	rm FIR_test c_ints IIR_test
