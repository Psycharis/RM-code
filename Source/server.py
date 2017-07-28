import socket

import pickle
from sage.all import *
#from sage.coding.reed_muller_code import BinaryReedMullerCode
#from sage.coding.reed_muller_code import ReedMullerVectorEncoder
#from sage.coding.linear_code import LinearCodeSyndromeDecoder

try:
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50327              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept() # connection with client.py
except:
    sys.exit("\nServer stop unexpectedly :/")

# ============== First Message START ==============
print "\n==============================="
print "========= Reed Muller ========="
print "======= Code simulator ========"
print "============ v0.1 === server =="
print "===============================\n"
# =============== First Message END ===============

try:
    # =============== Receive START ===============
    while 1:
        recvd_data = conn.recv(32768)
        if not recvd_data: break

        data = pickle.loads(recvd_data) # data de-serialization

        conn.sendall(recvd_data)
    # =============== Receive END ===============


    # ========== Reed Muller code intitialization START ==========
    r = data[20] # 'r' order value
    m = data[21] # 'm' code lenght value

    RM = codes.BinaryReedMullerCode(r, m) # initialize reed-muller code
    # =========== Reed Muller code intitialization END ===========


    max_errors = min(RM.decoder().decoding_radius(), RM.minimum_distance()/2) - 1 # max error weight that decoder can fix

    if max_errors < 0:
        max_errors = 0

    dec = RM.decoder('Syndrome', maximum_error_weight = max_errors) # initialize decoder

    unencode_w2s = []

    coErrors = 0 # correct words received
    reErrors = 0 # Repaired income words
    unErrors = 0 # Unsuccessful repaired income words:


    # =============== decode START ===============
    for i in range(0, 20):
        if not data[i] in RM:
            reErrors += 1
        try:
            E2 = dec.decode_to_message(data[i]) # decode the encoded message
        except:
            print "The word is not understandable due to errors"
            unErrors += 1
            continue

        unencode_w2s.append(E2)
        print str(E2)
    # ================ decode END ================


    coErrors = 20 - unErrors
    reErrors = reErrors - unErrors
    coErrors = coErrors - reErrors

    print "Correct income words: " + str(coErrors) + " words"
    print "Repaired income words: " + str(reErrors) + " words"
    print "Unsuccessful repaired income words: " + str(unErrors) + " words" # Last print of server

    conn.close()
except:
    sys.exit("\nConnection with client stop unexpectedly :/")
