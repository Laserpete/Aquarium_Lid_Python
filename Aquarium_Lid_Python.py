#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'pic')
libdir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from sensor import HTU21D
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG)

htu21d = HTU21D(1, 0x40)

#GPIO pins. These are the broadcom pin numbers, rather than the board physical pin numbers, which are given in the comments here;
FAN_GPIO = 16           # 36
LIGHT_SWITCH_GPIO = 20  # 38
HUMIDIFIER_GPIO = 21    # 40

FAN_MINUTES_MODULO = 5 # run fan for one minute every five minutes, feel free to change this
FAN_PWM_ON_PERCENTAGE = 25
FAN_SECONDS_ON 60

HUMIDITY_THRESHOLD = 85

# Setup GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SWITCH_GPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(HUMIDIFIER_GPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(FAN_GPIO, GPIO.OUT, initial=GPIO.LOW)
PWMFan=GPIO.PWM(FAN_GPIO, 100) # 100 Hz PWM on the fan pin


try:
    logging.info("Aquarium Lid Test")

    # Start the e-Ink display
    epd = epd2in9_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Objects for the fonts
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Set up EDP functions
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.display_Base(epd.getbuffer(time_image))

    while (True):

        # Measure and round humidity
        humid = htu21d.humidity()
        humid = round(humid.RH, 2)

        # Format humidity for display
        humidity = str(humid)
        humidity = "Humidity        : " + humidity + " %RH"

        # Measure and round temperature
        temp = htu21d.temperature()
        C, F, K = temp
        C = round(C, 2)

        # Format temperature for display
        temperature = str(C)
        temperature = "Temperature : " + temperature + " C"

        # Format time for display
        Time = "Time                : " + time.strftime('%H:%M:%S')

        # Display stuff on the screen
        time_draw.rectangle((10, 10, 296, 128), fill=255)
        time_draw.text((10, 10), 'Hello Mushrooms', font=font24, fill=0)
        time_draw.text((10, 40), Time, font=font24, fill=0)
        time_draw.text((10, 60), temperature, font=font24, fill=0)
        time_draw.text((10, 80), humidity, font=font24, fill=0)
        newimage = time_image.crop([10, 10, 296, 128])
        time_image.paste(newimage, (10, 10))
        epd.display_Partial(epd.getbuffer(time_image))

        # Unpack time.localtime tuple into some usable variables
        year, mon, day, hour, minutes, sec, wday, yday, dst = time.localtime()
        # Format hours for display
        printhourstring = "The current hour is : " + str(hour)
        print(printhourstring)

# Time based light control

        # if it is later than 0800, but earlier than 2000 turn the lights on
        if hour > 8 and hour <20:
            GPIO.output(LIGHT_SWITCH_GPIO, GPIO.HIGH)
            print("Lights On")
        # if it is afer 2000 or before 0800 turn the lights off
        if hour >=20 or hour <8:
            GPIO.output(LIGHT_SWITCH_GPIO, GPIO.LOW)
            print("Lights Off")

# Humidity based humidifier control        
        currentHumidityString = "Current humidity is : " + str(humid)
        print(currentHumidityString)

        if humid<HUMIDITY_THRESHOLD:
            GPIO.output(HUMIDIFIER_GPIO, GPIO.HIGH)
            PWMFan.start(FAN_PWM_ON_PERCENTAGE)
            print("Humidifer On")

        if humid>HUMIDITY_THRESHOLD:
            GPIO.output(HUMIDIFIER_GPIO, GPIO.LOW)
            PWMFan.stop()
            print("Humidifer Off")

 Fan control
         if minutes % FAN_MINUTES_MODULO == 0
            print("Minutes = ", minutes, "fan PWM = ", FAN_PWM_ON_PERCENTAGE)
            PWMFan.start(FAN_PWM_ON_PERCENTAGE)
            sleep(FAN_SECONDS_ON)
            PWMFan.stop()
            #GPIO.output(FAN_GPIO, GPIO.HIGH)
        # if minutes % FAN_MINUTES_MODULO != 0 or humid > 90:
        #     print ("Fan off.")
        #     PWMFan.stop()
        #     #GPIO.output(FAN_GPIO, GPIO.LOW)
        
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
