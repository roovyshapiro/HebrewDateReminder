##https://www.hebcal.com/home/219/hebrew-date-converter-rest-api
##
##To convert from Gregorian to Hebrew date use this URL format:
##https://www.hebcal.com/converter/?cfg=json&gy=2011&gm=6&gd=2&g2h=1
##
##gy=2011 – Gregorian year
##gm=6 – Gregorian month (1=January, 12=December)
##gd=2 – Gregorian day of month
##g2h=1 – Convert from Gregorian to Hebrew date
##gs=on – After sunset on Gregorian date
##cfg=json – output format is JSON (cfg=json) or XML (cfg=xml)

##To convert from Hebrew to Gregorian use this URL format:
##https://www.hebcal.com/converter/?cfg=json&hy=5749&hm=Kislev&hd=25&h2g=1
##
##hy=5749 – Hebrew year
##hm=Kislev – Hebrew month (Nisan, Iyyar, Sivan, Tamuz, Av, Elul, Tishrei, Cheshvan, Kislev, Tevet, Shvat, Adar1, Adar2)
##hd=25 – Hebrew day of month
##h2g=1 – Convert from Hebrew to Gregorian date
##cfg=json – output format is JSON (cfg=json) or XML (cfg=xml)
##
##Hebcal instituted a rate limit of 90 requests per 10 seconds

import csv, json, requests, time
from datetime import datetime
from collections import OrderedDict 

def greg_to_heb(year, month, day):
    '''
    Utilizes HebCal's API to convert gregorian dates to hebrew dates
    
    >>>print(heb_to_greg(5752, 'Av', 26))
    Sample JSON Response:
    {'gy': 1996, 'gm': 8, 'gd': 11,
     'hy': 5752, 'hm': 'Av','hd': 26,
     'hebrew': 'כ״ו בְּאָב תשנ״ו', 'events': ['Parashat Shoftim']}    
    '''
    
    url = f"https://www.hebcal.com/converter/?cfg=json&gy={year}&gm={month}&gd={day}&g2h=1"
    r = requests.get(url)
    #print("Status code:", r.status_code)

    data = r.json()
    heb_year = data['hy']
    heb_month = data['hm']
    heb_day = data['hd']
    
    return heb_year, heb_month, heb_day

def heb_to_greg(year, month, day):
    '''
    Utilizes HebCal's API to convert hebrew dates to gregorian dates
    
    >>>print(greg_to_heb(1993, 7, 14))
    Sample JSON response:
    {'gy': 1993, 'gm': 7, 'gd': 14,
    'hy': 5753, 'hm': 'Tamuz', 'hd': 25,
    'hebrew': 'כ״ה בְּתַמּוּז תשנ״ג', 'events': ['Parashat Matot-Masei']}
    '''
    
    url = f"https://www.hebcal.com/converter/?cfg=json&hy={year}&hm={month}&hd={day}&h2g=1"
    r = requests.get(url)
    #print("Status code:", r.status_code)

    data = r.json()
    secular_year = data['gy']
    secular_month = data['gm']
    secular_day = data['gd']
    #print(f"{month} {day} {year} converts to {secular_month} {secular_day} {secular_year}.")
    return secular_year, secular_month, secular_day

def heb_greg_csv(csv_file):
    '''
    Takes a csv file of hebrew dates and generates a csv file
    with those dates convereted into secular dates.
    It does this for the following three years from the current date.
    The hebrew csv file must be in the following format:

    First Name,Last Name,Month,Day,Year,Occasion
    Menachem,Schneerson,Nisan,11,5662,Birthday

    Occasion may be Birthday, Anniversary or Passing
    Hebrew month must be any of the following:
    Nisan, Iyyar, Sivan, Tamuz, Av, Elul, Tishrei, Cheshvan, Kislev, Tevet, Shvat, Adar1, Adar2)
    '''
    #Get the current secular date and then convert it to it's hebrew equivalent.
    #today = ['2019', '04', '09']
    today = (datetime.today().strftime('%Y,%m,%d'))
    today = today.split(',')
    current_heb_year, current_heb_month, current_heb_day = greg_to_heb(today[0],today[1],today[2])
    
    #Write the header which is used by generate_ics()
    with open('secular_dates.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['First Name','Last Name','Month','Day','Year','Occasion'])

    #Convert each hebrew date to its secular equivalent for the next three years
    #and write it to 'secular_dates.csv'
    with open(csv_file) as f:
        csv_reader = csv.reader(f)
        #example_data = list(csv_reader)
        next(csv_reader)
        num_requests = 0
        for row in csv_reader:
            for num in range(3):
                #Hebcal has a rate limit of 90 requests per 10 seconds.
                #If the amount of requests get too high, the user will need to wait 10 seconds.
                if num_requests == 80:
                    print('High volume of requests!')
                    print('Must wait 10 seconds before continuing!')
                    for x in range(1, 11):
                        print(str(x) + '0% complete.')
                        time.sleep(1)
                    print('Thank you for waiting. Program will now continue.\n')
                    num_requests = 0
                else:
                    secular_year, secular_month, secular_day = heb_to_greg(str(int(current_heb_year) + num), row[2], row[3])
                    num_requests += 1
                    with open('secular_dates.csv', 'a', newline='') as f:
                        csv_writer = csv.writer(f)
                        csv_writer.writerow([row[0],row[1],secular_month,secular_day,secular_year,row[5]])
    #We can now run generate_ics() to convert the csv into an ics file.
    generate_ics()
    return ''

def generate_ics():
    '''
    Reads 'secular_dates.csv', a file generated by heb_greg_csv with secular dates.
    Generates an ics file.
    Adds one email reminder for a week before the date and
    one email reminder the day before.
    '''
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

    #Write the calendar header header
    with open('HebrewDateCalendar.ics', 'a') as f:
        for line in cal_intro:
            f.write(line)
            f.write('\n')

    ##Read the rows in secular_dates.csv and replace the valarm and vevent values for each csv row
    ##The fields of secular_dates.csv follow this convention:
    ##row['First Name']
    ##row['Last Name']
    ##row['Month']    -> two digit such as '04' or '12'
    ##row['Day']      -> two digit such as '05' or '15'
    ##row['Year']     -> four digits such as '2019'
    ##row['Occasion'] -> 'Birthday', 'Passing', or 'Anniversary'
    with open('secular_dates.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        row_num = 0
        for row in csv_reader:
            row_num += 1
            #Dates can't be single digits without a preceeding '0'
            #TODO - what if a day is the 31st? The next will be the 32nd.
            #Need to use datetime to correctly increase day by 1.
            if len(row['Month']) == 1:
                row['Month'] = str(0) + str(row['Month'])
            if len(row['Day']) == 1:
                row['Day'] = str(0) + str(row['Day'])
                next_day = str(0) + str(int(row['Day']) + 1)
            elif len(row['Day']) == 2:
                next_day = str(int(row['Day']) + 1)
                                   
            vevent_dict['DTSTART;VALUE=DATE'] = "{}{}{}".format(row['Year'], row['Month'], row['Day'])
            vevent_dict['DTEND;VALUE=DATE'] = "{}{}{}".format(row['Year'], row['Month'],next_day)

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
            #configures an email alert one week prior to the event at 8pm.
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
    return ''

heb_greg_csv('hebrew_dates.csv')
