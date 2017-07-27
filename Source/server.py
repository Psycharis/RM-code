# Echo server program
import socket

import pickle
from sage.all import *
from sage.coding.reed_muller_code import BinaryReedMullerCode
from sage.coding.reed_muller_code import ReedMullerVectorEncoder
from sage.coding.linear_code import LinearCodeSyndromeDecoder

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50217              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Message by', addr

while 1:
    recvd_data = conn.recv(32768)
    if not recvd_data: break

    data = pickle.loads(recvd_data)

    conn.sendall(recvd_data)

r = data[20] # 'r' order value
m = data[21] # 'm' code lenght value

RM = codes.BinaryReedMullerCode(r, m) # initialize reed-muller code

max_errors = min(RM.decoder().decoding_radius(), RM.minimum_distance()/2) - 1

if max_errors < 0:
    max_errors = 0

dec = RM.decoder('Syndrome', maximum_error_weight = max_errors)

unencode_w2s = []

for i in range(0, 20):

    try:
        E2 = dec.decode_to_message(data[i]) # decode the encoded message
    except:
        print "The word is not understandable due to errors"
        continue

    unencode_w2s.append(E2)
    print str(E2)


conn.close()
