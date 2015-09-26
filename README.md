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

===========
Mount SD-Card to extend storage
===========

Shut down the beaglebone and plug in the SD-card. List the available drives:

> fdisk -l

You should see a list of drives and their partitions. If you turned on the beaglebone with the sd card inserted it will be located at /dev/mmcblk0, otherwise it will be at /dev/mmcblk1. Now use fdisk to modify the drive partitions (e careful to get the right drive here!):

> fdisk /dev/mmcblk0

This will open up a console program. Use d to delete the existing partitions and n to create a new one. Once you are done, use p to verify that you have the right partition and wite it to the card using w.

Finally, add the following line to /etc/fstab:

> /dev/mmcblk0p1    /media/card     auto     auto,rw,async,user,nofail  0  0

Contents of the sdcard will be available under /media/card/ .

You can now move your mysql database data to the sdcard by changing the value of datadir in /etc/mysql/my.cnf from /var/lib/mysql to /media/card/mysql and moving files (with permissions using rsync -a /var/lib/mysql/ /media/card/mysql/ .

http://electronicsembedded.blogspot.co.uk/2014/10/beaglebone-black-using-sd-card-as-extra.html

===========
Set up script to run automatically
===========

Create a shell script such as /root/start_logging.sh (make sure to set it to be executable and ensure permissions are set with chmod -x and chmod 777)

Create a service file in /lib/systemd/system/data_logger.service such as:

'[Unit]
Description=My Fancy Service
Requires=mysql.service
After=mysql.service

[Service]
Type=simple
ExecStart=/usr/bin/myFancyBash.sh

[Install]
WantedBy=multi-user.target'

Create a symbolic link between your script and a special location under /etc:

> ln -s /lib/systemd/system/data_logger.service /etc/systemd/system/data_logger.service

Make systemd aware of your new service

> systemctl daemon-reload

> systemctl enable data_logger.service

> systemctl start data_logger.service

Use can then use systemctl stop/start/status/disable to manipulte the service.

https://gist.github.com/tstellanova/7323116

