##The fields of dates.csv follow this convention:
##row['First Name']
##row['Last Name']
##row['Month']    -> two digit such as '04' or '12'
##row['Day']      -> two digit such as '05' or '15'
##row['Year']     -> four digits such as '2019'
##row['Occasion'] -> 'Birthday', 'Passing', or 'Anniversary'

import csv, json
from datetime import datetime
from collections import OrderedDict 

users_email = "roovyshapiro@gmail.com"
current_time = datetime.now()
#converts current time into a usable format for DTSTAMP eg, 20190325T210030Z
dtstamp = current_time.strftime("%Y%m%d") + "T" + current_time.strftime("%H%M%S") + "Z"

#ics header - this will only be printed once.
cal_intro = ["BEGIN:VCALENDAR",
             "VERSION:2.0",
             "PRODID:-//RoovyShapiro/NONSGML HebrewDateReminder//EN",
             "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH",
             "X-LOTUS-CHARSET:UTF-8",
             "X-PUBLISHED-TTL:PT7D",
             "X-WR-CALNAME:Hebrew Date Calendar",
             "X-WR-CALDESC:Hebrew Date Calendar by Roovy Shapiro"]

#the values of vevent_dict are rewritten for each event
vevent_dict = OrderedDict()
vevent_dict = {'BEGIN':'VEVENT',
               'DTSTART;VALUE=DATE':'startdate',
               'DTEND;VALUE=DATE':'enddate',
               'DTSTAMP':'dtstamp',
               'UID':'users_email',
               'CREATED':'dtsampt',
               'DESCRIPTION':'description',
               'LAST-MODIFIED':'dtstamp',
               'LOCATION': 'location',
               'SEQUENCE':'0',
               'STATUS':'CONFIRMED',
               'SUMMARY':'summary',
               'TRANSP':'OPAQUE',
               }

#the values for the email notification are rewritten for each event
valarm_dict = OrderedDict()
valarm_dict = {'BEGIN':'VALARM',
               'ACTION':'EMAIL',
               'DESCRIPTION':'description',
               'SUMMARY':'summary',
               'ATTENDEE':'users_email',
               'TRIGGER':'-P0DT7H10M0S',
               'END':'VALARM',
               }

#Write the calendar header
with open('HebrewDateCalendar.ics', 'a') as f:
    for line in cal_intro:
        f.write(line)
        f.write('\n')

#Read the rows in dates.csv and replace the valarm and vevent values for each csv row
with open('dates.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    row_num = 0
    for row in csv_reader:
        row_num += 1
        vevent_dict['DTSTART;VALUE=DATE'] = "{}{}{}".format(row['Year'], row['Month'], row['Day'])
        if row['Day'].startswith('0'):
            vevent_dict['DTEND;VALUE=DATE'] = "{}{}{}{}".format(row['Year'], row['Month'],'0',int(row['Day']) + 1)
        else:
            vevent_dict['DTEND;VALUE=DATE'] = "{}{}{}".format(row['Year'], row['Month'],int(row['Day']) + 1)

        vevent_dict['DTSTAMP'] = dtstamp
        vevent_dict['UID'] = str(row_num) + f"-{users_email}"
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

        valarm_dict['DESCRIPTION'] = vevent_dict['DESCRIPTION']
        valarm_dict['SUMMARY'] = vevent_dict['SUMMARY']
        valarm_dict['ATTENDEE'] = f'mailto:{users_email}'
        #sends an email alert one week prior to the event at 8pm.
        valarm_dict['TRIGGER'] = "-P6DT4H0M0S"

        #Once the values have been overwritten, they are appended to the ics file.
        with open('HebrewDateCalendar.ics', 'a') as f:
            for k in vevent_dict.keys():
                f.write("{}:{}".format(k, vevent_dict[k]))
                f.write('\n')
            #Two alarms are created - one for a week in advance, and the other for a day in advance.
            for i in range(2):
                for k in valarm_dict.keys():
                    f.write("{}:{}".format(k, valarm_dict[k]))
                    f.write('\n')
                #sends a second email alert on the day before the event at 8pm.
                valarm_dict['TRIGGER'] = "-P0DT4H0M0S"
            f.write('END:VEVENT\n')

#closing tag of the ics is appended to the end of the file              
with open('HebrewDateCalendar.ics', 'a') as f:
    f.write('END:VCALENDAR')
