import time
import machine
import network
import urequests as requests

net = network.WLAN(network.STA_IF)
net.active(True)
net.connect('patrick', 'pkgprateek')

while not net.isconnected():
	time.sleep(1)

count = 0
adc = machine.ADC(0)
signal = 0
lst = []
url = "http://139.59.13.34/data/add"
headers = {"Content-type":"application/json"}
start = time.ticks_ms()
while True:
	signal = adc.read()
	if signal > 550:
		count = count + 1
	if time.ticks_ms() - start > 15000:
		if count < 12:
			count = 13
		if count > 23:
			count = 23
		break
	time.sleep_ms(1000)

rep = requests.post(url = url, headers = headers, json = {"data": count * 4})
machine.reset()