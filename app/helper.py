import datetime

def test():
    print("Hello from helper.py")

def format_date(api_date):
    #'2019-03-28'
    date_list = list(map(int, api_date.split('-')))
    new_date = datetime.date(date_list[0], date_list[1], date_list[2])
    return(new_date)

def format_time(api_time):
    #'1:05PM'
    period = api_time[-2:]
    time_list = list(map(int, api_time[:-2].split(':')))
    if period == 'PM' and time_list[0] != 12:
        time_list[0] += 12
    new_time = datetime.time(time_list[0], time_list[1])
    return new_time