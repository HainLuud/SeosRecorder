from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
import sys

def send_print(comment, apdu):
  print(comment)
  print("Rdr |", toHexString(apdu))
  response, sw1, sw2 = cardservice.connection.transmit(apdu)

  #command was successful
  if [sw1, sw2] == [0x90, 0x00]:
    print("Tag | " + toHexString(response) + "\n")
  else:
    print('Error: {}'.format(toHexString([sw1,sw2])))
    print('Response', response)
    
    if (toHexString([sw1,sw2]) == "69 88"):
      print("Incorrect secure messaging data objects")
    elif (toHexString([sw1,sw2]) == "69 82"):
      print("Security status not satisfied")
    sys.exit()

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=5, cardType=cardtype )
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()


#get UID
#send_print("Card UID: ", [0xFF, 0xCA, 0x00, 0x00, 0x00])
#get ATR
#ATR = cardservice.connection.getATR()
#print("ATR: {}\n".format(toHexString(ATR)))

# Return FCI (file control information) template, optional use of FCI tag and length
send_print("SELECT by DF_name (command always the same)", toBytes("00 a4 04 00 0a a0 00 00 04 40 00 01 01 00 01 00")) # this command is constant

send_print("HID Seos proprietary command (command always the same, response always* different)", toBytes("80 a5 04 00 2a 06 12 2b 06 01 04 01 81 e4 38 01 01 02 01 18 01 01 91 75 05 06 14 2b 06 01 04 01 81 e4 38 01 01 02 01 18 01 01 81 23 91 26 01 00"))

send_print("Start General authentication (EXTERNAL AUTHENTICATE - an entity in the card authenticates an entity in the outside world) \n(command always the same, response always* different)", toBytes("00 87 00 01 04 7c 02 81 00"))

send_print("Continue General authentication (Response from the outside world and verification by the card) (command always* different, response always* different)", toBytes("00 87 00 01 2c 7c 2a 82 28 0e 0e 01 fa 44 16 73 23 84 0f 09 8a d5 19 36 08 cb 56 6b 61 8c f8 e3 d2 f3 dd 49 3a ed ae c1 88 b7 5d b4 40 17 c2 26 4b 00"))

send_print("GET DATA command (asks the card to send the content of an EF over SM) \n(command always* different, response is always* different)", toBytes("0c cb 3f ff 16 85 08 28 58 cc f3 8a 69 30 70 97 00 8e 08 7b 19 c8 b4 74 4a 61 65 00"))

send_print("", toBytes("ca 00 7a 29"))                      
