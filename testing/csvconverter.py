import csv, json
from datetime import datetime
from collections import OrderedDict 

current_time = datetime.now()
dtstamp = current_time.strftime("%Y%m%d") + "T" + current_time.strftime("%H%M%S") + "Z"

cal_intro = ["BEGIN:VCALENDAR",
             "VERSION:2.0",
             "PRODID:-//hebcal.com/NONSGML Hebcal Calendar v6.2//EN",
             "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH",
             "X-LOTUS-CHARSET:UTF-8",
             "X-PUBLISHED-TTL:PT7D",
             "X-WR-CALNAME:Hebcal Diaspora 2019-2023",
             "X-WR-CALDESC:Jewish Holidays from www.hebcal.com"]

vevent_dict = OrderedDict()
vevent_dict = {'BEGIN':'VEVENT',
               'DTSTART;VALUE=DATE':'startdate',
               'DTEND;VALUE=DATE':'enddate',
               'DTSTAMP':'20190325T210030Z',
               'UID':'20170214-menachemshapirosbirthday@shapiro.com',
               'CREATED':'20170707T003707Z',
               'DESCRIPTION':'description',
               'LAST-MODIFIED':'20170707T003707Z',
               'LOCATION': 'location',
               'SEQUENCE':'0',
               'STATUS':'CONFIRMED',
               'SUMMARY':'summary',
               'TRANSP':'OPAQUE',
               }

valarm_dict = OrderedDict()
valarm_dict = {'BEGIN':'VALARM',
               'ACTION':'EMAIL',
               'DESCRIPTION':'This is an event reminder',
               'SUMMARY':'Alarm notification',
               'ATTENDEE':'mailto:roovy.q@gmail.com',
               'TRIGGER':'-P0DT7H10M0S',
               'END':'VALARM',
               }

valarm_dict2 = OrderedDict()              
valarm_dict2 = {'BEGIN':'VALARM',
               'ACTION':'DISPLAY',
               'DESCRIPTION':'This is an event reminder',
               'TRIGGER':'-P0DT0H10M0S',
               'END':'VALARM',
               }


    
with open('test.txt', 'a') as f:
    for line in cal_intro:
        f.write(line)
        f.write('\n')

with open('dates.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        vevent_dict['DTSTART;VALUE=DATE'] = "{}{}{}".format(row['Year'], row['Month'], row['Day'])
        vevent_dict['DTEND;VALUE=DATE'] = "{}{}{}{}".format(row['Year'], row['Month'],0,int(row['Day']) + 1)
        vevent_dict['DTSTAMP'] = dtstamp
        vevent_dict['CREATED'] = dtstamp
        vevent_dict['LAST-MODIFIED'] = dtstamp
        if row['Occasion'] == 'Birthday':
            vevent_dict['SUMMARY'] = "{} {}'s Birthday".format(row['First Name'], row['Last Name'])
            vevent_dict['DESCRIPTION'] = "Happy Birthday {} {}!".format(row['First Name'], row['Last Name'])
        elif row['Occasion'] == 'Passing':
            vevent_dict['SUMMARY'] = "We remember {} {}'s Passing".format(row['First Name'], row['Last Name'])
            vevent_dict['DESCRIPTION'] = "{} {}'s Neshama should have an Aliyah!".format(row['First Name'], row['Last Name'])
        elif row['Occasion'] == 'Anniversary':
            vevent_dict['SUMMARY'] = "{} {}'s Anniversary".format(row['First Name'], row['Last Name'])
            vevent_dict['DESCRIPTION'] = "Happy Anniversary to Mr. and Mr.s {} {}!".format(row['First Name'], row['Last Name'])
            
##        print(row['First Name'])
##        print(row['Last Name'])
##        print(row['Month'])
##        print(row['Day'])
##        print(row['Year'])
##        print(row['Occasion'])
      
        with open('test.txt', 'a') as f:
            for k in vevent_dict.keys():
                f.write("{}:{}".format(k, vevent_dict[k]))
                f.write('\n')
                
