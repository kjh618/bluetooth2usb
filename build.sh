#!/bin/bash

cargo build --target=arm-unknown-linux-gnueabi && scp target/arm-unknown-linux-gnueabi/debug/bluetooth2usb pi@raspberrypi.local:~
