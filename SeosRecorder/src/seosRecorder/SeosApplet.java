package seosRecorder;

import javacard.framework.*;

public class SeosApplet extends Applet{
	
	byte[] resp1 = {0x6f, 0x0c, (byte)0x84, 0x0a, 0xa, 0x0, 0x0, 0x04, 0x40, 0x00, 0x01};
	byte[] resp2 = {(byte)0xcd, (byte)0x02, (byte)0x02, (byte)0x06, (byte)0x85, (byte)0x38, (byte)0x27, (byte)0xee, (byte)0x1e, (byte)0x43, (byte)0xa3, (byte)0xb6, (byte)0x16, (byte)0x0a, (byte)0x00, (byte)0xa3, (byte)0x74, (byte)0x1a, (byte)0x08, (byte)0x51, (byte)0xb1, (byte)0xe8, (byte)0x7d, (byte)0xf3, (byte)0x00, (byte)0x10, (byte)0xce, (byte)0x97, (byte)0x95, (byte)0x82, (byte)0x0c, (byte)0xa5, (byte)0x5f, (byte)0x5b, (byte)0x72, (byte)0x31, (byte)0xf0, (byte)0x92, (byte)0x47, (byte)0xe8, (byte)0xbf, (byte)0x32, (byte)0x52, (byte)0xe5, (byte)0x0d, (byte)0x9e, (byte)0x03, (byte)0x29, (byte)0xcf, (byte)0xa2, (byte)0xb0, (byte)0x94, (byte)0x5f, (byte)0x0f, (byte)0x39, (byte)0xb6, (byte)0xd2, (byte)0xab, (byte)0xd8, (byte)0x5e, (byte)0x4e, (byte)0x30, (byte)0x8e, (byte)0x08, (byte)0xf3, (byte)0x12, (byte)0x5b, (byte)0x0e, (byte)0xb8, (byte)0xdd, (byte)0x2c, (byte)0xd8, (byte)0x90, (byte)0x00, (byte)0xf3, (byte)0xce};
	byte[] resp3 = {(byte)0x7c, (byte)0x0a, (byte)0x81, (byte)0x08, (byte)0xf5, (byte)0x48, (byte)0x90, (byte)0x3c, (byte)0xcb, (byte)0x4d, (byte)0xdc, (byte)0x9d, (byte)0x90, (byte)0x00, (byte)0x37, (byte)0x78};
	byte[] resp4 = {(byte)0x7c, (byte)0x2a, (byte)0x82, (byte)0x28, (byte)0x93, (byte)0xa3, (byte)0x1e, (byte)0x29, (byte)0xcb, (byte)0x27, (byte)0x5d, (byte)0xe3, (byte)0xd1, (byte)0x9e, (byte)0xd4, (byte)0xfd, (byte)0x4d, (byte)0x40, (byte)0x14, (byte)0xf6, (byte)0x6e, (byte)0x67, (byte)0x15, (byte)0xe1, (byte)0xc7, (byte)0x33, (byte)0x30, (byte)0x6d, (byte)0x9a, (byte)0xcb, (byte)0x20, (byte)0x7b, (byte)0xeb, (byte)0xbc, (byte)0xf6, (byte)0x06, (byte)0x38, (byte)0x38, (byte)0xc8, (byte)0xe9, (byte)0x32, (byte)0x10, (byte)0xd7, (byte)0xdb, (byte)0x90, (byte)0x00, (byte)0xde, (byte)0xa3};
	byte[] resp5 = {(byte)0x85, (byte)0x40, (byte)0xd4, (byte)0x55, (byte)0x7b, (byte)0xa9, (byte)0x80, (byte)0x81, (byte)0x9b, (byte)0x55, (byte)0xd0, (byte)0x73, (byte)0xd6, (byte)0xf9, (byte)0xae, (byte)0x25, (byte)0x05};
	byte[] resp6 = {(byte)0xca, (byte)0x00, (byte)0x7a, (byte)0x29};
	byte[] cmdEnd = {(byte)0xFF, (byte)0xFF, (byte)0xFF};
	
	// One full dialogue recording is between 156 and 184 bytes
	byte[] memory1 = new byte[256];
	byte[] memory2 = new byte[256];
	byte[] memory3 = new byte[256];
	byte[] memory4 = new byte[256];
	byte[] memory5 = new byte[256];
	byte[] memory6 = new byte[256];
	byte[] destMemory = memory1;
	byte memoryArraySelector = 1;
	short memPointer = 0;
	
	byte[] clearMemory = new byte[256];
	
