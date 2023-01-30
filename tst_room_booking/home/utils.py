from datetime import datetime, timedelta
from home.models import Event

def formatevent(starttime, endtime, description):
    timediff = (endtime.hour - starttime.hour) + ((endtime.minute - starttime.minute)/60)
    min = (starttime.minute)
    height = timediff * 100 + timediff//1*7
    top = (height - 100) / 2 + min/0.6
    return f"<div style='background-color: red; color: black; position: relative; top: {top}%; height: {height}%; width: 100%;'>{description}</div>"

<<<<<<< HEAD
def formatrow(week, hour, room_id, monday, sunday):
    events = Event.objects.filter(start_time__hour=hour, room=room_id, start_time__gt=monday, start_time__lt=sunday)
=======
def formatrow(week, hour, room_id, hidden_description):
    events = Event.objects.filter(start_time__hour=hour, room=room_id)
>>>>>>> 563ffe058c8e85bfcb6f73924f050aa14face278
    row = f"<td style='width: 5%;'>{str(hour).zfill(2)}:00</td>"
    for days in week:
        dayevents = events.filter(start_time__day=days)
        if dayevents.exists():
            starttime = dayevents.first().start_time
            endtime = dayevents.first().end_time
            if hidden_description:
                description = "booked"
            else:
                description = dayevents.first().description
            row += f"<td>{formatevent(starttime=starttime, endtime=endtime,description=description)}</td>"
        else:
            row += f"<td></td>"
    return f"<tr>{row}</tr>"

<<<<<<< HEAD
def formatcal(room_id, cal_date):
    now = datetime.strptime(cal_date,"%Y-%d-%m")
    monday = now - timedelta(days = now.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    friday = monday + timedelta(days=4)
    saturday = monday + timedelta(days=5)
    sunday = monday + timedelta(days=6)
    weekdatetime = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
    week = [monday.day,tuesday.day,wednesday.day,thursday.day,friday.day,saturday.day,sunday.day]
=======
def formatcal(room_id, hidden_description):
    monday = datetime.today().day - datetime.today().weekday()
    week = [monday,monday+1,monday+2,monday+3,monday+4,monday+5,monday+6]
>>>>>>> 563ffe058c8e85bfcb6f73924f050aa14face278
    cal = f'<table border="1" width="100%" height="500">'
    cal += "<tr><td style='width: 5%;'></td><td>Montag</td><td>Dienstag</td><td>Mittwoch</td><td>Donnerstag</td><td>Freitag</td><td>Samstag</td><td>Sonntag</td></tr>"
    line2 = "<td style='width: 5%;'></td>"
    for day in weekdatetime:
        line2 += f'<td>{day.day}.{day.month}</td>'
    cal += f'<tr>{line2}</tr>'
    for x in range(7,19,1):
<<<<<<< HEAD
        cal += f'{formatrow(week=week, hour=x, room_id=room_id, monday=monday, sunday=sunday)}'
=======
        cal += f'{formatrow(week=week, hour=x, room_id=room_id, hidden_description=hidden_description)}'
>>>>>>> 563ffe058c8e85bfcb6f73924f050aa14face278
    cal += f'</table>'
    return cal