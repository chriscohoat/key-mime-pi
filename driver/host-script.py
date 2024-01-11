# !/usr/bin/python3

# https://stackoverflow.com/questions/37943825/send-hid-report-with-pyusb

import usb.core

def hid_set_report(dev, report):
      """ Implements HID SetReport via USB control transfer """
      dev.ctrl_transfer(
          0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
          9,     # SET_REPORT
          0x200, # "Vendor" Descriptor Type + 0 Descriptor Index
          0,     # USB interface № 0
          report # the HID payload as a byte array -- e.g. from struct.pack()
      )
def hid_get_report(dev):
      """ Implements HID GetReport via USB control transfer """
      return dev.ctrl_transfer(
          0xA1,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
          1,     # GET_REPORT
          0x200, # "Vendor" Descriptor Type + 0 Descriptor Index
          0,     # USB interface № 0
          64     # max reply size
      )
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x10,  #   Usage Maximum (Button 16)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x10,  #   Report Count (16)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x04,  #   Report Count (4)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))

dev = usb.core.find(idVendor=0x1d6b, idProduct=0x0104)

if dev is None:
    raise ValueError('Device not found')

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

dev.set_configuration()

# Gettting the report

print("Getting report")

report = hid_get_report(dev)

print("Report: ", report)

# send the report

# hid_set_report(dev, GAMEPAD_REPORT_DESCRIPTOR)
print("Sending report")

# This is needed to release interface, otherwise attach_kernel_driver fails
# due to "Resource busy"
usb.util.dispose_resources(dev)

# It may raise USBError if there's e.g. no kernel driver loaded at all
if reattach:
    print("Reattaching kernel driver")
    dev.attach_kernel_driver(0)