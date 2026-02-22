import sys
from datetime import datetime, timezone, timedelta

def parse_line(line):
    date_part, tz_part = line.strip().split()
    
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    
    sign_char = tz_part[3]
    sign = 1 if sign_char == '+' else -1
    
    offset_str = tz_part[4:]
    hours, minutes = map(int, offset_str.split(':'))
    
    offset = timedelta(hours=sign * hours, minutes=sign * minutes)
    tz = timezone(offset)
    
    dt = dt.replace(tzinfo=tz)
    return dt.astimezone(timezone.utc)

line1 = sys.stdin.readline()
line2 = sys.stdin.readline()

if line1 and line2:
    dt1 = parse_line(line1)
    dt2 = parse_line(line2)

    delta = abs(dt1 - dt2)
    print(delta.days)