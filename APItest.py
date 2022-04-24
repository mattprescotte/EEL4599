import requests
import time

while True:
	currentTemp = 330
	currentPres = 225
	myString = "http://api.thingspeak.com/update?api_key=8O0PFDFMUYX0ARAN&field1=" + str(currentTemp) + "&field2=" + str(currentPres)
	requests.get(myString)
	print("Temperature and pressure update made!")
	time.sleep(4)
