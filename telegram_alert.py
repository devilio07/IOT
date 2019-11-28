import requests
import json, time, conf
from boltiot import Bolt

product=Bolt(conf.API,conf.ID)

def get_sensor_value(pin):
	try:
		response=product.analogRead(pin)
		data=json.loads(response)
		if data["success"] !=1:
			print("Request unsuccessful")
			print("Response is :",data)
			return -999
		sensor_value=int(data['value'])
		return sensor_value
	except Exception as e:
		print("Something went wrong")
		print(e)
		return -999

def telegram_message(message):
	url="https://api.telegram.org/" + conf.BOT_ID + "/sendMessage"
	data={
		"chat_id":conf.CHAT_ID,
		"text":message
	}

	try:
		response=requests.request(
			"POST",
			url,
			params=data
		)
		print("Telegram response:")
		print(response.text)
		telegram_data=json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
		print("An error occured in sendinf the alert message via Telegram")
		print(e)
		return False

while True:
	sensor_value=get_sensor_value("A0")
	print("The current sensor value is :",sensor_value)

	if sensor_value==-999:
		print("Request was unsuccesdfull. Skipping")
		time.sleep(10)
		continue
	
	if sensor_value>= conf.threshold:
		print("Sensor value has exceeded the threshold")
		message="Alert! Sensor value has exceeded " + str(conf.threshold)+ ". The current value is " + str(sensor_value)
		telegram_status=telegram_message(message)
		print("This is telegram status :",telegram_status)

	time.sleep(10)
