########################################################################################################################
# usb_transaction_testbench.py
#
# Testbench for testing single transactions with Turnigy Accucell 6 80W charger
# Code is written in PyCharm IDE 5.0.1 and runs on Ubuntu 14.04
########################################################################################################################

import usb1
import binascii
from analyzeReply import *


VENDOR_ID = 0000
PRODUCT_ID = 0001
INTERFACE = 0
context = usb1.USBContext()

result = context.getDeviceList(skip_on_access_error=False, skip_on_error=False)

deviceList = []

for device in result:
    if device.getVendorID() == VENDOR_ID and \
                    device.getProductID() == PRODUCT_ID:
        print('found')
        busnum = device.getBusNumber()
        print 'Bus Nr.:', busnum
        portlist = device.getPortNumberList()
        print 'Port list:', portlist
        address = device.getDeviceAddress()
        print 'Device bus address:', address
        deviceList.append(device)

if len(deviceList) < 1:
    print 'error: no device found'
else:
    device = deviceList[0]
    handle = device.open()

    if handle.kernelDriverActive(INTERFACE):
        print('kernel active')
        handle.detachKernelDriver(INTERFACE)
        print('kernel detached')
        if handle.kernelDriverActive(INTERFACE):
            print('error detaching kernel')
    else:
        print('kernel inactive')

    handle.claimInterface(INTERFACE)

    print 'interface claimed'

    endpoint = 1
    data = binascii.unhexlify('0f035a005affff0000000000000000000000000000000000000000000000000000000000000000000000000'
                              '00000000000000000000000000000000000000000')
    # data = binascii.unhexlify('0f03570057ffff0000000000000000000000000000000000000000000000000000000000000000000000000'
    #                           '00000000000000000000000000000000000000000')
    # data = binascii.unhexlify('0f035f005fffff0000000000000000000000000000000000000000000000000000000000000000000000000'
    #                           '00000000000000000000000000000000000000000')

    timeoutms = 1000
    sent = handle.interruptWrite(endpoint, data, timeoutms)
    print 'Nr. bytes sent:', sent
    result = handle.interruptRead(endpoint, 64)

    transaction_5a(result)

    print '\nData received:'
    print binascii.b2a_hex(result)


    handle.releaseInterface(INTERFACE)
    print 'interface released'
    # handle.attachKernelDriver(INTERFACE)
    # print 'kernel driver reattached'
