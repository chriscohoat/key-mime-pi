# !/usr/bin/python3

# https://stackoverflow.com/questions/37943825/send-hid-report-with-pyusb

import usb.core

dev = usb.core.find(idVendor=0x1d6b, idProduct=0x0104)

if dev is None:
    raise ValueError('Device not found')

try:
    dev.reset()
except Exception as e:
    print( 'reset', e)

reattach = False
if dev.is_kernel_driver_active(0):
    print( 'detaching kernel driver')
    reattach = True
    dev.detach_kernel_driver(0)

print("Claiming device")

endpoint_in = dev[0][(0,0)][0]
endpoint_out = dev[0][(0,0)][1]

# Send a command to the Teensy
endpoint_out.write( "version".encode() + bytes([0]) )

# Read the response, an array of byte, .tobytes() gives us a bytearray.
buffer = dev.read(endpoint_in.bEndpointAddress, 64, 1000).tobytes()

# Decode and print the zero terminated string response
n = buffer.index(0)
print( buffer[:n].decode() )

print("Done")

# This is needed to release interface, otherwise attach_kernel_driver fails
# due to "Resource busy"
usb.util.dispose_resources(dev)

# It may raise USBError if there's e.g. no kernel driver loaded at all
if reattach:
    print("Reattaching kernel driver")
    dev.attach_kernel_driver(0)