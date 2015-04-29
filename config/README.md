# Configuration Files

## Webapp Start Scripts
```
cp gunicorn_start /home/maypi/webapp/bin/
cp wiegand_start /home/maypi/webapp/bin/
```

## Supervisor Config files
```
cp supervisor/gunicorn.conf /etc/supervisor/conf.d/
cp supervisor/wiegand.conf /etc/supervisor/conf.d/
```

## NGINX
```
cp nginx/maypi.conf /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/maypi.conf /etc/nginx/sites-enabled
```

## PiGPIO
http://abyz.co.uk/rpi/pigpio/download.html
```
git clone https://github.com/joan2937/pigpio
cd PIGPIO
make
make install
sudo cp /home/maypi/webapp/maypi/config/init/pigpiod /etc/init.d/pigpiod
sudo update-rc.d pigpiod defaults
```