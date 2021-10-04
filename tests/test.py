import os
import random

f = None
debug = True
#debug = False

# Max mesasge length is 64K
MAX_MSG_LEN = 65535

def dbg_write(file, always_print, dbg_print):
    if debug:
        str_to_write = always_print + dbg_print
    else:
        str_to_write = always_print 

    file.write(str_to_write)


def setUpRun():
    """Will be executed first, before anything else."""
    print("In setup!...")
    global f
    # Output file for fragmentation details 
    f = open("fragments.txt","w")

def tearDownRun():
    """Will be executed last."""
    print("In teardown!...")
    f.close()


class Fragment_factory:

    #Vertices
    def START(self, data):
        # Message size is chosen at random, between 1501 and 64k bytes
        # For simplicity, this model does NOT create messages that do not need fragmentation. 
        data['MsgLen'] = max(1501, round(random.random() * MAX_MSG_LEN))
        data['BytesLeft'] = int(data['MsgLen']) 
        dbg_write(f, "\nNew Message: ", "MsgLen = {} \n".format(data['MsgLen']))
        data['FragNumber'] = 0


    def FRAGMENT(self, data):
        # Start creating fragments. Each fragment is 1500 bytes, except the last one. 
        data['FragmentSize'] = min(int(data['BytesLeft']), 1500) 

        # It is possible to have fragments of less than 1500 bytes. This can be simulated by using the 
        # following line instead of the one above, which sets all (except the last one) fragments to 1500 bytes. 
        # data['FragmentSize'] = min(round(random.random() * int(data['BytesLeft'])), 1500) 

        # Calculaet how many bytes are left in the message.
        data['BytesLeft'] = int(data['BytesLeft']) - int(data['FragmentSize'])

        # Write the current fragment datails to the output file
        dbg_write(f, "", "FRAGMENT {}. FragmentSize={} BytesLeft={}  \n".format(data['FragNumber'], data['FragmentSize'], data['BytesLeft']))


    def END(self, data):
        pass

    # Edges
    def FRAG_START(self, data):
        dbg_write(f, "FRAG_START, ", "MsgLen={}    BytesLeft={}\n".format(data['MsgLen'], data['BytesLeft']))

    def FRAG_AGAIN(self, data):
        data['FragNumber'] = int(data['FragNumber']) + 1

    def FRAG_END(self, data):
        dbg_write(f, "FRAG_END ", "")

    def NEW_MSG(self, data):
        pass
