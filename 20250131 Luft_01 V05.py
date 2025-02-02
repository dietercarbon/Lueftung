#==========================================================================
#
#  20250131 Luft_01 V05.py
#
#  1 BME680, 1 LDR
#
#  onboard LED:
#  Z47  *  =  WLAN Verbindung erfolgreich hergestellt
#  Z53  **  =  MQTT-Client erfolgreich erstellt
#  Z61  ***  =  "on" ge-publisht
#
#  Z28  MQTT_TOPIC = "Luft_1"
#  Z50  client = MQTTClient("PicoW11", MQTT_BROKER)
#
#==========================================================================
#
# Bibliotheken laden
import machine
import network
from time import sleep
from simple import MQTTClient
from Zugang import wlanSSID, wlanPW, IP_MQTT_broker
from machine import ADC, Pin, I2C
from bme680 import *

# WLAN-Zugangsdaten und MQTT-Broker-Details
WIFI_SSID = wlanSSID()
WIFI_PASSWORD = wlanPW()
MQTT_BROKER = IP_MQTT_broker()
MQTT_TOPIC = "Luft_01"
MQTTClientName = MQTT_TOPIC

# RPi Pico - Pin assignment
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

# Initialisieren des LDR-ADCs  und LED-Anzeige
ldr = ADC(2)
LED = machine.Pin("LED", machine.Pin.OUT)

def LED_blinkt(Zahl):
    for Nummer in range(Zahl):
        LED.value(1);sleep(0.3);LED.value(0);sleep(0.2)
    return 

# Verbindung zum WLAN herstellen
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    sleep(0.1)

Blinki = 1 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
#  *  =  WLAN Verbindung erfolgreich hergestellt

# MQTT-Client erstellen
client = MQTTClient(MQTTClientName, MQTT_BROKER)

Blinki = 2 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
#  **  =  MQTT-Client erfolgreich erstellt


# Hauptprogramm
while True:
    
    try:
        # Temperatur fünfstellig mit Vorzeichen und einer Nachkommastelle, z.B. "+25,4"
        temp = "{:+05.1f}".format(bme.temperature-4).replace(".", ",")

        # Luftfeuchte dreistellig, ggf. mit führenden Nullen, z.B. "098"
        hum = "{:03.0f}".format(bme.humidity)

        # Luftdruck vierstellig, ggf. mit führenden Nullen, z.B. "0850"
        pres = "{:04.0f}".format(bme.pressure)
        
        gas = str(round(bme.gas/1000, 2)) + ' KOhms'

        print('Temperature:', temp, ' C')
        print('Humidity:', hum, ' %')
        print('Pressure:', pres,' hPa')
        print('Gas:', gas)
        print('-------')
    except OSError as e:
        print('Failed to read sensor.')

    
    wert_ldr = ldr.read_u16()
    ldrStr = str(wert_ldr)
    
    sendStr = temp + " " + hum + " " + pres + " " + ldrStr
    #         Temperatur relativeLuftfeuchtigkeit Luftdruck Helligkeit
    #         "+25,4 080 0900 16000"
    #         "012345678901234567890"
    
    client.connect()
    client.publish(MQTT_TOPIC, sendStr)
    
    Blinki = 3 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
    #  ***  =  "on" ge-publisht
    client.disconnect()
    sleep(5)
 
        
