import smartcard
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
import sys, getopt

INS_meanings = {0x04:"Deativate file", 0x0C:"Erase record(s)", 0x0E:"Erase binary", 0x0F:"Erase binary", 0x10:"Perform SCQL operation",
    0x12:"Perform transaction operation", 0x14:"Perform user operation", 0x20:"Verify", 0x21:"Verify", 0x22:"Manage security environment",
    0x24:"Change reference data", 0x26:"Disable verification requirement", 0x28:"Wnambe verification requirement", 
    0x2A:"Perform security operation", 0x2C:"Reset retry counter", 0x44:"Activate file", 0x46:"Generate asymetric key-pair", 
    0x70:"Manage channel", 0x82:"External (/mutual) authenticate", 0x84:"Get challenge", 0x86:"General authenticate", 0x87:"General authenticate",
    0x88:"Internal authenticate", 0xA0:"Search binary", 0xA1:"Search binary", 0xA2:"Search record", 0xA4:"Select", 0xB0:"Read binary",
    0xB1:"Read binary", 0xB2:"Read record(s)", 0xB3:"Read record(s)", 0xC0:"Get response", 0xC2:"Envelope", 0xC3:"Envelope", 0xCA:"Get data",
    0xCB:"Get data", 0xD0:"Write binary", 0xD1:"Write binary", 0xD2:"Write record", 0xD6:"Update binary", 0xD7:"Update binary",
    0xDA:"Put data", 0xDB:"Put data", 0xDC:"Update record", 0xDD:"Update record", 0xE0:"Create file", 0xE2:"Append record", 0xE4:"Delete file",
    0xE6:"Terminate DF", 0xE8:"Terminate EF", 0xFE:"Terminate card usage"}

flags = []
def send(apdu, arrayNr=0) -> [int]:
    response, sw1, sw2 = cardservice.connection.transmit(apdu)

    #command was successful
    if [sw1, sw2] == [0x90, 0x00]:
        if response == []: sys.exit("Done")
        if "verbose" in flags:
            print("Memory array", arrayNr)
            print("Tag | " + toHexString(response) + "\n")
    else:
        print('Error: {}, sending APDU: {}'.format(toHexString([sw1,sw2]), toHexString(apdu)))
        print('Response', toHexString(response))
        
        if (toHexString([sw1,sw2]) == "69 88"):
            print("Incorrect secure messaging data objects")
        elif (toHexString([sw1,sw2]) == "69 82"):
            print("Security status not satisfied")
        sys.exit()
    return response

def bitvector(n) -> [bool]:
    return [int(digit) for digit in bin(n)[2:]] 

def printVerbose(CLA, INS, P1, P2, Lc, Data, Le) -> None:
    # Print what is means
    CLA_message = [ "The command is the last or only command of a chain.", 
                    "No Secure Messaging or no indication.", 
                    "Logical channel number 0."]
    CLA_bv = bitvector(CLA)
    if CLA_bv[4]: CLA_message[0] = "The command is not the last command of a chain."
    if CLA_bv[2:4] == [0,1]: CLA_message[1] = "Proprietary Secure Messaging format."
    elif CLA_bv[2:4] == [1,0]: CLA_message[1] = "Secure Messaging according to Chapter 6 of ISO/IEC 7816-4, command header not processed according to 6.2.3.1"
    elif CLA_bv[2:4] == [1,0]: CLA_message[1] = "Secure Messaging according to Chapter 6 of ISO/IEC 7816-4, command header authenticated according to 6.2.3.1"
    if CLA_bv[0:2] == [0,1]: CLA_message[2] = "Logical channel number 1."
    elif CLA_bv[0:2] == [1,0]: CLA_message[2] = "Logical channel number 2."
    elif CLA_bv[0:2] == [1,1]: CLA_message[2] = "Logical channel number 3."

    if INS in INS_meanings:
        INS_message = INS_meanings[INS]
    else:
        INS_message = "Proprietary instruction"

    P1P2_message = ""
    if INS == 0xA4:
        P1P2_message = ""
    pass

