from config import *
import requests
import os
import time
import subprocess
import datetime

statsdict = {}
statsdict["last_sent"] = int(time.time())

def push(**kwargs):
	response = requests.post(PUSHOVER_URL, data=kwargs)
	responsejson = response.json()
	if responsejson['status'] == 1:
		return 'Successful'
	else:
		return 'Error'

def ping(ip):
	command = subprocess.Popen(["ping", "-n", "-c 5", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, error = command.communicate()
	return out

if __name__ == "__main__":
	while True:

		#Ping the device to see if it appears
		result = ping(DEVICE_IP)

		#If it did, set it to True
		statsdict["device_present"] = "time=" in result

		#Work out the time difference
		timedifference = statsdict["last_sent"] - int(time.time())

		#If the device is here, and we haven't seen it in a while
		if statsdict["device_present"] and timedifference > 600:
			push(user=USER_ID, token=API_TOKEN, 
				 message="%s just got home" % (NAME,), 
				 title=APP_NAME)
			statsdict["last_sent"] = int(time.time())

		#Sleep for a bit
		time.sleep(600)