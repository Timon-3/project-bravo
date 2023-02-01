#!/usr/bin/python
# -*- coding:utf-8 -*-


#   Added with 'crontab -e' the script to cron
#   */5 * * * * python3 /home/pi/Desktop/project-bravo/tst_room_booking/raspi/code/eink_control_next.py
#
import sys
import os
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from eink_tools import *

logging.basicConfig(level=logging.INFO)


# positioning and size variables
timebox_size=[100,180]
timebox_pos=[300,90]
timebox_start=7
timebox_end=19
timebox_length=timebox_end-timebox_start+1

#Next Meeting variables
next_meet_size=[300,200]
next_meet_pos=[20,70]
next_meet_length=2

# Testdata (pls change)
room_id="4"
next_meet_arr=json_to_dict()
room_inventory={"chair": 15,"table": 15,"beamer": 2,"video": True,"ethernet": True,"wifi": True}


# other variables
weekdays=["Mo","Di","Mi","Do","Fr","Sa","So"]

dt=datetime.now()
weekday_today=dt.isoweekday()
ROOM_STATE=["Frei","Besetzt"]

# Fonts
font10 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 10)
cal_font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), int(timebox_size[1]/20))
meeting_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), int(next_meet_size[1]/10))
meeting_desc_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Regular.ttf'), int(next_meet_size[1]/11))
title_font = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), 23)
date_font = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Regular.ttf'), 17)
font34 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Black.ttf'), 34)

try:
    logging.info("Roomreservation")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    #epd.Clear()
    
    # Creates new screen
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame # B/W Image
    #Himage = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame  # Image in grayscales (fill = epd.GRAY2)
    draw = ImageDraw.Draw(Himage)
    
    # Add Date
    draw.text((10, 0), "Raum 31.0.09", font = title_font, fill = 0)
    draw.text((10, 25), weekdays[weekday_today-1] +", "+ str(dt.strftime('%d.%m.%Y')), font = date_font, fill = 0)
    #Himage.paste(centre_text((200,100),weekdays[weekday_today-1] +", "+ str(dt.strftime('%d.%m.%Y')),date_font))

    # Add Room-State
    draw.text((190, 0), room_state(next_meet_arr), font = font34, fill = 0)

    # Add QR-Code
    Himage.paste(add_qrcode(), (315,0))

    # Roominfo shows all the Roomsymbols with informations
    counter=0
    for item in room_inventory:
        if room_inventory[item]:
            Himage.paste(add_icon(os.path.join(picdir,item+".png")), (counter*35,273))
            if type(room_inventory[item])!=bool:
                draw.text((counter*35+15,273), str(room_inventory[item]))
            counter+=1

    # Next meetings
    
    Himage.paste(show_next_meetings(find_next_meetings(next_meet_arr),next_meet_size,next_meet_length),next_meet_pos)
    
    # Timemodule
    Himage.paste(show_time_module(next_meet_arr,timebox_size,timebox_length,timebox_start),timebox_pos)

    #Himage.paste(add_icon(os.path.join(picdir,"rd.png"),400), (0,0))
    logging.info("Fill eInk Screen")
    draw.text((225, 290), "Zuletzt Aktualisiert:"+ str(dt.strftime('%d.%m.%Y-%H:%M')), font = font10)

    # Send all the stuff to the eInk Screen
    #Himage.show()
    epd.display(epd.getbuffer(Himage))
    #epd.display_4Gray(epd.getbuffer_4Gray(Himage)) # for Grayscales


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()