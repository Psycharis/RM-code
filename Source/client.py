import socket, pickle
import random

from sage.all import *
#from sage.coding.reed_muller_code import BinaryReedMullerCode
#from sage.coding.reed_muller_code import ReedMullerVectorEncoder

try:
    HOST = 'localhost'    # The remote host
    PORT = 50327              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT)) # socket connection with server.py
except:
    sys.exit("\nConnection refused, server is not running :/")

if __name__ == "__main__":

# ============== First Message START ==============
    print "\n==============================="
    print "========= Reed Muller ========="
    print "======= Code simulator ========"
    print "============ v0.1 === client =="
    print "===============================\n"
# =============== First Message END ===============


    try:
# ============== User Input-1 START ==============
        while True:

            r = raw_input("Give reed-muller's order: ")
            m = raw_input("Give reed-muller's code length: ")

            if(r is not '' and m is not '' and r.isdigit() and m.isdigit()):

                if (m >= r and m >= 0 and r >= 0):
                    r = int(r)
                    m = int(m)
                    break
                else:
                    print "Your input is invalid!"

            else:
                print "Your input is invalid!"
# =============== User Input-1 END ===============


# ============== Check for dual-code START ==============
        if((m-r-1) >= 0 and (m-r-1) <= m):
            r = m-r-1
            print
            print "** switching to dual reed-muller code"
            print
# =============== Check for dual-code END ===============


# ========== Reed Muller code intitialization START ==========
        RM = codes.BinaryReedMullerCode(r, m) # initialize reed-muller code
# =========== Reed Muller code intitialization END ===========

        max = RM.minimum_distance() / 2 # max weight error

# ============== User Input-2 START ==============
        while True:

            errw = raw_input("Give error weight less or equal than " + str(max) + ": ")
            words = raw_input("Give number of words to make " + str(errw) + " errors : ")

            if(errw is not '' and errw.isdigit() and words is not '' and words.isdigit()):
                errw = int(errw)
                words = int(words)
                if(errw >= 0 and errw <= max and words >= 0 and words <= 20):
                    break
                else:
                    print "Your input is invalid!"
            else:
                print "Your input is invalid!"
# =============== User Input-2 END ===============


        ENCODER = codes.encoders.ReedMullerVectorEncoder(RM) # initialize vector encoder

        print
        print "** minimum distance: " + str(RM.minimum_distance())
        print "** number of variables: " + str(RM.number_of_variables())
        print

        w2s = [] # w2s = words to send
        encoded_w2s = [] # encoded words to send

# ============== create 20 random words START ==============
        for i in range(0, 20):
            pre_vector_array = [] # initialize empty array

            for i in range(0, RM.dimension()):
                pre_vector_array.append(randrange(0,2)) # create random bits in single array

            w2s.append(vector(pre_vector_array)) # append array as vector in w2s
            print vector(pre_vector_array)
# =============== create 20 random words END ===============


# ============== Encode START ==============
        for i in range(0, 22):
            if i < 20:
                E = ENCODER.encode(w2s[i])
            elif i == 20:
                E = r
            else:
                E = m
            encoded_w2s.append(E)
# =============== Encode END ===============


# ============== Errors in words START ==============
        randomWords = []
        Chan = channels.StaticErrorRateChannel(RM.ambient_space(), errw) # channel for simulate errors in transmition

        randomWords = sample(range(20), words) # create list of random words that will get the errors

        while words > 0:
            encoded_w2s[randomWords[words - 1]] = Chan(encoded_w2s[randomWords[words - 1]]) # add errors in words
            words -= 1
# =============== Errors in words END ===============


# ============== Data ser & send START ==============
        data_string = pickle.dumps(encoded_w2s) # data serialization

        s.send(data_string)

        s.close()
# =============== Data ser & send END ===============

        print 'Message has been sent successfully' # Last print of client
    except:
        sys.exit("\nScript stopped responding, something gone wrong :/")
