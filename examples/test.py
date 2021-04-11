#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from sensor import HTU21D


logging.basicConfig(level=logging.DEBUG)

htu21d = HTU21D(1, 0x40)


try:
    logging.info("epd2in9 V2 Demo")
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
        humid = round(humid.RH)
        humidity = str(humid)
        humidity = "Humidity : " + humidity + " %"

        temp = htu21d.temperature()
        C, F, K = temp
        C = round(C, 2)
        temperature = str(C)
        temperature = "Temperature : " + temperature + " C"

        Time = "Time : " + time.strftime('%H:%M:%S')
        time_draw.rectangle((0, 0, 128, 296), fill=255)
        time_draw.text((10, 10), 'Hello Mushrooms', font=font24, fill=0)
        time_draw.text((10, 30), Time, font=font24, fill=0)
        time_draw.text((10, 50), temperature, font=font24, fill=0)
        time_draw.text((10, 70), humidity, font=font24, fill=0)
        
        
        
        
        newimage = time_image.crop([0, 0, 128, 296])
        time_image.paste(newimage, (10, 10))
        epd.display_Partial(epd.getbuffer(time_image))

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
