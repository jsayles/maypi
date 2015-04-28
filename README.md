# The MayPi Doorman System
The MayPi Doorman System was developed to serve as the electronic doorman at the newly renovated
Red Victorian Coliving Hotel in San Francisco's historic Haight Ashbury neighborhood.

## What's in a name?
MayPi is named after William May.  William May has been The Fairmont San Francisco's Doorman for over 27 years! As he likes to say this service has helped him earn his PhD in People. He's now up for a Hotel Hero Award for Lifetime Achievement in Operations. 
Learn more here: 
 - https://www.youtube.com/watch?v=c4ozJKBp0XI

## Icon
Lock icon provided by Svangraph
 - https://www.iconfinder.com/icons/61825/lock_icon#size=128

## Hardware
The hardware used for this system includes:
 - Raspberry Pi Model B
 - PiFace Digital I/O Expander
   - Slightly modified to expose 2 GPIO pins
 - Wiegand Key Pad
 - 12v Electric door strike
 - Various other parts

## Software
 - Raspian Wheezy
 - Nginx
 - Gunicorn
 - Django 1.8
 - Python 2.7

## Raspberry Pi Setup

### Install Raspian
https://www.raspberrypi.org/downloads/

### Install a few essentials and set up the pi
```
sudo apt-get install git tmux python-pip python-dev virtualenvwrapper
sudo apt-get install nginx gunicorn supervisor
```
### Disable Swap
```
sudo apt-get remove dphys-swapfile
```
### Ram tmp dir
```
sudo vi /etc/fstab
tmpfs /tmp tmpfs nodev,nosuid,size=50M 0 0
rmdir /var/tmp
ln -s /tmp /var/tmp
```

### Force HDMI
```
sudo vi /boot/config.txt
hdmi_force_hotplug=1
```

### Install Adafuit Tools
https://github.com/adafruit/Adafruit-Pi-Finder#adafruit-raspberry-pi-finder
```
curl -SLs https://apt.adafruit.com/bootstrap | bash
```

### Install Wiring Pi
https://projects.drogon.net/raspberry-pi/wiringpi/download-and-install/
```
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```

### Install PiGPIO
http://abyz.co.uk/rpi/pigpio/download.html
```
git clone https://github.com/joan2937/pigpio
cd PIGPIO
make
make install
```

## Setup Maypi Application
```
sudo adduser maypi
sudo su - maypi
virtualenv webapp
cd webapp
mkdir static
mkdir media
source bin/activate
git clone https://github.com/jsayles/maypi.git
cd maypi
cp maypi/local_settings.example.py maypi/local_settings.py
vi maypi/local_settings.py
pip install -r requirements.txt
./manage.py migrate
./manage.py collectstatic
```

## Setup Nginx/Supervisor/Gunicorn
Follow the instructions in config/README.md