from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
import sys, time, getopt

def send_print(apdu):
    response, sw1, sw2 = cardservice.connection.transmit(apdu)

    #command was successful
    if [sw1, sw2] == [0x90, 0x00]:
        print("Tag | " + toHexString(response) + "\n")
    else:
        print('Error: {}, sending APDU: {}'.format(toHexString([sw1,sw2]), toHexString(apdu)))
        print('Response', toHexString(response))
        
        if (toHexString([sw1,sw2]) == "69 88"):
            print("Incorrect secure messaging data objects")
        elif (toHexString([sw1,sw2]) == "69 82"):
            print("Security status not satisfied")
        sys.exit()

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=5, cardType=cardtype )
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()

cmd = 1
if cmd == 1:
    # Get memory dump
    for l in range(1,7):
        print("Get recordings")
        send_print(toBytes("00 f{} 04 00 00".format(l)))
elif cmd == 2:
    print("Clear memory")
    send_print(toBytes("00 fe 04 00 00"))