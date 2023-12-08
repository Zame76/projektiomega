from time import sleep
import RPi.GPIO as GPIO, sqlite3, time, datetime

while True:
	connection = sqlite3.connect('/home/omega/PythonKoodit/projektiomega/db/omega.db')#avataan yhteys omega.db tietokantaan
	test = datetime.datetime.today().timetuple()
	x = datetime.datetime.now()
	t = x.strftime("%Y-%m-%d"+'%')#aika ilmoitetaan muodossa vuosi-kuukausi-päivä
	h = x.strftime("%H")
	print("Time:", t)
	print(h)

	configlista = []
	pricelista = []
	cursor = connection.cursor()
	cursor.execute("SELECT * from ConfigValues")
	rows = cursor.fetchall()
	for row in rows:
		configlista = [row]
	print("timetuple ", test)
	print("minutes ", test[4])
	print("hours ", test[3])
	print("Min hinta ", configlista[0][2])
	print("Max hinta ", configlista[0][3])

	cursor = connection.cursor()
	cursor.execute("SELECT * from ElectricityPrices WHERE PriceDate like ? AND DateHour=?",(t,h))
	rivit = cursor.fetchall()
	for rivi in rivit:
		pricelista = [rivi]

	print("Hinta nyt ", pricelista[0][3])
	connection.close()#suljetaan yhteys

#asetetaan pinnit ledeille
	LED_RED = 16
	LED_YELLOW = 24
	LED_GREEN = 23

#pinnit asetetaan output moodiin
	GPIO.setmode(GPIO.BCM)

	print("CTRL + C to quit")

	if configlista[0][2] > pricelista[0][3]:
		GPIO.setup(LED_RED, GPIO.OUT)
		hintapinni = LED_GREEN
	
	elif configlista[0][3] < pricelista[0][3]:
		GPIO.setup(LED_GREEN, GPIO.OUT)
		hintapinni = LED_RED
	
	else:
		GPIO.setup(LED_YELLOW, GPIO.OUT)
		hintapinni = LED_YELLOW
	laskuri = 0
	try:
#looppi, jossa ledit ovat valaistuneena sekunnin ajan, jonka jälkeen ledi sammuu ja seuraava syttyy
		while laskuri < 30:

			GPIO.output(hintapinni, GPIO.HIGH)
			sleep(1)
			GPIO.output(hintapinni, GPIO.LOW)
			sleep(3)
			laskuri += 1
		
	finally:
		GPIO.cleanup()
