#!/bin/sh
sudo apt-get -y install samba samba-common samba-common-bin
sudo apt-get -y install ntfs-3g python-wxglade python-wxgtk2.8 python-matplotlib
sudo apt-get -y install lighttpd 
sudo service lighttpd force-reload

cd /
sudo mkdir pub
cd pub
sudo git clone https://github.com/PlesaEEVBlog/RPi_LogNut.git
sudo mkdir python
sudo mkdir temp
sudo mkdir log
sudo mkdir www
sudo mkdir scripts
sudo chown -R  pi /pub

# Make a symlink to www
sudo rmdir /var/www/html
sudo ln -s /pub/www/  /var/www/html
sudo ln -s /pub/logs/  /pub/www/logs

# Temporary filesystem
sudo bash -c 'printf "tmpfs           /pub/temp        tmpfs   defaults,noatime,mode=0755,size=128M 0 0\n" >> /etc/fstab'

#Install adafruit library
cd /
cd opt
sudo git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install

#sudo nano /etc/samba/smb.conf
# add following to smb.conf
# Symlink
#follow symlinks = yes
#wide links = yes
#unix extensions = no
#
#[pub]
#   comment= RPi pub
#   path=/pub
#   browseable=Yes
#   writeable=Yes
#   only guest=no
#   create mask=0777
#   directory mask=0777
#   public=no

# following sequence modify smb.conf
sudo bash -c 'printf "# Symlink\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "follow symlinks = yes\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "wide links = yes\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "unix extensions = no\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "[pub]\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   comment= RPi pub\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   path=/pub\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   browseable=Yes\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   writeable=Yes\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   only guest=no\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   create mask=0777\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   directory mask=0777\n" >> /etc/samba/smb.conf'
sudo bash -c 'printf "   public=no\n" >> /etc/samba/smb.conf'
echo "------------DONE---------------------"

# set Password for Samba
echo "Run"
echo "sudo smbpasswd -a pi"
echo "to set Samba password"

