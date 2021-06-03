#!/bin/bash

# sudo dockerd &

RUSTFLAGS='-L /usr/arm-linux-gnueabi/lib/ -L /usr/lib/arm-linux-gnueabi/' \
    cross build --target arm-unknown-linux-gnueabi && \
    scp target/arm-unknown-linux-gnueabi/debug/bluetooth2usb pi@raspberrypi.local:~