def processDump(memoryArrays) -> None:
    #print(toHexString(memoryArrays[0]))
    """
        APDU structure:
        CLA (1 byte)        Instruction class - indicates the type of command, e.g. interindustry or proprietary 
        INS (1 byte)        Instruction code - indicates the specific command, e.g. "write data" 
        P1-P2 (2 bytes)     Instruction parameters for the command, e.g. offset into file at which to write the data 
        Lc (0,1 or 3 byte)  Length contained in Data 
        Data (x bytes)  
        Le (0-3 bytes)      Length of expected response
    """
    cmdCounter = 1
    memArray = 0
    memPointer = 0
    
    while memArray < len(memoryArrays):
        # Select memory array
        memory = memoryArrays[memArray]
        if memory == [0] * 256: break

        # Discern APDU
        CLA, INS, P1, P2 = memory[memPointer: memPointer + 4]
        memPointer += 4
        
        if [CLA,INS,P1,P2] == [0xca, 0x00, 0x7a, 0x29]:
            Lc = []
            DATA = []
            Le = []
        elif [CLA,INS,P1,P2] == [0x00, 0xCA, 0x7F, 0x68]:
            print("APDU {} \n\tUnknown APDU  00 CA 7F 68 00 00".format(cmdCounter))
            cmdCounter += 1
            memPointer += 5
            continue
        else:
            # Discounting the possibility that Lc is absent
            if memory[memPointer] != 0:
                Lc = [memory[memPointer]]
                memPointer += 1
            else:
                Lc = [memory[memPointer: memPointer + 3]]
                memPointer += 3
            #print("asd",Lc)
            DATA = memory[memPointer: memPointer + int.from_bytes(Lc, byteorder='big', signed=False)]
            memPointer += int.from_bytes(Lc, byteorder='big', signed=False)

            if memory[memPointer: memPointer + 3] == [255,255,255]:
                Le = []
            else: 
                Le = memory[memPointer:memPointer + len(Lc)]#5C 03 5F C1 0C
                if type(Le) is not list:Le = [Le]
            memPointer += len(Le)
        
        # Print APDU byte values
        if "verbose" not in flags:
            print("""APDU {}\n\tCLA: {}\n\tINS: {}\n\tP1-P2: {}\n\tLc: {}\n\tData: {}\n\tLe: {}\n""".format(
                cmdCounter, toHexString([CLA]), toHexString([INS]), toHexString([P1, P2]), toHexString(Lc), 
                toHexString(DATA), toHexString(Le)))
        else:
            printVerbose(CLA, INS, P1, P2, Lc, DATA, Le)
        
        if memory[memPointer:memPointer + 3] == [255,255,255]:
            cmdCounter += 1
            # If the end of the memory array is inly 0x00 values
            if memory[memPointer + 3:] == len(memory[memPointer + 3:]) * [0]:
                memArray += 1
                memPointer = 0
            else:
                memPointer += 3
        else:
            print("Failed processing the recordings.")
            print("Memory arrays:",memoryArrays)
            print("MemPointer", memPointer)
            exit()
        

def usage() -> None:
    print("usage: python recieve_recordings.py OPTION")
    print("The messaging printed by this script is simplified. If full description of command meanings is wanted, " +
            "then consulting the ISO/IEC 7816-4 standard is necessary.")
    print("OPTIONS:")
    print("   -w \t wipe Java card's memory")
    print("   -r \t retrieve card's recordings")
    #print("   -v \t verbose output")
    print('   -h \t this menu')

def arg_process(argv) -> None:
    if (argv == []): 
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv,"hwrv")
    except getopt.GetoptError:
        usage()
        sys.exit()
    
    for opt, arg in opts:
        if opt == '-w':
            flags.append("wipe")
        elif opt == '-r':
            flags.append("return")
        #elif opt == "-v":
        #    flags.append("verbose")
        else:
            usage()
            sys.exit()

if __name__ == "__main__":
    arg_process(sys.argv[1:])

    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=5, cardType=cardtype )
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect()

    if "return" in flags:
        print("Getting recordings")
        cardsMemory = []
        for l in range(1,7):
            cardsMemory.append(send(toBytes("00 f{} 04 00 00".format(l)), l))
        processDump(cardsMemory)
    
    if "wipe" in flags:
        print("Clearing memory")
        send(toBytes("00 fe 04 00 00"))
    