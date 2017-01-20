CFLAGS := -w


all:
	gcc $(CFLAGS) -o basic basic.c

host:
	socat TCP4-LISTEN:4000,fork,reuseaddr exec:./basic &

clean:
	rm -f basic
