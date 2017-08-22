# RPi_LogNut
Logging platform based on RPi2/3 Raspbian and using D3js for data visualization
To install on Raspberry Pi, dowload latest Raspbian 
https://downloads.raspberrypi.org/raspbian_latest
or
https://downloads.raspberrypi.org/raspbian/images/raspbian-2017-08-17/2017-08-16-raspbian-stretch.zip

Restore it to SD card and after automatic resize run

curl https://raw.githubusercontent.com/PlesaEEVBlog/RPi_LogNut/master/Install_GPIB_Support.sh | sudo bash

This version is working with Raspbian on RPi0, RPi0W, RPi2,RPi3.RPi1 should work as well, but was not tested.
Used linux-gpib-4.0.4rc2 where is patched support for NI GPIB-USB HS adapter

Optional:

After kernel update run 
curl https://raw.githubusercontent.com/PlesaEEVBlog/RPi_LogNut/master/Update_GPIB.sh | sudo bash

Setup webserver and Samba :
curl https://raw.githubusercontent.com/PlesaEEVBlog/RPi_LogNut/master/Web_Samba.sh | sudo bash

Overclock SD card :
sudo bash -c 'printf "dtoverlay=sdtweak,overclock_50=80\n" >> /boot/config.txt'

Test overclock :
curl http://www.nmacleod.com/public/sdbench.sh | sudo bash
