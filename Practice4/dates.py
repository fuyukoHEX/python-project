import datetime

def subtract_five_days():
    return datetime.date.today() - datetime.timedelta(days=5)

def yesterday_today_tomorrow():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    return yesterday, today, tomorrow

def drop_microseconds():
    return datetime.datetime.now().replace(microsecond=0)

def date_diff_in_seconds(date1_str, date2_str):
    date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
    return abs((date2 - date1).total_seconds())


print("Write a Python program to subtract five days from current date.")
print(subtract_five_days())

print("Write a Python program to print yesterday, today, tomorrow.")
yesterday, today, tomorrow = yesterday_today_tomorrow()
print(yesterday)
print(today)
print(tomorrow)

print("Write a Python program to drop microseconds from datetime.")
print(drop_microseconds())

print("Write a Python program to calculate two date difference in seconds.")
date1_input = input()
date2_input = input()
print(date_diff_in_seconds(date1_input, date2_input))