use rusb::{DeviceHandle, GlobalContext};
use std::time::Duration;

pub struct UsbDevice {
    endpoint_address: u8,
    handle: DeviceHandle<GlobalContext>,
}

impl UsbDevice {
    pub fn new() -> rusb::Result<UsbDevice> {
        // TODO: Search for valid device/interface/endpoint
        // TODO: Return error instead of unwrapping options

        let devices = rusb::devices()?;
        // for device in devices.iter() {
        //     println!("{:?}", device);
        // }
        let device = devices.iter().nth(0).unwrap();

        let config = device.active_config_descriptor()?;
        // println!("{:?}", config);

        let interface = config.interfaces().nth(0).unwrap();
        let interface = interface.descriptors().nth(0).unwrap();

        let mut endpoints = interface.endpoint_descriptors();
        // for endpoint in interface.endpoint_descriptors() {
        //     println!("{:?}, {:?}, {:?}", endpoint, endpoint.direction(), endpoint.transfer_type());
        // }
        let endpoint = endpoints.nth(0).unwrap();

        let mut handle = device.open()?;
        handle.set_auto_detach_kernel_driver(true)?;
        handle.claim_interface(interface.interface_number())?;

        Ok(UsbDevice {
            endpoint_address: endpoint.address(),
            handle,
        })
    }

    pub fn write(&self, bytes: &[u8]) -> rusb::Result<usize> {
        self.handle
            .write_bulk(self.endpoint_address, bytes, Duration::from_secs(5))
    }
}
