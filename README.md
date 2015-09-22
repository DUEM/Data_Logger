Data_Logger
===========

Software for the data logger


===========
Setting up CAN on beaglebone black
===========
Adapted from: http://www.embedded-things.com/bbb/enable-canbus-on-the-beaglebone-black/

To set up CAN with can-utils on the beaglebone here's what you need to do:

Firstly we need to modify the device-tree overlay to enable the can hardware.

SSH into the beaglbone though the USB @192.168.7.2 (you will need to install drivers and use an SSH client such as PUTTY if you are using windows) or otherwise. You will need to have the Beaglebone connected to the internet in some way or another to get some files.

Download BB-DCAN1-00A0.dts from the git using

> wget https://raw.githubusercontent.com/DUEM/Data_Logger/master/BB-DCAN1-00A0.dts

(if you don't have a web connection you could theoretically copy this into a new file using nano)

Compile this into a dtbo file using:

> dtc -O dtb -o BB-DCAN1-00A0.dtbo -b 0 -@ BB-DCAN1-00A0.dts

And enable it using:

> sudo cp BB-DCAN1-00A0.dtbo /lib/firmware

> echo BB-DCAN1 > /sys/devices/bone_capemgr.*/slots

(NB. I think the second of these lines shouldn't have to be repeated, but I've had to run it every time I reboot the BBB)

Ensure the required kernel modules are installed using:

> sudo modprobe can && sudo modprobe can-dev && sudo modprobe can-raw

Now we need to install can-utils, I did the following:

> mkdir tmp && cd tmp/

> git clone https://github.com/linux-can/can-utils.git

> cd can-utils/

> ./autogen.sh

> ./configure

> make

> make install

Now all you need to do to set up CAN is:

> echo BB-DCAN1 > /sys/devices/bone_capemgr.*/slots

> sudo ip link set can0 up type can bitrate 500000

> sudo ifconfig can0 up

Plug your beaglebone into a tranceiver with pins P9_24->RXD and P_26->TXD (these are next to the serial header). Now you can use cansend and candump to send and recieve messages. See: https://discuss.cantact.io/t/using-can-utils/24

===========
Setting up nginx + php on Beaglebone Black
===========

Install nginx:

> apt-get update
> apt-get install nginx

Config files are in /etc/nginx. Server files are in /usr/share/nginx/www.

Disable default processes that use port 80:

> systemctl disable cloud9.service

> systemctl disable gateone.service

> systemctl disable bonescript.service

> systemctl disable bonescript.socket

> systemctl disable bonescript-autorun.service

> systemctl disable avahi-daemon.service

> systemctl disable gdm.service

> systemctl disable mpd.service

Test the installation by going to the ip of your BB in your web-browser.

Install php fastcgi:

> apt-get install php5-fpm php5-mysql

Open /etc/nginx/sites-available/default with your text editor of choice (I use nano) and uncomment the section regarding php fastcgi. Also add index.php to the list of the other index names.

Restart nginx:

> nginx -s reload

Resources:
http://www.element14.com/community/community/designcenter/single-board-computers/next-gen_beaglebone/blog/2013/11/20/beaglebone-web-server--setup
https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04
https://www.nginx.com/resources/wiki/start/topics/examples/phpfcgi/



