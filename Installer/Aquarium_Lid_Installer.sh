#!/bin/bash

apt-get update && apt-get upgrade -y

apt-get install git -y

git clone https://github.com/LaserPete/Aquarium_Lid_Python

apt-get install python3 -y

apt-get install python3-pip -y

apt-get install python3-pil -y

apt-get install python3-numpy -y

pip3 install RPi.GPIO

pip3 install spidev

pip3 install sensor

pip3 install smbus

touch /etc/crontab

echo "@reboot pi bash /home/pi/Aquarium_Lid_Python/Aquarium_Lid.sh" >> /etc/crontab

raspi-config nonint do_i2c 0

raspi-config nonint do_spi 0

reboot

exit 0

