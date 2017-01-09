Buffer Overflow examples.

We'll be running the examples in here on the server.

The users can connect to the binary on a defined socket, which will be covered in the problem description.  The user can then provide the input, and if they get it correct, the system will echo the flag.

Each binary will provide the source code to the users, so we'll try a variety of buffer overflow examples to see how far people get.

Running the binaries.

Be in the director for the binary, and run
socat TCP4-LISTEN:4000,fork,reuseaddr exec:./binary
where 4000 represnts the port to listen on, and ./binary represents the binary

Best of luck
