import os
import random

f = None
debug = True
#debug = False

# Max mesasge length is 64K
MAX_MSG_LEN = 65535
# Maximum Transmission Unit (max size of payload in one fragment)
MTU = 1500 

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
    global local
    local = []
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
        data['FragArray'] = []

        # Code to select fragment number in random (not in order) - but still assuming all fragments
        # except the last one is of 1500 bytes. 
        global local
        NumOfFrags = int(int(data['MsgLen']) / MTU + 1)

        # Create an array with all frag numbers
        local = [x for x in range(0, NumOfFrags)]

        # Select a frag number randomly from the array
        r = random.choice(local)
        data['FragNumber'] = r

        # This frag number is used; so remove it from the array
        local.remove(r)




    def FRAGMENT(self, data):
        # Start creating fragments. Each fragment is 1500 bytes, except the last one. 
        data['FragmentSize'] = min(int(data['BytesLeft']), 1500) 

        # Calculate how many bytes are left in the message.
        data['BytesLeft'] = int(data['BytesLeft']) - int(data['FragmentSize'])

        # Write the current fragment datails to the output file
        dbg_write(f, "", "FRAGMENT {}. FragmentSize={} BytesLeft={}  \n".format(data['FragNumber'], data['FragmentSize'], data['BytesLeft']))


    def END(self, data):
        pass

    # Edges
    def FRAG_START(self, data):
        dbg_write(f, "FRAG_START, ", "MsgLen={}    BytesLeft={}\n".format(data['MsgLen'], data['BytesLeft']))

    def FRAG_AGAIN(self, data):
        # Select the next frag number, randomly. Remove the selected number from the array.
        r = random.choice(local)
        local.remove(r)
        data['FragNumber'] = r

    def FRAG_END(self, data):
        dbg_write(f, "FRAG_END ", "")

    def NEW_MSG(self, data):
        pass
