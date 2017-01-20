CFLAGS := -w

basic:
	gcc $(CFLAGS) -o basic basic.c

host:
	socat TCP4-LISTEN:4001,fork,reuseaddr exec:./basic &

clean:
	rm -f basic
