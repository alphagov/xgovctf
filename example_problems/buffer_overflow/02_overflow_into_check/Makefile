CFLAGS := -w

basic:
	gcc $(CFLAGS) -o basic basic.c

host:
	socat TCP4-LISTEN:4002,fork,reuseaddr exec:./basic &

install:
	cp basic static/

clean:
	rm -f basic
