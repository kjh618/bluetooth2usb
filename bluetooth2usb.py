#!/usr/bin/env python3

import time
import socket
import usb.core


USB_DEVICE_ID_VENDOR = 0x1fc9
USB_DEVICE_ID_PRODUCT = 0x2016

BLUETOOTH_SERVER_ADDRESS = 'B8:27:EB:7C:30:21'
BLUETOOTH_CHANNEL = 1


class UsbDevice:
    def __init__(self):
        self.device = None
        while True:
            self.device = usb.core.find(idVendor=USB_DEVICE_ID_VENDOR, idProduct=USB_DEVICE_ID_PRODUCT)
            if self.device is not None:
                break
            time.sleep(1)
        self.config = self.device.get_active_configuration()
        self.interface = self.config[(0, 0)]
        self.endpoint = self.interface[0]
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
    
    def id(self):
        return f'{self.device.idVendor:x}:{self.device.idProduct:x}'

    def write(self, data):
        self.endpoint.write(data)


usb_device = None
bt_server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
bt_server.bind((BLUETOOTH_SERVER_ADDRESS, BLUETOOTH_CHANNEL))
bt_server.listen(0)
bt_client = None

while True:
    print('-' * 50)

    if usb_device is None:
        print('Connecting to USB device...')
        try:
            usb_device = UsbDevice()
        except Exception as e:
            print('Failed to connect to USB device:', e)
            time.sleep(1)
            continue
    print('USB device connected:', usb_device.id())

    if bt_client is None:
        print('Connecting to Bluetooth client...')
        try:
            bt_client, bt_client_address = bt_server.accept()
        except Exception as e:
            print('Failed to connect to Bluetooth client:', e)
            time.sleep(1)
            continue
    print('Bluetooth client connected:', bt_client_address)

    while True:
        print('Receiving data from Bluetooth client...')
        try:
            data = bt_client.recv(4096)
        except Exception as e:
            print('Bluetooth client disconnected:', e)
            bt_client.close()
            bt_client = None
            break
        print(f'Received {len(data)} bytes')

        print('Writing data to USB device...')
        try:
            usb_device.write(data)
        except Exception as e:
            print('USB device disconnected:', e)
            bt_client.send(b'f') # Fail
            usb_device = None
            break
        print(f'Wrote {len(data)} bytes')
        bt_client.send(b's') # Success
