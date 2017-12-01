#!/bin/bash
sudo rmmod i2c_bcm2708
sudo rmmod i2c_dev
sudo modprobe i2c_bcm2708
sudo modprobe i2c_dev

