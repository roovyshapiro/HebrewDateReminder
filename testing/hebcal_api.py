##https://www.hebcal.com/home/219/hebrew-date-converter-rest-api
##
##To convert from Gregorian to Hebrew date use this URL format:
##
##https://www.hebcal.com/converter/?cfg=json&gy=2011&gm=6&gd=2&g2h=1
##
##gy=2011 – Gregorian year
##gm=6 – Gregorian month (1=January, 12=December)
##gd=2 – Gregorian day of month
##g2h=1 – Convert from Gregorian to Hebrew date
##gs=on – After sunset on Gregorian date
##cfg=json – output format is JSON (cfg=json) or XML (cfg=xml)
##To convert from Hebrew to Gregorian use this URL format:
##
##https://www.hebcal.com/converter/?cfg=json&hy=5749&hm=Kislev&hd=25&h2g=1
##
##hy=5749 – Hebrew year
##hm=Kislev – Hebrew month (Nisan, Iyyar, Sivan, Tamuz, Av, Elul, Tishrei, Cheshvan, Kislev, Tevet, Shvat, Adar1, Adar2)
##hd=25 – Hebrew day of month
##h2g=1 – Convert from Hebrew to Gregorian date
##cfg=json – output format is JSON (cfg=json) or XML (cfg=xml)
##
##Hebcal instituted a rate limit of 90 requests per 10 seconds

import requests, json

def greg_to_heb(year, month, day):
    '''
    Utilizes HebCal's API to convert gregorian dates to hebrew dates
    '''
    url = f"https://www.hebcal.com/converter/?cfg=json&gy={year}&gm={month}&gd={day}&g2h=1"
    r = requests.get(url)
    print("Status code:", r.status_code)

    data = r.json()
    hebrew_year = data['hy']
    hebrew_month = data['hm']
    hebrew_day = data['hd']

    print(f"{month} {day} {year} converts to {hebrew_month} {hebrew_day} {hebrew_year}.")
    return ''

def heb_to_greg(year, month, day):
    '''
    Utilizes HebCal's API to convert hebrew dates to gregorian dates
    '''
    #Calculates the hebrew date's english equivalent for the next 5 years
    
    for year_increment in range(year, year + 5):
        url = f"https://www.hebcal.com/converter/?cfg=json&hy={year_increment}&hm={month}&hd={day}&h2g=1"
        r = requests.get(url)
        print("Status code:", r.status_code)

        data = r.json()
        secular_year = data['gy']
        secular_month = data['gm']
        secular_day = data['gd']
        print(f"{month} {day} {year_increment} converts to {secular_month} {secular_day} {secular_year}.")
    return ''

print(heb_to_greg(5752, 'Av', 26))
#print(greg_to_heb(1993, 7, 14))
