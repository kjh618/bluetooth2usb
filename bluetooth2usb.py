#!/usr/bin/env python3

import time
import socket
import usb.core
import gpiozero


USB_DEVICE_ID_VENDOR = 0x1fc9
USB_DEVICE_ID_PRODUCT = 0x2016

BLUETOOTH_SERVER_ADDRESS = 'B8:27:EB:7C:30:21'
BLUETOOTH_CHANNEL = 1

LED_PIN = 5


class UsbDevice:
    def __init__(self, id_vendor, id_product):
        self.device = None
        while True:
            self.device = usb.core.find(idVendor=id_vendor, idProduct=id_product)
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


class BluetoothClient:
    def __init__(self, bt_socket):
        self.bt_socket = bt_socket

    def address(self):
        address, channel = self.bt_socket.getpeername()
        return f'{address}, {channel}'

    def recv(self, n):
        return self.bt_socket.recv(n)

    def close(self):
        self.bt_socket.close()


usb_device = None

bt_server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
bt_server_socket.bind((BLUETOOTH_SERVER_ADDRESS, BLUETOOTH_CHANNEL))
bt_server_socket.listen(0)
bt_client = None

led = gpiozero.LED(LED_PIN)
led.blink(1, 1)

while True:
    print('-' * 50)

    # TODO: Check if connected as well
    if usb_device is None:
        print('Connecting to USB device...')
        led.blink(0.2, 0.8)
        try:
            usb_device = UsbDevice(USB_DEVICE_ID_VENDOR, USB_DEVICE_ID_PRODUCT)
        except Exception as e:
            print('Failed to connect to USB device:', e)
            time.sleep(1)
            continue

    print('USB device connected:', usb_device.id())

    # TODO: Check if connected as well
    if bt_client is None:
        print('Connecting to Bluetooth client...')
        led.blink(0.1, 0.1)
        try:
            bt_client_socket, _ = bt_server_socket.accept()
            bt_client = BluetoothClient(bt_client_socket)
        except Exception as e:
            print('Failed to connect to Bluetooth client:', e)
            time.sleep(1)
            continue

    print('Bluetooth client connected:', bt_client.address())

    while True:
        led.on()

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
            usb_device = None
            print('Disconnecting bluetooth client...')
            bt_client.close()
            bt_client = None
            print('Bluetooth client disconnected')
            break

        print(f'Wrote {len(data)} bytes')
        led.blink(0.1, 0.1, 2, False)