	public static void install(byte[] ba, short ofs, byte len) {
		(new SeosApplet()).register();
	}
	/* Process logic
	 * The card sends out the anomaly commands as recorded with the proxmark
	 * During process it records APDUs sent to it 
	 */
	public void process(APDU apdu) {
		byte[] buf = apdu.getBuffer(); // contains C-APDU bytes
		
		if ( (short)(255 - memPointer) < (short)(buf[ISO7816.OFFSET_LC] + 8) ) {
			
			switch (memoryArraySelector % 6) {
				case 0: 
					destMemory = memory1;
					memoryArraySelector = 0;
					break;
				case 1: 
					destMemory = memory2;
					break;					
				case 2: 					
					destMemory = memory3;
					break;
				case 3: 
					destMemory = memory4;
					break;
				case 4: 
					destMemory = memory5;
					break;
				case 5: 
					destMemory = memory6;
					break;
			}
			memoryArraySelector += 1;
			memPointer = 0;
		}
		short recievedLen = (short)((buf[ISO7816.OFFSET_LC] + 6) & (short)0xff);
		
		switch (buf[ISO7816.OFFSET_INS]) {
			case (byte)0xa4: // first APDU
				apdu.setIncomingAndReceive(); // read APDU data bytes
				//short len = (short)(buf[ISO7816.OFFSET_CDATA] & (short)0xff); // how much data should be sent back
				
				// Copy received command to memory
				Util.arrayCopy(buf, (short)0, destMemory, memPointer, recievedLen);
				memPointer += recievedLen;
				
				// Set FF FF FF after received command
				Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
				memPointer += 3;
				
				Util.arrayCopy(resp1, (short)0, buf, (short)0, (short)11);
				apdu.setOutgoingAndSend((short)0, (short)11); 
				
				return;
				
			case (byte)0xa5: // second APDU
				apdu.setIncomingAndReceive(); // read APDU data bytes
				Util.arrayCopy(buf, (short)0, destMemory, memPointer, recievedLen);
				memPointer += recievedLen;
				
				// Set FF FF FF after received command
				Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
				memPointer += 3;
				
				Util.arrayCopy(resp2, (short)0, buf, (short)0, (short)76);
				apdu.setOutgoingAndSend((short)0, (short)76); 
				return;
			
			case (byte)0x87: // third and fourth APDU
				apdu.setIncomingAndReceive(); // read APDU data bytes
				if (buf[ISO7816.OFFSET_LC] == 0x04) {
					Util.arrayCopy(buf, (short)0, destMemory, memPointer, recievedLen);
					memPointer += recievedLen;
					
					// Set FF FF FF after received command
					Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
					memPointer += 3;
					
					Util.arrayCopy(resp3, (short)0, buf, (short)0, (short)16);
					apdu.setOutgoingAndSend((short)0, (short)16); 
					return;
				}
				else if (buf[ISO7816.OFFSET_LC] == 0x2c) {
					Util.arrayCopy(buf, (short)0, destMemory, memPointer, recievedLen);
					memPointer += recievedLen;
					
					// Set FF FF FF after received command
					Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
					memPointer += 3;
					
					Util.arrayCopy(resp4, (short)0, buf, (short)0, (short)48);
					apdu.setOutgoingAndSend((short)0, (short)48); 
					return;
				}
				return;

			case (byte)0xcb: // fifth APDU
				apdu.setIncomingAndReceive(); // read APDU data bytes
				Util.arrayCopy(buf, (short)0, destMemory, memPointer, recievedLen);
				memPointer += recievedLen;
				
				// Set FF FF FF after received command
				Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
				memPointer += 3;
				
				Util.arrayCopy(resp5, (short)0, buf, (short)0, (short)17);
				apdu.setOutgoingAndSend((short)0, (short)17); 
				return;
			
			case (byte)0x00: // sixth APDU
				apdu.setIncomingAndReceive(); // read APDU data bytes
				Util.arrayCopy(buf, (short)0, destMemory, memPointer, (short)4);
				memPointer += 4;
				
				// Set FF FF FF after received command
				Util.arrayCopy(cmdEnd, (short)0, destMemory, memPointer, (short) 3);
				memPointer += 3;
				
				Util.arrayCopy(resp6, (short)0, buf, (short)0, (short)2);
				apdu.setOutgoingAndSend((short)0, (short)2); 
				return;
				
			case (byte)0xf1: // send back recordings
				Util.arrayCopy(memory1, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
			case (byte)0xf2: // send back recordings
				Util.arrayCopy(memory2, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
			case (byte)0xf3: // send back recordings
				Util.arrayCopy(memory3, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
			case (byte)0xf4: // send back recordings
				Util.arrayCopy(memory4, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
			case (byte)0xf5: // send back recordings
				Util.arrayCopy(memory5, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
			case (byte)0xf6: // send back recordings
				Util.arrayCopy(memory6, (short)0, buf, (short)0, (short)256);
				apdu.setOutgoingAndSend((short)0, (short)256); 
				return;
				
			case (byte)0xfe: // clear memory
				memPointer = 0;
				memoryArraySelector = 1;
				destMemory = memory1;
				Util.arrayCopy(clearMemory, (short)0, memory1, (short)0, (short)256);
				Util.arrayCopy(clearMemory, (short)0, memory2, (short)0, (short)256);
				Util.arrayCopy(clearMemory, (short)0, memory3, (short)0, (short)256);
				Util.arrayCopy(clearMemory, (short)0, memory4, (short)0, (short)256);
				Util.arrayCopy(clearMemory, (short)0, memory5, (short)0, (short)256);
				Util.arrayCopy(clearMemory, (short)0, memory6, (short)0, (short)256);
				return;
		}
		
		ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
	}
}
