#!//bin/bash
Raspbian_version=`egrep "jessie|wheezy" /etc/os-release`
if [ `echo $Raspbian_version|grep -c "jessie"` == 1 ]
then
  echo "Raspbian Jessie detected"
else
  echo "Other version of Raspbian detected"
fi


kernel_version=`uname -a|awk '{print $3}'`
if [ $kernel_version != "4.4.38-v7+" ]
then
        echo "Kernel version is not 4.4.38, running update,upgrate and dist-upgrade"
        sudo apt-get update
        sudo apt-get -y upgrade
        sudo apt-get -y dist-upgrade
        sudo apt-get -y install raspberrypi-kernel raspberrypi-kernel-headers raspberrypi-bootloader
        echo "Raspberry Pi needs to reboot to load new kernel and then run script again"
        read -rsp $'Press enter to continue...\n'
        sudo reboot
else
        echo "Proper kernel detected"
        read -rsp $'Press enter to continue...\n'
fi

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get -y install raspberrypi-kernel raspberrypi-kernel-headers raspberrypi-bootloader
sudo apt-get -y install screen mc i2c-tools samba samba-common-bin bc python-dev rpi-update tk-dev build-essential texinfo texi2html libcwidget-dev libncurses5-dev libx11-dev binutils-dev bison flex libusb-1.0-0 libusb-dev libmpfr-dev libexpat1-dev tofrodos subversion autoconf automake libtool
sudo apt-get -y purge wolfram-engine sonic-pi scratch
sudo apt-get -y autoremove
#sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source && sudo chmod +x /usr/bin/rpi-source && /usr/bin/rpi-source -q --tag-update
#sudo rpi-source
cd /
cd opt
sudo svn checkout http://svn.code.sf.net/p/linux-gpib/code/trunk/linux-gpib/ linux-gpib
cd linux-gpib
sudo ./bootstrap
sudo ./configure
sudo make clean
sudo make
sudo make install
cd ..
sudo svn checkout https://github.com/python-ivi/python-vxi11/trunk python-vxi11
cd python-vxi11
sudo python setup.py install
cd ..
sudo svn checkout https://github.com/python-ivi/python-usbtmc/trunk python-usbtmc
cd python-usbtmc
sudo python setup.py install
cd ..
# Install FxLoad
sudo mkdir gpib_firmware
cd gpib_firmware
sudo wget http://linux-gpib.sourceforge.net/firmware/gpib_firmware-2008-08-10.tar.gz
sudo tar xvzf gpib_firmware-2008-08-10.tar.gz
sudo cp  gpib_firmware-2008-08-10/agilent_82357a/82357a_fw.hex /usr/share/usb/agilent_82357a/
sudo cp  gpib_firmware-2008-08-10/agilent_82357a/measat_releaseX1.8.hex /usr/share/usb/agilent_82357a/
sudo cp  gpib_firmware-2008-08-10/ni_gpib_usb_b/niusbb_loader.hex /usr/share/usb/ni_usb_gpib/
sudo cp  gpib_firmware-2008-08-10/ni_gpib_usb_b/niusbb_firmware.hex /usr/share/usb/ni_usb_gpib/
sudo apt-get -y install fxload

# SI units prefix support in Python
# https://github.com/cfobel/si-prefix
sudo pip install --upgrade pip
sudo pip install si-prefix

if lsusb | grep -q '0957:0518'; then
sudo sed -i 's/ni_pci/agilent_82357a/g' /etc/gpib.conf
echo "Agilent 82357B found"
sudo modprobe agilent_82357a
fi

if lsusb | grep -q '3923:709b'; then
sudo sed -i 's/ni_pci/ni_usb_b/g' /etc/gpib.conf
echo "National Instruments NI GPIB-USB-HS found"
sudo modprobe ni_usb_gpib
fi

sudo ldconfig
sudo depmod -a
sudo gpib_config