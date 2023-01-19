#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import qrcode # pip install qrcode[pil]
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
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

from eink_tools import *
from eink_module import *

logging.basicConfig(level=logging.DEBUG)


#Nonsense

# positioning and size variables
timebox_size=[100,180]
timebox_pos=[300,90]
timebox_start=6
timebox_end=19
timebox_length=timebox_end-timebox_start+1


#Next Meeting variables
next_meet_size=[300,200]
next_meet_pos=[20,60]
next_meet_length=2

# Testdata (pls change)
next_meet_arr=[{"name": "Stefano Berta","date":"19.01.2023","starttime":"09:30","endtime":"11:15","descr":"Keine Beschreibung"},{"name":"Timon Frey","date":"19.01.2023","starttime":"11:45","endtime":"14:45","descr":"After Action Review"},{"name":"Thomas Marti","date":"19.01.2023","starttime":"15:00","endtime":"17:00","descr":"Tom Tom"}]
qr_code_text="Admin Passwort: 12346"
room_inventory={"chair": 10,"table": 20,"beamer": 1,"video": True,"wifi": True,"ethernet": True}


# other variables
weekdays=["Mo","Di","Mi","Do","Fr","Sa","So"]

dt=datetime.now()
weekday_today=dt.isoweekday()
ROOM_STATE=["Frei","Besetzt"]




font10 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 10)
cal_font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), int(timebox_size[1]/20))
meeting_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), int(next_meet_size[1]/10))
meeting_desc_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Regular.ttf'), int(next_meet_size[1]/11))
date_font = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), 23)
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
    draw.text((10, 0), weekdays[weekday_today-1] +", "+ str(dt.strftime('%d.%m.%Y')), font = date_font, fill = 0)
    #Himage.paste(centre_text((200,100),weekdays[weekday_today-1] +", "+ str(dt.strftime('%d.%m.%Y')),date_font))
    #centre_image()
    # Add Room-State
    draw.text((180, 0), room_state(next_meet_arr), font = font34, fill = 0)

    # Add QR-Code
    Himage.paste(add_qrcode(qr_code_text), (315,0))

    # Roominfo
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
    Himage.paste(show_time_module(timebox_size,next_meet_arr,timebox_length,timebox_start),timebox_pos)

    """ timedot_pos=float(dt.strftime('%H'))+1/60*float(dt.strftime('%M'))-timebox_start
    # Time with  horizontal lines
    for i in range (timebox_length):
        draw.text((timebox_pos[0], timebox_pos[1]+timebox_size[1]/timebox_length*i-(timebox_length/2)), str(i+timebox_start).zfill(2)+":00", font = cal_font)
        
        draw.line((timebox_pos[0]+timebox_size[0]/timebox_length*3.5, timebox_pos[1]+timebox_size[1]/timebox_length*i, timebox_size[0]+timebox_pos[0], timebox_pos[1]+timebox_size[1]/timebox_length*i))
    
    # Add Events to Timemodule
    for meeting in next_meet_arr:
        starttime_float=float(meeting["starttime"][:2])+1/60*float(meeting["starttime"][-2:])
        endtime_float=float(meeting["endtime"][:2])+1/60*float(meeting["endtime"][-2:])
        draw.rounded_rectangle((timebox_pos[0]+timebox_size[0]/3.5,timebox_pos[1]+timebox_size[1]/timebox_length*(starttime_float-timebox_start),timebox_pos[0]+timebox_size[0]/10*9,timebox_pos[1]+timebox_size[1]/timebox_length*(endtime_float-timebox_start)),outline = 1, fill = 0,radius=5) 
        #for meeting_details in meeting:

    # The NOW-Point
    draw.line(((timebox_pos[0]+timebox_size[0]/timebox_length*3.5), (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos),(timebox_pos[0]+timebox_size[0]*0.75+1), (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos)),width = 3,fill=1)
    draw.line(((timebox_pos[0]+timebox_size[0]/timebox_length*3.5), (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos),(timebox_pos[0]+timebox_size[0]*0.75), (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos)),width = 1)
    draw.ellipse(((timebox_pos[0]+timebox_size[0]/timebox_length*3.5)-3, (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos)-3,(timebox_pos[0]+timebox_size[0]/timebox_length*3.5)+3, (timebox_pos[1]+timebox_size[1]/timebox_length*timedot_pos)+3),outline = 1, fill = 0)
     """

    #Himage.paste(add_icon(os.path.join(picdir,"rd.png"),400), (0,0))
    logging.info("Fill eInk Screen")
    draw.text((225, 290), "Zuletzt Aktualisiert:"+ str(dt.strftime('%d.%m.%Y-%H:%M')), font = font10)
    # Send all the stuff to the eInk Screen
    #Himage.show()
    epd.display(epd.getbuffer(Himage))
    #epd.display_4Gray(epd.getbuffer_4Gray(Himage)) # for Grayscales
    

    
    if(0):
        print("Support for partial refresh, but the refresh effect is not good, but it is not recommended")
        print("Local refresh is off by default and is not recommended.")

    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
