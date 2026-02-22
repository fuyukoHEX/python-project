import sys
from datetime import datetime

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def parse_datetime(line):
    date_part, tz_part = line.strip().split()
    tz_offset = tz_part[3:]
    iso_str = f"{date_part}T00:00:00{tz_offset}"
    return datetime.fromisoformat(iso_str)

if __name__ == '__main__':
    lines = [line.strip() for line in sys.stdin if line.strip()]
    
    if len(lines) >= 2:
        bday_dt_orig = parse_datetime(lines[0])
        curr_dt = parse_datetime(lines[1])
        
        bday_tz = bday_dt_orig.tzinfo
        b_month = bday_dt_orig.month
        b_day = bday_dt_orig.day
        
        base_year = curr_dt.year
        min_delta_secs = float('inf')
        
        for y in (base_year - 1, base_year, base_year + 1):
            c_month, c_day = b_month, b_day
            
            if b_month == 2 and b_day == 29 and not is_leap(y):
                c_month, c_day = 2, 28
                
            cand_dt = datetime(y, c_month, c_day, 0, 0, 0, tzinfo=bday_tz)
            
            delta = cand_dt - curr_dt
            secs = int(delta.total_seconds())
            
            if 0 <= secs < min_delta_secs:
                min_delta_secs = secs
                
        days_left = (int(min_delta_secs) + 86399) // 86400
        
        print(days_left)