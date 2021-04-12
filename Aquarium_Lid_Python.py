#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from lib/waveshare_epd import epd2in9_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from sensor import HTU21D

import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG)

htu21d = HTU21D(1, 0x40)

lightSwitchGPIO = 20
humidifierGPIO = 21
fanGPIO = 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lightSwitch, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(humidifier, GPIO.OUT, initial=GPIO.LOW)



try:
    logging.info("Aquarium Lid Test")
    epd = epd2in9_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # partial update
    logging.info("5.show time")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.display_Base(epd.getbuffer(time_image))
    num = 0
    while (True):
        humid = htu21d.humidity()
        humid = round(humid.RH, 2)
        humidity = str(humid)
        humidity = "Humidity        : " + humidity + " %RH"

        temp = htu21d.temperature()
        C, F, K = temp
        C = round(C, 2)
        temperature = str(C)
        temperature = "Temperature : " + temperature + " C"

        Time = "Time                : " + time.strftime('%H:%M:%S')

        time_draw.rectangle((10, 10, 296, 128), fill=255)
        time_draw.text((10, 10), 'Hello Mushrooms', font=font24, fill=0)
        time_draw.text((10, 40), Time, font=font24, fill=0)
        time_draw.text((10, 60), temperature, font=font24, fill=0)
        time_draw.text((10, 80), humidity, font=font24, fill=0)
        newimage = time_image.crop([10, 10, 296, 128])
        time_image.paste(newimage, (10, 10))
        epd.display_Partial(epd.getbuffer(time_image))

        #  unpack time.localtime tuple into some usable variables and print it out
        year, mon, day, hour, minutes, sec, wday, yday, dst = time.localtime()
        printhourstring = "The current hour is : " + str(hour)
        print(printhourstring)

        # if it is later than 0800, but earlier than 2000 turn the lights on
        if hour > 8 and hour <20:
            GPIO.output(lightSwitchGPIO, GPIO.HIGH)
            print("Lights On")
        # if it is afer 2000 or before 0800 turn the lights off
        if hour >20 or hour <8:
            GPIO.output(lightSwitchGPIO, GPIO.LOW)
            print("Lights Off")
        
        currentHumidityString = "Current humidity is : " + str(humid)
        print(currentHumidityString)

        if humid<90:
            GPIO.output(humidifierGPIO, GPIO.HIGH)
            print("Humidifer On")

        if humid>90:
            GPIO.output(humidifierGPIO, GPIO.LOW)
            print("Humidifer Off")

        if minutes % 5 == 0:
            print("Minutes = " minutes "fan on.")
            GPIO.output(fanGPIO, GPIO.HIGH)
            sleep(30)
            GPIO.output(fanGPIO, GPIO.LOW)

        
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in9_V2.epdconfig.module_exit()
    exit()
