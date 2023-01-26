# Here are all the functions, to simplify the eInk Design process
import qrcode # pip install qrcode[pil]
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
import os
import json
from urllib.request import urlopen

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
datadir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')

name="name"
starttime="start_time"
endtime="end_time"
description="description"
format = "%Y-%m-%d %H:%M"
format_date="%Y-%m-%d"


# Import from JSON
def json_to_dict(room_name):
    #with urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=google") as url:
    with open(os.path.join(datadir,'reservations.json'), encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data[room_name]

# Creates Icons in e defined size
def add_icon(icon_img,size=35):
    ic_im = Image.open(icon_img)
    ic_im = ic_im.resize((size,size))
    return ic_im



# Create and add QR Code
def add_qrcode(qr_code_text,size=90):
    qr_img=qrcode.make(qr_code_text)
    qr_img = qr_img.resize((size,size),resample=5)
    return qr_img

# Check busy status
def room_state(meetings_dict,datetime_now=datetime.now()):
    room_state = "Frei"
    for meetings in meetings_dict:
        meeting_start_time = datetime.strptime(meetings[starttime], format)
        meeting_end_time = datetime.strptime(meetings[endtime], format)
        if datetime_now > meeting_start_time and datetime_now < meeting_end_time:
            room_state="Besetzt"
    return room_state

# Check busy status old
# def room_state(meetings_dict,datetime_now=datetime.now()):
#     room_state = "Frei"
#     date_now=datetime_now.strftime("%d.%m.%Y")
#     time_now=datetime_now.strftime("%H:%M")
#     format = "%Y-%m-%d %H:%M"
#     for meetings in meetings_dict:
#         meeting_start_time = datetime.strptime(meetings[starttime], format)
#         meeting_end_time = datetime.strptime(meetings[endtime], format)
#         if meetings[starttime][-5:]==date_now:
#             if time_now > meetings[starttime][-5:] and time_now < meetings[endtime][-5:]:
#                 room_state="Besetzt"
#     return room_state

# Creates a overview of the next meetings
def show_next_meetings(next_meet_arr,next_meet_size,next_meet_length,dt=datetime.now()):
    meeting_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), int(next_meet_size[1]/10))
    meeting_desc_font= ImageFont.truetype(os.path.join(fontdir, 'Roboto-Regular.ttf'), int(next_meet_size[1]/11))
    meeting_icon_size=25

    next_meet_arr=sorted(next_meet_arr, key=lambda item: item.get(starttime)) # Sort mext_meet_arr by starttime

    image=Image.new('1',next_meet_size, 255)
    draw = ImageDraw.Draw(image)
    next_meet_length=min(next_meet_length,len(next_meet_arr))
    date_now=dt.strftime("%Y-%m-%d")

    if next_meet_length >=1:
        desc=""
        for i in range (next_meet_length):
            image.paste(add_icon(os.path.join(picdir,"person.png"),meeting_icon_size), (0,int(next_meet_size[1]/next_meet_length)*i))
            image.paste(add_icon(os.path.join(picdir,"duration.png"),meeting_icon_size), (0,int(next_meet_size[1]/next_meet_length)*i+meeting_icon_size))
            draw.text((meeting_icon_size, (next_meet_size[1]/next_meet_length)*i+meeting_icon_size/6), next_meet_arr[i][name], font = meeting_font)
            meeting_date=""
            next_meeting_date=next_meet_arr[i][starttime][:next_meet_arr[i][starttime].index(" ")]
            if date_now<next_meeting_date:meeting_date=next_meeting_date[-2:]+"."+next_meeting_date[-5:-3]+"."+next_meeting_date[:4]+" - "
            draw.text((meeting_icon_size, (next_meet_size[1]/next_meet_length)*i+meeting_icon_size+meeting_icon_size/6),meeting_date+next_meet_arr[i][starttime][-5:]+"-"+next_meet_arr[i][endtime][-5:], font = meeting_font)
            if len(next_meet_arr[i][description])>=30: desc=next_meet_arr[i][description][0:28]+"..."
            else: desc=next_meet_arr[i][description]
            draw.text((0, (next_meet_size[1]/next_meet_length)*i+2*meeting_icon_size), desc, font = meeting_desc_font)
    else:
        draw.text((0,0),"Heute sind keine Meetings geplant", font = meeting_desc_font)
    return image

