
all: make host install

make:
	cd 01_length_check; make;
	cd 02_overflow_into_check; make;
	cd 02_static_password; make;
	cd 03_overflow_null; make;
	cd 04_smash_the_stack; make;

host:
	cd 01_length_check; make host;
	cd 02_overflow_into_check; make host;
	cd 02_static_password; make host;
	cd 03_overflow_null; make host;
	cd 04_smash_the_stack; make host;

install:
	cd 01_length_check; make install;
	cd 02_overflow_into_check; make install;
	cd 02_static_password; make install;
	cd 03_overflow_null; make install;
	cd 04_smash_the_stack; make install;

clean:
	cd 01_length_check; make clean;
	cd 02_overflow_into_check; make clean;
	cd 02_static_password; make clean;
	cd 03_overflow_null; make clean;
	cd 04_smash_the_stack; make clean;
