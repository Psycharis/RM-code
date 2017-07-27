import socket, pickle
from random import randint

from sage.all import *
from sage.coding.reed_muller_code import BinaryReedMullerCode
from sage.coding.reed_muller_code import ReedMullerVectorEncoder

HOST = 'localhost'    # The remote host
PORT = 50217              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if __name__ == "__main__":

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

    if((m-r-1) >= 0 and (m-r-1) <= m):
        r = m-r-1
        print "** switching to dual reed-muller code"

    RM = codes.BinaryReedMullerCode(r, m) # initialize reed-muller code
    max = RM.minimum_distance() / 2

    while True:

        errw = raw_input("Give error weight less or equal than " + str(max) + ": ")

        if(errw is not '' and errw.isdigit()):
            errw = int(errw)
            if(errw >= 0 and errw <= max):
                break
            else:
                print "Your input is invalid!"
        else:
            print "Your input is invalid!"

    ENCODER = codes.encoders.ReedMullerVectorEncoder(RM) # initialize vector encoder

    print "** minimum distance: " + str(RM.minimum_distance())
    print "** number of variables: " + str(RM.number_of_variables())

    w2s = [] # w2s = words to send
    encoded_w2s = [] # encoded words to send

    # create 20 random words
    for i in range(0, 20):
        pre_vector_array = [] # initialize empty array

        for i in range(0, RM.dimension()):
            pre_vector_array.append(randrange(0,2)) # create random bits in single array

        w2s.append(vector(pre_vector_array)) # append array as vector in w2s
        print vector(pre_vector_array)

    for i in range(0, 22):
        if i < 20:
            E = ENCODER.encode(w2s[i])
        elif i == 20:
            E = r
        else:
            E = m
        encoded_w2s.append(E)


    Chan = channels.StaticErrorRateChannel(RM.ambient_space(), errw) # add errors
    random = randint(0, 19) # random number 0-20

    encoded_w2s[random] = Chan(encoded_w2s[random])

    data_string = pickle.dumps(encoded_w2s)

    s.send(data_string)

    s.close()
    print 'Message has been sent successfully'
