#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from sensor import HTU21D
import traceback
import time
from waveshare_epd import epd2in9_V2
import logging
import sys
import os
picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


htu21d = HTU21D(1, 0x40)

humid = htu21d.humidity()
humid = round(humid.RH, 2)
temp = htu21d.temperature()
print(temp)
C, F, K = temp
C = round(C, 2)
print(C)

humidity = str(humid)
temperature = str(C)
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2 Demo")

    epd = epd2in9_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height),
                       255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'Hello Mushrooms', font=font24, fill=0)
    draw.text((10, 20), temperature, font=font24, fill=0)
    draw.text((10, 40), humidity, font=font24, fill=0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in9_V2.epdconfig.module_exit()
    exit()
