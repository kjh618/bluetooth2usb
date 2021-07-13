# bluetooth2usb

Use a Raspberry Pi to add Bluetooth capabilities to a USB device.

<img alt="Title image" src="/images/20210710_160922.jpg" width=300>

`bluetooth2usb.py` receives data from a Bluetooth connection and writes that data to a connected USB device byte-for-byte.

It can be used to convert a simple USB printer to a Bluetooth capable one.


## Usage

1. Download and copy `bluetooth2usb.py` to your Raspberry Pi.
2. Modify the constant values `USB_DEVICE_ID_VENDOR`, `USB_DEVICE_ID_PRODUCT`, `BLUETOOTH_SERVER_ADDRESS`, `LED_PIN` at the top of the file as necessary.
3. Run `bluetooth2usb.py`.
4. Or to install it as a `systemd` service, follow the instruction at [the official Raspberry Pi docs](https://www.raspberrypi.org/documentation/linux/usage/systemd.md). Example `.service` file can be found at `bluetooth2usb.service`.
5. Connect a USB device and a Bluetooth client to the Pi.
6. Send Bluetooth data from the client to the Pi. The connected USB device should receive the same data.


## LED Behavior

* Slowly blinking (0.2 s on, 0.8 s off): Waiting for a USB device to be connected.
* Quickly blinking (0.1 s on, 0.1 s off): Waiting for a Bluetooth connection.
* Continuously on: Everything is connected and waiting for Bluetooth data.
* Quickly blinking twice while on: Received and wrote data.
