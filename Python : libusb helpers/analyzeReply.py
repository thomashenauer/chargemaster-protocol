########################################################################################################################
# analyzeReply.py
#
# Functions for decoding the usb transaction-replies of Turnigy Accucell 6 80W Charger
########################################################################################################################

import binascii
import struct
from termcolor import colored


def transaction_5a(result):

    print '\nReceived data:'

    if binascii.b2a_hex(result[0]) != '0f':
        print colored('Header not correct! Aborting decoding. Received: ' + binascii.b2a_hex(result[0]), 'red')
        return

    packetlength = struct.unpack('B', result[1])[0]
    if packetlength != 37:
        print colored('Unexpected packet length! Aborting decoding. Received: ' + binascii.b2a_hex(result[1]), 'red')
        return

    if binascii.b2a_hex(result[2]) != '5a':
        print colored('Wrong transaction type! Aborting decoding. Received: ' + binascii.b2a_hex(result[2]), 'red')
        return

    unknown1 = binascii.b2a_hex(result[3])
    print 'Unknown field Nr. 1:', unknown1
    if unknown1 != '00':
        print colored('!!! Values changed !!! previous: 00', 'red')

    resttime = struct.unpack('B', result[4])[0]
    print 'Resttime:', resttime, 'minutes'

    temp = struct.unpack('B', result[5])[0]
    if temp == 1:
        saftytimerenable = True
    else:
        saftytimerenable = False
    print 'Safty Timer Enable:', saftytimerenable
    saftytimertimeout = struct.unpack('>H', result[6:8])[0]
    print 'Safty Timer Timeout:', saftytimertimeout, 'minutes'

    temp = struct.unpack('B', result[8])[0]
    if temp == 1:
        capacitycutoutenable = True
    else:
        capacitycutoutenable = False
    print 'Capacity Cutout Enable:', capacitycutoutenable
    capacitycutoutvalue = struct.unpack('>H', result[9:11])[0]
    print 'Capacity Cutout Value:', capacitycutoutvalue, 'mAh'

    temp = struct.unpack('B', result[11])[0]
    if temp == 1:
        keybeepenable = True
    else:
        keybeepenable = False
    print 'Keybeep Enable:', keybeepenable

    temp = struct.unpack('B', result[12])[0]
    if temp == 1:
        buzzerenabled = True
    else:
        buzzerenabled = False
    print 'Buzzer Enable:', buzzerenabled

    inputcutoff = float(struct.unpack('>H', result[13:15])[0])/1000
    print 'Input Cutoff Voltage:', inputcutoff, 'V'

    unknown2 = binascii.b2a_hex(result[15:17])
    print 'Unknown field Nr. 2:', unknown2
    if unknown2 != '0000':
        print colored('!!! Values changed !!! previous: 0000', 'red')

    protectiontemp = struct.unpack('B', result[17:18])[0]
    print 'Protection Temperature:', protectiontemp, 'degrees'

    batteryvoltage = float(struct.unpack('>H', result[18:20])[0])/1000
    print 'Battery Voltage:', batteryvoltage, 'V'

    cell1voltage = float(struct.unpack('>H', result[20:22])[0])/1000
    print 'Cell 1 Voltage:', cell1voltage, 'V'

    cell2voltage = float(struct.unpack('>H', result[22:24])[0])/1000
    print 'Cell 2 Voltage:', cell2voltage, 'V'

    cell3voltage = float(struct.unpack('>H', result[24:26])[0])/1000
    print 'Cell 3 Voltage:', cell3voltage, 'V'

    cell4voltage = float(struct.unpack('>H', result[26:28])[0])/1000
    print 'Cell 4 Voltage:', cell4voltage, 'V'

    cell5voltage = float(struct.unpack('>H', result[28:30])[0])/1000
    print 'Cell 5 Voltage:', cell5voltage, 'V'

    cell6voltage = float(struct.unpack('>H', result[30:32])[0])/1000
    print 'Cell 6 Voltage:', cell6voltage, 'V'

    unknown3 = binascii.b2a_hex(result[32:38])
    print 'Unknown field Nr. 3:', unknown3
    if unknown3 != '000000000000':
        print colored('!!! Values changed !!! previous: 000000000000', 'red')

    unknown4 = binascii.b2a_hex(result[38:39])
    print colored('Unknown field Nr. 4: ' + str(unknown4) + ' (changes)', 'yellow')

    if binascii.b2a_hex(result[39:41]) != 'ffff':
        print colored('Stop sign not correct! Aborting decoding. Received: ' + binascii.b2a_hex(result[39:41]), 'red')
        return

    print '\nData received:'
    print binascii.b2a_hex(result)