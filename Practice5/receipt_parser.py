import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

price_pattern = re.compile(r'\d{1,3}(?: \d{3})*,\d{2}')
all_prices = price_pattern.findall(text)

item_pattern = re.compile(
    r'\d+\.\n(.+?)\n\d+,\d{3} x',
    re.DOTALL
)

items = [item.strip().replace('\n', ' ') for item in item_pattern.findall(text)]

total_pattern = re.compile(r'ИТОГО:\n([\d ]+,\d{2})')
total_match = total_pattern.search(text)
total_sum = total_match.group(1) if total_match else None

datetime_pattern = re.compile(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})')
datetime_match = datetime_pattern.search(text)
datetime_value = datetime_match.group(1) if datetime_match else None

payment_pattern = re.compile(r'(Банковская карта|Наличные):')
payment_match = payment_pattern.search(text)
payment_method = payment_match.group(1) if payment_match else None

data = {
    "items": items,
    "total_sum": total_sum,
    "payment_method": payment_method,
    "datetime": datetime_value
}

print(json.dumps(data, ensure_ascii=False, indent=4))