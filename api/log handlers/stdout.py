__author__ = 'collinpetty'

import zmq
context = zmq.Context()
sub = context.socket(zmq.SUB)
print("Connecting...")
sub.connect("tcp://127.0.0.1:7979")
sub.setsockopt_string(zmq.SUBSCRIBE, "pico", encoding='utf-8')

print("Running...")
while True:
    topic, message = sub.recv_multipart()
    print("%s - %s" % (topic, message))