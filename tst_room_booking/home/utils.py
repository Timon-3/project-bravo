from datetime import datetime
from home.models import Event

def formatevent(starttime, endtime, description):
    timediff = (endtime.hour - starttime.hour)
    min = (starttime.minute)
    height = timediff * 100
    top = (height - 100) / 2 + min/0.6
    return f"<div style='background-color: red; color: black; position: relative; top: {top}%; height: {height}%; width: 100%;'>{description}</div>"

def formatrow(week, hour):
    events = Event.objects.filter(start_time__hour=hour)
    row = f"<td>{hour}</td>"
    for days in week:
        dayevents = events.filter(start_time__day=days)
        if dayevents.exists():
            starttime = dayevents.first().start_time
            endtime = dayevents.first().end_time
            description = dayevents.first().description
            row += f"<td>{formatevent(starttime=starttime, endtime=endtime,description=description)}</td>"
        else:
            row += f"<td></td>"
    return f"<tr>{row}</tr>"

def formatcal():
    monday = datetime.today().day - datetime.today().weekday()
    week = [monday,monday+1,monday+2,monday+3,monday+4,monday+5,monday+6]
    cal = f'<table border="1" width="1250" height="500">'
    cal += "<tr><td></td><td>Montag</td><td>Dienstag</td><td>Mittwoch</td><td>Donnerstag</td><td>Freitag</td><td>Samstag</td><td>Sonntag</td></tr>"
    line2 = "<td></td>"
    for day in week:
        line2 += f'<td>{day}</td>'
    cal += f'<tr>{line2}</tr>'
    for x in range(7,19,1):
        cal += f'{formatrow(week=week, hour=x)}'
    cal += f'</table>'
    return cal