#!//bin/bash
cd /
cd opt
# wget https://sourceforge.net/code-snapshots/svn/l/li/linux-gpib/code/linux-gpib-code-1655-trunk.zip
sudo wget https://downloads.sourceforge.net/project/linux-gpib/linux-gpib%20for%203.x.x%20and%202.6.x%20kernels/4.0.4/linux-gpib-4.0.4rc2.tar.gz
sudo tar xvzf linux-gpib-4.0.4rc2.tar.gz
#sudo svn checkout http://svn.code.sf.net/p/linux-gpib/code/trunk/linux-gpib/ linux-gpib
cd linux-gpib-4.0.4rc2
sudo ./bootstrap
sudo ./configure
sudo make clean
sudo make
sudo make install
