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


logging.basicConfig(level=logging.DEBUG)


htu21d = HTU21D(1, 0x40)

humid = htu21d.humidity()
humid = round(humid.RH)
humidity = str(humid)
humidity = "Humidity : " + humidity + " %"

temp = htu21d.temperature()
C, F, K = temp
C = round(C, 2)
temperature = str(C)
temperature = "Temperature : " + temperature + " C"

try:
    logging.info("epd2in9 V2 Demo")
    epd = epd2in9_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # # Drawing on the Horizontal image
    # logging.info("1.Drawing on the Horizontal image...")
    # Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'Hello Mushrooms', font = font24, fill = 0)
    # draw.text((10, 20), temperature, font=font24, fill=0)
    # draw.text((10, 40), humidity, font=font24, fill=0)
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)

    # partial update
    logging.info("5.show time")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.display_Base(epd.getbuffer(time_image))
    num = 0
    while (True):
        draw = ImageDraw.Draw(Himage)
        time_draw.rectangle((10, 10, 120, 50), fill=255)
        time_draw((10, 0), 'Hello Mushrooms', font=font24, fill=0)
        time_draw((10, 20), temperature, font=font24, fill=0)
        time_draw((10, 40), humidity, font=font24, fill=0)
        time_draw.text((10, 60), time.strftime(
            '%H:%M:%S'), font=font24, fill=0)
        newimage = time_image.crop([10, 10, 120, 50])
        time_image.paste(newimage, (10, 10))
        epd.display_Partial(epd.getbuffer(time_image))

        num = num + 1
        if(num == 10):
            break

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
