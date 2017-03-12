
import RPi.GPIO as GPIO
import time
from datetime import datetime

class KlikAanKlikUit():

    PERIODUSEC = 0.000250
    PIN = 4

    VENSTERBANK = 0000
    SCHEMERLAMP = 0001
    HOEKLAMP = 0002

    def __init__(self, address):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT, initial=GPIO.LOW)
        self.address = address

    def lampOn(self, unit):
        for i in range(5):
            self._sendStartPulse()
            self._sendAddress(self.address)
            self._sendBit(0)
            self._sendBit(1)
            self._sendUnit(unit)
            self._sendStopPulse()


    def lampOff(self, unit):
        for i in range(5):
            self._sendStartPulse()
            self._sendAddress(self.address)
            self._sendBit(0)
            self._sendBit(0)
            self._sendUnit(unit)
            self._sendStopPulse()

    def _sendStartPulse(self):
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(self.PERIODUSEC)
        GPIO.output(self.PIN, GPIO.LOW)
        time.sleep(self.PERIODUSEC*10.5)

    def _sendStopPulse(self):
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(self.PERIODUSEC)
        GPIO.output(self.PIN, GPIO.LOW)
        time.sleep(self.PERIODUSEC*40)

    def _sendAddress(self, address):
        for i in reversed(range(26)):
            self._sendBit((address >> i) & 1)

    def _sendUnit(self, unit):
        for i in range(4):
            self._sendBit(unit & (1 << (3-i)))

    def _sendBit(self, isOne):
        if isOne:
            GPIO.output(self.PIN, GPIO.HIGH)
            time.sleep(self.PERIODUSEC)
            GPIO.output(self.PIN, GPIO.LOW)
            time.sleep(self.PERIODUSEC*5)
            GPIO.output(self.PIN, GPIO.HIGH)
            time.sleep(self.PERIODUSEC)
            GPIO.output(self.PIN, GPIO.LOW)
            time.sleep(self.PERIODUSEC)
        else:
            GPIO.output(self.PIN, GPIO.HIGH)
            time.sleep(self.PERIODUSEC)
            GPIO.output(self.PIN, GPIO.LOW)
            time.sleep(self.PERIODUSEC)
            GPIO.output(self.PIN, GPIO.HIGH)
            time.sleep(self.PERIODUSEC)
            GPIO.output(self.PIN, GPIO.LOW)
            time.sleep(self.PERIODUSEC*5)

    def cleanup(self):
        GPIO.cleanup(self.PIN)


if __name__ == "__main__":
    k = KlikAanKlikUit(0b01011011000111101001110010)
    print "lamp On"
    #for i in range(2^4-1):
    for i in [ k.SCHEMERLAMP, k.HOEKLAMP, k.VENSTERBANK]:
        for j in range(5):
            k.lampOn(i)
        time.sleep(1)

    for i in [k.SCHEMERLAMP, k.HOEKLAMP, k.VENSTERBANK]:
        for j in range(5):
            k.lampOff(i)
        time.sleep(1)


        #k.lampOn(k.SCHEMERLAMP)

    print "lamp on complete"
    k.cleanup()

