#!/usr/bin/env python3

import time
import socket
import usb.core


PRINTER_USB_ID_VENDOR = 0x1fc9
PRINTER_USB_ID_PRODUCT = 0x2016
SERVER_BLUETOOTH_ADDRESS = 'B8:27:EB:7C:30:21'
BLUETOOTH_CHANNEL = 1


class UsbPrinter:
    def __init__(self):
        self.device = usb.core.find(idVendor=PRINTER_USB_ID_VENDOR, idProduct=PRINTER_USB_ID_PRODUCT)
        if self.device is None:
            raise ValueError('Device not found')
        self.config = self.device.get_active_configuration()
        self.interface = self.config[(0, 0)]
        self.endpoint = self.interface[0]
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
    
    def write(self, data):
        self.endpoint.write(data)


printer = None
server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((SERVER_BLUETOOTH_ADDRESS, BLUETOOTH_CHANNEL))
server.listen(0)
client = None

while True:
    if printer is None:
        print('Connecting to printer...')
        try:
            printer = UsbPrinter()
        except Exception as e:
            print('Failed to connect to printer:', e)
            time.sleep(1)
            continue
        print('Printer connected')

    if client is None:
        print('Connecting to client...')
        client, client_address = server.accept()
        print('Client connected:', client_address)

    while True:
        print('Receiving...')
        try:
            data = client.recv(4096)
        except Exception as e:
            print('Client disconnected:', e)
            client.close()
            client = None
            break
        print(f'Received {len(data)} bytes')

        print(f'Printing...')
        try:
            printer.write(data)
        except Exception as e:
            print('Printer disconnected:', e)
            client.send(b'f') # Fail
            printer = None
            break
        print(f'Printed {len(data)} bytes')
        client.send(b's') # Success
