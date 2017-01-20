CFLAGS := -w -O0


all:
	gcc $(CFLAGS) -o basic basic.c

host:
	socat TCP4-LISTEN:4002,fork,reuseaddr exec:./basic &

clean:
	rm -f basic
