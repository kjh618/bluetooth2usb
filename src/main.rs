use bluetooth2usb::UsbDevice;
use std::process;

fn main() {
    let device = UsbDevice::new().unwrap_or_else(|e| {
        eprintln!("{}", e);
        process::exit(1);
    });

    device.write(b"test\n").unwrap_or_else(|e| {
        eprintln!("{}", e);
        process::exit(1);
    });
}
