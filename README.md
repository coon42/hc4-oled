# hc4-oled

This is a simple python3 daemon for the OLED display of the Odroid HC4. It can display some information about the operating system, the disks and some other hardware components.  
  
I developed and tested this on a Odroid HC4 with Armbian Buster, kernel 5.10.57-meson64 and a mdadm RAID1 consisting of two Toshiba DT01ACA300 hard disks. 

### Setup
```
root@odroidhc4:~# apt update
root@odroidhc4:~# apt install --no-install-recommends --no-install-suggests python3 python3-pip python3-dev python3-setuptools python3-wheel python3-psutil zlib1g-dev libjpeg-dev libfreetype6-dev git
root@odroidhc4:~# pip3 install --upgrade luma.core luma.oled Pillow mdstat
root@odroidhc4:~# cd /opt/
root@odroidhc4:/opt# git clone https://codeberg.org/wh0ami/hc4-oled/
root@odroidhc4:/opt# cd hc4-oled/
root@odroidhc4:/opt/hc4-oled# chmod -R o-rwx .
root@odroidhc4:/opt/hc4-oled# chmod 750 displayDaemon.py
root@odroidhc4:/opt/hc4-oled# cp hc4-oled.service /etc/systemd/system/
root@odroidhc4:/opt/hc4-oled# systemctl daemon-reload
root@odroidhc4:/opt/hc4-oled# systemctl enable --now hc4-oled.service
```

If you want to see, whether the service is currently running, you can use `systemctl status hc4-oled.service`.
