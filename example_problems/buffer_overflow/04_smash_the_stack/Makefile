CFLAGS := -w -g -fno-stack-protector -z execstack


all:
	gcc $(CFLAGS) -o basic basic.c

host:
	socat TCP4-LISTEN:4003,fork,reuseaddr exec:./basic &

clean:
	rm -f basic
