#!/usr/bin/python3
#
# Testing green access to green containers
#
import requests
import sys

serverip = "18.222.236.224"
billport = ":8080"
weightport = ":8081"

urlhttp = "http://"
urlcmd = ''
urladr = ''

truckname = 'trucktest'
truckid = ''
truckrishouy = '12345678'

global response
funcret = ''

def funcseturl():
	urladr1 = urlhttp + serverip + billport + urlcmd
	return urladr1

def funcget():
	urladr = funcseturl()
	global response
	try:
		response = requests.get(urladr)
		print(response.status_code, end = '')
		funcret1 = response.status_code
		if response.status_code == 200:
			print (' OK')
		else:
			print (' ',response.headers)
	except:
		print ('ERR : ',sys.exc_info()[0])
		funcret1 = '999'
	return funcret1

def funcpost():
	urladr = funcseturl()
	global response
	try:
		response = requests.post(urladr)
		print(response.status_code, end = '')
		funcret1 = response.status_code
		if response.status_code == 200:
			print (' OK')
		elif response.status_code == 430:
			print (' OK')
		else:
			print (' ',response.headers)
	except:
		print ('ERR : ',sys.exc_info()[0])
		funcret1 = '999'
	return funcret1

def funcput():
	urladr = funcseturl()
	global response
	try:
		response = requests.put(urladr)
		print(response.status_code, end = '')
		funcret1 = response.status_code
		if response.status_code == 200:
			print (' OK')
		else:
			print (' ',response.headers)
	except:
		print ('ERR : ',sys.exc_info()[0])
		funcret1 = '999'
	return funcret1




print('Provider Health : ', end = '')				# stay on the line
urlcmd = '/health'									# test health
err = funcget()

print('Provider Name : ', end = '')
urlcmd = '/provider/trucktest'
if funcpost() != 200:
	quit()
truckstr = str(response.text)
truckid = truckstr[2:7]
print('truckid: ',truckid)
print('Provider Change Name :', end = '')
urlcmd = '/provider/'+truckid+'/trucktestnew'
err = funcput()

print('Provider Get Rates :', end = '')
urlcmd = '/rates'
err = funcget()

print('Provider Post Rates : ', end = '')
urlcmd = '/rates'
err = funcpost()

print('Provider Post Truck : ', end = '')
urlcmd = '/truck/124456/'+truckid
err = funcpost()

print('Provider Put Truck : ', end = '')
urlcmd = '/truck/123456/'+truckid
err = funcput()

print('Provider Get Truck : ', end = '')
urlcmd = '/truck/123456'
err = funcget()

print('Provider Get Bill : ', end = '')
urlcmd = '/bill/'+truckid
err = funcget()





#GET http://18.222.236.224:8080/health	: return status 200, text: Payment team is OK

#POST .../provider/<name> (ex: ../bruno)	: return status 200, json: ID of the provider, ex: {"10003": "bruno"}

#PUT .../provider/<ID>/<name>	ex:.../10003/bruno3	: return status 200, text: 
#								Update provider name by id:10003. New name is: bruno3

#GET .../rates							: return status 200, text lines:
#product_id,rate,scope
#Navel,93,All
#Blood,112,All
#Mandarin,104,All
#Shamuti,84,All
#Tangerine,92,All
#Clementine,113,All
#Grapefruit,88,All
#Valencia,87,All
#Mandarin,102,10001
#Mandarin,120,10002
#Tangerine,85,10005
#Valencia,90,3

#POST .../rates						: return status 200, text: Rates Are Up To Date

#POST .../truck/<trucknum>/<ID>	ex : .../12345678/10001	: OK

#GET .../truck/<trucknum>/<ID>		: return ERR 500

#GET .../bill/<ID>				: return status 200, json
#			{
 #   "id": "10002",
 #   "name": "bruno2",
 #   "from": "None",
 #   "to": "None",
 #   "truckCount": "0",
 #   "sessionCount": "0",
 #   "products": [],
 #   "total": "0"
#}

