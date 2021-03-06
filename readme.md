
Aquarium Lid Installation
-------------------------

1. Take a micro SD card

1. Burn a new image of Raspian Lite onto it

1. In the boot partition of the SD card, create a file called "ssh". Lower case, no file extension.
This will enable SSH from first boot. The Pi will delete the file once it has changed the setting.

1. In the rootfs partition of the SD card, navigate to /etc/wpa_supplicant.

1. Open wpa_supplicant.conf in an editor, add the following lines, and enter your WiFi information

	```
	network={
	ssid="WIFI_SSID"
	psk="WIFI_PASSWORD"
	}
	```

	The RasPi should now join your WiFi network on boot

1. Put the SD card in the RasPi, turn it on, log in over SSH.

	It will give you a warning about the remote host identification changing

1. Change the password on the Pi

1. Update, Upgrade, install relevant packages;
	```
	sudo apt-get update -y
 	sudo apt-get upgrade -y 

	sudo apt-get install python3 python3-pip python3-pil python3-numpy git -y

	pip3 install RPi.GPIO spidev sensor smbus
	```  

1. Clone the git repository
	```
	git clone https://github.com/LaserPete/Aquarium_Lid_Python.git /home/pi/Aquarium_Lid_Python
	```
1. Modify Crontab in order to get the script to run on boot using 
	```
	sudo touch /etc/crontab
    sudo echo "@reboot pi bash /home/pi/Aquarium_Lid_Python/Aquarium_Lid.sh" >> /etc/crontab
	```

1. Enable the i2c and SPI buses on the Raspberry Pi.
	```    
	sudo raspi-config nonint do_i2c 0
    sudo raspi-config nonint do_spi 0
	```
1. When it is all done, sudo reboot, hope for the best
