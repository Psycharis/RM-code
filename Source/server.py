# Echo server program
import socket

import pickle
from sage.all import *
from sage.coding.reed_muller_code import BinaryReedMullerCode
from sage.coding.reed_muller_code import ReedMullerVectorEncoder
from sage.coding.linear_code import LinearCodeSyndromeDecoder

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50017              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

while 1:
    recvd_data = conn.recv(8192)
    if not recvd_data: break

    data = pickle.loads(recvd_data)

    conn.sendall(recvd_data)

r = data[20]
m = data[21]

RM = codes.BinaryReedMullerCode(r, m) # initialize reed-muller code
ENCODER = codes.encoders.ReedMullerVectorEncoder(RM) # initialize vector encoder
err = codes.decoders.LinearCodeNearestNeighborDecoder(RM)
D = RM.decoder()

try:
    vector = RM.syndrome(data[0])
    print str()
    flag = true
    check = 0
    for i in range(0, 20):
        word = RM.syndrome(data[i])
        for y in range(0, len(vector)):
            if word[y] == 1:
                check += 1
        if check > 1:
            flag = false
            check = 0

    unencode_w2s = []

    print
    if flag:
        for i in range(0, 20):
            data[i] = err.decode_to_message(data[i])
            E2 = data[i]
            unencode_w2s.append(E2)
            print str(unencode_w2s[i])
    else:
            print "The code is not understandable due to errors"
except:
    print "The code is not understandable due to errors"

conn.close()