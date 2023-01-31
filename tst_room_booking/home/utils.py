from datetime import datetime, timedelta
from home.models import Event

def formatevent(starttime, endtime, description):
    timediff = (endtime.hour - starttime.hour) + ((endtime.minute - starttime.minute)/60)
    min = (starttime.minute)
    height = timediff * 100 + timediff//1*7
    top = (height - 100) / 2 + min/0.6
    return f"""<div style='font-weight: bold; color: rgb(224 224 234); position: relative; top: {top}%; height: {height}%; width: 100%;
            background-color:rgb(64 104 137);border-radius:6px;background-image: linear-gradient(to bottom right, rgb(64 104 137),
            rgb(124 164 207));box-shadow: 1px 4px lightgrey;'>{description}</div>"""

def formatrow(week, hour, room_id, minimum_date, maximum_date, hidden_description):
    events = Event.objects.filter(start_time__hour=hour, room=room_id, start_time__gt=minimum_date, start_time__lt=maximum_date)
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

def formatcal(room_id, cal_date, hidden_description):
    now = datetime.strptime(cal_date,"%Y-%d-%m")
    monday = now - timedelta(days = now.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    friday = monday + timedelta(days=4)
    saturday = monday + timedelta(days=5)
    sunday = monday + timedelta(days=6)
    minimum_date = monday - timedelta(days=1)
    maximum_date = sunday + timedelta(days=1)
    weekdatetime = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
    week = [monday.day,tuesday.day,wednesday.day,thursday.day,friday.day,saturday.day,sunday.day]
    cal = f'<table border="1" width="100%" height="500">'
    cal += "<tr><td style='width: 5%;'></td><td>Montag</td><td>Dienstag</td><td>Mittwoch</td><td>Donnerstag</td><td>Freitag</td><td>Samstag</td><td>Sonntag</td></tr>"
    line2 = "<td style='width: 5%;'></td>"
    for day in weekdatetime:
        line2 += f'<td>{day.day}.{day.month}</td>'
    cal += f'<tr>{line2}</tr>'
    for x in range(7,19,1):
        cal += f'{formatrow(week=week, hour=x, room_id=room_id, minimum_date=minimum_date, maximum_date=maximum_date, hidden_description=hidden_description)}'
    cal += f'</table>'
    return cal