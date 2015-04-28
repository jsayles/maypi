# Configuration Files

## Webapp Start Scripts
cp gunicorn_start /home/maypi/webapp/bin/
cp wiegand_start /home/maypi/webapp/bin/

## Supervisor Config files
cp gunicorn.conf /etc/supervisor/conf.d/
cp wiegand.conf /etc/supervisor/conf.d/
