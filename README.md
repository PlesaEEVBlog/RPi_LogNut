# RPi_LogNut
Logging platform based on RPi2/3 Raspbian and using D3js for data visualization
To install on Raspberry Pi, dowload latest Raspbian 
https://downloads.raspberrypi.org/raspbian/images/raspbian-2017-03-03/2017-03-02-raspbian-jessie.zip
Restore it to SD card and after automatic resize run

curl https://raw.githubusercontent.com/PlesaEEVBlog/RPi_LogNut/master/Install_GPIB_Support.sh | sudo bash

This version is working with kernel 4.4.50
Used linux-gpib-4.0.4rc2 where is patched support issue for NI GPIB-USB HS adapter