# Searches for the next (max x) meetings
def find_next_meetings(meetings_list,datetime_now=datetime.now()):
    next_meetings_list=[]
    date_now=datetime_now.date()

    for meetings in meetings_list:
        meeting_end=datetime.strptime(meetings[endtime],format)
        if datetime_now <= meeting_end:
            next_meetings_list.append(meetings)
    return next_meetings_list

# # Searches for the next (max x) meetings old
# def find_next_meetings(meetings_list,datetime_now=datetime.now()):
#     date_now=datetime_now.strftime("%d.%m.%Y")
#     time_now=datetime_now.strftime("%H:%M")
#     format = "%Y-%m-%d %H:%M"
#     next_meetings_list=[]
#     for meetings in meetings_list:
#         if meetings[starttime][-5:]==date_now:
#             if time_now < meetings[endtime]:
#                 next_meetings_list.append(meetings)
#     return next_meetings_list

# Timemodule
def show_time_module(meet_arr,timebox_size,timebox_length,timebox_start,dt=datetime.now()):
    todays_meetings=find_next_meetings(meet_arr,dt.replace(hour=1))
    cal_font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), int(timebox_size[1]/20))
    offset=timebox_length/2 
    image=Image.new('1',timebox_size, 255)
    draw = ImageDraw.Draw(image)
    timedot_pos=float(dt.strftime('%H'))+1/60*float(dt.strftime('%M'))-timebox_start
    date_now=dt.strftime("%Y-%m-%d")

    # Time with horizontal lines
    for i in range (timebox_length):
        draw.text((0,timebox_size[1]/timebox_length*i), str(i+timebox_start).zfill(2)+":00", font = cal_font)
        
        draw.line((timebox_size[0]/timebox_length*3.5, timebox_size[1]/timebox_length*i+offset, timebox_size[0], timebox_size[1]/timebox_length*i+offset))
    
    # Add Events to Timemodule
    for meeting in todays_meetings:
        if date_now<meeting[starttime][:meeting[starttime].index(" ")]:
            continue
        meeting_starttime=meeting[starttime][-5:]
        meeting_endtime=meeting[endtime][-5:]
        starttime_float=float(meeting_starttime[:2])+1/60*float(meeting_starttime[-2:])
        endtime_float=float(meeting_endtime[:2])+1/60*float(meeting_endtime[-2:])
        draw.rounded_rectangle((timebox_size[0]/3.5,timebox_size[1]/timebox_length*(starttime_float-timebox_start)+offset,timebox_size[0]/10*9,timebox_size[1]/timebox_length*(endtime_float-timebox_start)+offset),outline = 1, fill = 0,radius=5) 
        #for meeting_details in meeting:

    # The NOW-Pointer
    draw.line(((timebox_size[0]/timebox_length*3.5), (timebox_size[1]/timebox_length*timedot_pos)+offset,(timebox_size[0]*0.75+1), (timebox_size[1]/timebox_length*timedot_pos)+offset),width = 3,fill=1)
    draw.line(((timebox_size[0]/timebox_length*3.5), (timebox_size[1]/timebox_length*timedot_pos)+offset,(timebox_size[0]*0.75), (timebox_size[1]/timebox_length*timedot_pos)+offset),width = 1)
    draw.ellipse(((timebox_size[0]/timebox_length*3.5)-3, (timebox_size[1]/timebox_length*timedot_pos)-3+offset,(timebox_size[0]/timebox_length*3.5)+3, (timebox_size[1]/timebox_length*timedot_pos)+3+offset),outline = 1, fill = 0)

    return image

    
def centre_image(size,message="",font=""):
    W, H = size
    image = Image.new('1', size, 255)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font)
    return 2
def centre_text(size,message="",font=""):
    W, H = size
    image = Image.new('1', size, 255)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font)
    return image