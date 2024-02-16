from datetime import datetime
from pytz import timezone

month_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

def getToday():
    today = datetime.now(timezone('US/Eastern'))
    return today

def getDayOfWeek():
    dayOfWeek = getToday().strftime('%A')[:2]
    return dayOfWeek

def getMonth():
    month = month_dict[getToday().month]
    return month

def getDate():
    day = getToday().day
    return day

def getYear():
    year = getToday().year
    return year

def getHour():
    hour = getToday().hour
    return hour

def getMinute():
    minute = getToday().minute
    return minute