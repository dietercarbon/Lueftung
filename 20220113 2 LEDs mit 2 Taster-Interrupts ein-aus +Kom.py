#==============================================================================================
#Ein-/Aus-Schalten von 2 LEDs aufgrund von Interrupts von 2 Tastern.
#
#Zweck: zeigt Komponenten der Interrupt-Steuerung (zur Weiterverwendung)
#==============================================================================================
#Importieren der benötigten Bibliotheken
#==============================================================================================
#Modul "machine" zur
#  * GPIO Ausgabe-Steuerung an die LEDs,
#  * GPIO Eingabe-Steuerung durch die Taster,
#  * Konfiguration der Interrupts.

import machine
#Modul "utime" zum Einbau von Verzögerungen.
import utime

#==============================================================================================
#Definieren bzw. Vorbelegen der Default-Werte
#==============================================================================================
#Default-Werte für die Taster-Variablen; "0" bedeutet ausgeschaltet, nicht gedrückt.
#Da diese Variablen zur Wert-Übergabe aus den Interrupt-Unterprogrammen genutzt werden,
#müssen sie in den Interrupt-Unterprogrammen als globale Variablen definiert werden.

taster1=0
taster2=0

#==============================================================================================
#Definieren der zu benutzenden GPIO-Pins
#==============================================================================================
#Objekt-Definition der Klasse "Pin" mit Variablen-Namen (hier "LEDx") zur Bestimmung
#  * welcher GPIO-Pin soll benutzt werden (hier GPIO "15" +"14"), und
#  * wie soll er benutzt werden (hier "Pin.OUT"), also zur Ausgabe (hier an LEDs).
#ALSO hier: LEDs an GP15 und GP14 werden zur Anzeige benutzt werden.

LED1 = machine.Pin(15, machine.Pin.OUT)
LED2 = machine.Pin(14, machine.Pin.OUT)

#Objekt-Definition der Klasse "Pin" mit Variablen-Namen (hier "Tasterxan") zur Bestimmung
#  * welcher GPIO-Pin soll benutzt werden (hier GPIO "16" +"17"), und
#  * wie soll er benutzt werden (hier "Pin.IN"), also zur Eingabe (hier durch Taster).
#  * ob "0 Volt" oder "3,3 Volt" am GPIO erwartet werden.
#    (hier: 3,3 Volt), daher hat der leerlaufende Eingang 0 Volt, was "PULL_DOWN" entspricht).
#ALSO hier: Taster an GP16 und GP17 werden zur Eingabe benutzt werden.

Taster1an = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
Taster2an = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)

#==============================================================================================
#Definieren der zu benutzenden UNTERPROGRAMME
#==============================================================================================
#Definition der (hier 2) Interrupt-Unterprogramme, welche durch  Interrupt aufgerufen werden.
#Der gewählte Name beschreibt, dass das Unterprogramm durch Drücken des Tasters gestartet wird.
#Nach Durchlauf des Unterprogramms springt der Programmlauf wieder zurück an diejenige Stelle
#im Hauptprogramm, an der die Unterbrechung erfolgte und "macht" dort weiter.
#ALSO hier: wenn der Taster gedrückt wird,
#           * wird die Variable "tasterx" von 0 auf 1 bzw. von 1 auf 0 geschaltet, und
#           * wartet das Programm eine Zehntelsekunde zur Vermeidung von Taster-Prellungen.

def tast1prog(p):
    #Variablen (hier "taster1" + "taster2"), die zur Kommunikation mit dem Hauptprogramm genutzt
    #werden, müssen "global" (also in allen Programmteilen gültig und nutzbar) definiert werden.
    global taster1
    if taster1 == 1:
        taster1 = 0
        utime.sleep(0.1)
    elif taster1 == 0:
        taster1 = 1
        utime.sleep(0.1)

def tast2prog(p):
    global taster2
    if taster2 == 1:
        taster2 = 0
        utime.sleep(0.1)
    elif taster2 == 0:
        taster2 = 1
        utime.sleep(0.1)

#==============================================================================================
#Definieren des Interupt-Triggers (= Auslöser)
#==============================================================================================
#"Taster1/2an" sind erwartete GPIO-Eingänge, welche hier
#  * zum Trigger eines Interrupts definiert werden,
#  * einen Anstieg (= steigende Flanke) "RISING" also "0" auf "1" erwarten, und
#  * im Eintritts-Fall die Unterprogramme "tast1/2prog" aufrufen.

Taster1an.irq(trigger = machine.Pin.IRQ_RISING, handler = tast1prog)
Taster2an.irq(trigger = machine.Pin.IRQ_RISING, handler = tast2prog)

#==============================================================================================
# HAUPTPROGRAMM * HAUPTPROGRAMM * HAUPTPROGRAMM * HAUPTPROGRAMM * HAUPTPROGRAMM
#==============================================================================================
#Die Endlos-Schleife schaltet die jewelige LED aufgrind des Wertes der Variablen
#"tasterx" ein und aus.

while True:
    if taster1 == 1:
        LED1.value(1)
    elif taster1 == 0:
        LED1.value(0)
    if taster2 == 1:
        LED2.value(1)
    elif taster2 == 0:
        LED2.value(0)

#==============================================================================================
# Ende HAUPTPROGRAMM * Ende HAUPTPROGRAMM * Ende HAUPTPROGRAMM * Ende HAUPTPROGRAMM * Ende  
#==============================================================================================
