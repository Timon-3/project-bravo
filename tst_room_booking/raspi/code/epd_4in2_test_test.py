#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import qrcode # pip install qrcode[pil]
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2
import time
import locale
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime, date

logging.basicConfig(level=logging.DEBUG)

#positioning and size variables
calendar_size=[300,200]
calendar_pos=[10,80]
calendar_rows=13
weekdays=["Mo","Di","Mi","Do","Fr","Sa","So"]
calender_col=len(weekdays)+1
dt=datetime.now()
weekday_today=dt.isoweekday()
ROOM_STATE=["Frei","Besetzt"]

qr_code_text="Hier könnte Ihre Werbung stehen"

start_time=6

cal_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), int(calendar_size[1]/20))
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)

try:
    logging.info("Roomreservation")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()



    
    # Creates new screen
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    
    # Add Date
    draw.text((10, 0), weekdays[weekday_today-1] +" "+ str(dt.strftime('%d.%m.%Y')), font = font24, fill = 0)

    # Add Room-State
    draw.text((180, 0), ROOM_STATE[0], font = font34, fill = 0)

    # Create and add QR Code
    qr_img=qrcode.make(qr_code_text)
    type(qr_img)
    qr_img.save("test-url.png")
    im = Image.open("test-url.png")
    im = im.resize((90,90))
    Himage.paste(im, (320,-5))


    
    
    #Kalender Modul
    
    draw.text((10, 30), 'Kalender', font = font24, fill = 0)
    
    draw.rectangle((calendar_pos[0], calendar_pos[1], calendar_size[0]+calendar_pos[0], calendar_size[1]+calendar_pos[1]), outline = 0) # Rahmen
    
    for i in range(calender_col):
        
        if i>0:
            # Write Weekday text
            draw.text((calendar_pos[0]+calendar_size[0]/calender_col/2.5+calendar_size[0]/calender_col*i, calendar_pos[1]), weekdays[i-1], font = cal_font) 
            # Calendar vertical lines
            draw.line((calendar_pos[0]+calendar_size[0]/calender_col*i, calendar_pos[1], calendar_pos[0]+calendar_size[0]/calender_col*i, calendar_size[1]+calendar_pos[1]))

    
    # Calendar horizontal lines and time
    for i in range (calendar_rows):
        draw.line((calendar_pos[0], calendar_size[1]/calendar_rows*i+calendar_pos[1], calendar_size[0]+calendar_pos[0], calendar_size[1]/calendar_rows*i+calendar_pos[1]))
        # Write time text
        if i>0:
            draw.text((calendar_pos[0]+calendar_size[0]/calender_col/4, calendar_pos[1]+calendar_size[1]/calendar_rows*i), str(i+start_time-1)+":00", font = cal_font)
        if i+start_time == 13:
            draw.rectangle((calendar_pos[0], calendar_size[1]/calendar_rows*i+calendar_pos[1], calendar_size[0]+calendar_pos[0], calendar_size[1]/calendar_rows*(i+1)+calendar_pos[1]), outline = 0)
        
    
    logging.info("Fill eInk Screen")
    # Send all the stuff to the eInk Screen
    epd.display(epd.getbuffer(Himage))
    

    
    if(0):
        print("Support for partial refresh, but the refresh effect is not good, but it is not recommended")
        print("Local refresh is off by default and is not recommended.")
 
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
