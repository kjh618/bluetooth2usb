use std::time::Duration;

fn main() {
    let devices = rusb::devices().unwrap();
    for device in devices.iter() {
        println!("{:?}", device);
    }
    let device = devices.iter().nth(0).unwrap();

    let config = device.active_config_descriptor().unwrap();
    println!("{:?}", config);

    let interface = config.interfaces().nth(0).unwrap();
    let interface = interface.descriptors().nth(0).unwrap();

    let endpoints = interface.endpoint_descriptors();
    for endpoint in endpoints {
        println!("{:?}\n{:?}\n{:?}", endpoint, endpoint.direction(), endpoint.transfer_type());
    }
    let endpoint = interface.endpoint_descriptors().nth(0).unwrap();

    let mut handle = device.open().unwrap();
    handle.set_auto_detach_kernel_driver(true).unwrap();
    handle.claim_interface(interface.interface_number()).unwrap();
    handle.write_bulk(endpoint.address(), b"test\n", Duration::from_secs(5)).unwrap();
}
