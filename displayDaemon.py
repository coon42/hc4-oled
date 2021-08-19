#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#     Dev: wh0ami
# Licence: Public Domain <https://unlicense.org>
# Project: https://codeberg.org/wh0ami/hc4-oled/

# importing dependencies
from time import sleep, time, strftime, gmtime
from psutil import boot_time
from multiprocessing import cpu_count
from os import path, getloadavg
import mdstat
import subprocess

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

def main():
	# initialize oled display
	device = ssd1306(i2c(port=0, address=0x3C), rotate=2)

	# initialize font
	font = ImageFont.truetype(path.abspath(path.join(path.dirname(__file__), 'fonts', 'DejaVuSansMono.ttf')), 17)

	# method for displaying a string on the oled display
	def printString(string):
		with canvas(device) as draw:
			try:
				draw.text((0, 0), string, fill="white", font=font)
			except IOError:
				pass

	# infinite loop until the process is getting stopped
	while True:
		# sleep value between different content in seconds
		pause = 5

		# read current raid status from /proc/mdstat via mdstat library
		raid = mdstat.parse()
		# iterate over all disks of md0 and request the disks serial number from the kernel
		# each disk has a own view with its raid status (faulty or not)
		for disk in raid['devices']['md0']['disks']:
			cmd = "/lib/udev/scsi_id --page=0x80 --whitelisted --device=/dev/"+ disk +" -x | awk -F'=' '/ID_SERIAL_SHORT/ {print $2;}'"
			process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			output, error = process.communicate()
			id = str(output.decode('UTF-8')).strip()

			result = '+++ Disk +++\n• '+ id +'\n• '
			if raid['devices']['md0']['disks'][disk]['faulty']:
				printString(result +'faulty')
			else:
				printString(result +'not faulty')
			sleep(pause)

		# get the current raid status and display it
		if raid['devices']['md0']['resync'] is not None:
			printString('+++ RAID +++\n• '+ raid['devices']['md0']['resync']['operation'] +'\n• '+ raid['devices']['md0']['resync']['progress'])
		else:
			printString('+++ RAID +++\n• synced')
		sleep(pause)

		# print system load
		load = getloadavg()
		printString('Load1:  '+ str(load[0]) + '\n' + 'Load5:  '+ str(load[1]) + '\n' + 'Load15: '+ str(load[2]))
		sleep(pause)

		# print uptime
		printString('+ Uptime +\n' + strftime("• %d days\n  and %H:%Mh", gmtime(time() - boot_time())))
		sleep(pause)

		# print cpu temperature and freq
		f = open('/sys/class/thermal/thermal_zone0/hwmon0/temp1_input')
		temp = str(int(round(int(f.read())/1000, 0)))
		f.close()

		# the clock rate is calculated as a average over all cores
		corenum = cpu_count()
		freqsum = 0
		for i in range(corenum):
			f = open('/sys/devices/system/cpu/cpu'+ str(i) +'/cpufreq/cpuinfo_cur_freq')
			freq = int(f.read())
			f.close()
			freqsum += freq
		freq = str(int(round(freqsum/1000/corenum, 0)))

		printString('+++ CPU +++\n• '+ temp +'°C\n• '+ freq +' MHz')
		sleep(pause)

# main method
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass