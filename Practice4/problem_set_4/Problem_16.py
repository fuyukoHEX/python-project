def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def get_utc_seconds(s):
    y = int(s[0:4])
    m = int(s[5:7])
    d = int(s[8:10])
    h = int(s[11:13])
    minute = int(s[14:16])
    sec = int(s[17:19])
    sign = s[23]
    th = int(s[24:26])
    tm = int(s[27:29])

    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    total_days = 0
    for i in range(1970, y):
        if is_leap(i):
            total_days += 366
        else:
            total_days += 365

    for i in range(1, m):
        if i == 2 and is_leap(y):
            total_days += 29
        else:
            total_days += days_in_month[i]

    total_days += (d - 1)

    total_sec = total_days * 86400 + h * 3600 + minute * 60 + sec

    offset = th * 3600 + tm * 60
    if sign == '+':
        total_sec -= offset
    else:
        total_sec += offset

    return total_sec

line1 = input()
line2 = input()

t1 = get_utc_seconds(line1)
t2 = get_utc_seconds(line2)

print(t2 - t1)