digit = {
    "ZER": "0","ONE": "1","TWO": "2","THR": "3","FOU": "4","FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}

reversed_key = {}

for key in digit:
    value = digit[key]
    reversed_key[value] = key

def decode(sn):
    number_as_string = ""
    index = 0
    while index < len(sn):
        part_of_number = sn[index: index + 3]
        number_as_string += digit[part_of_number]
        index += 3

        return int(number_as_string)
    
def encode(sn):
    int_to_string = ""
    for digit in str(sn):
        number_string = reversed_key[digit]
        int_to_string += number_string

        return int_to_string
    
word = input().strip()

if "+" in word:
    part = word.split("+")
    operation = "+"
elif "-" in word:
    part = word.split("-")
    operation = "-"
else:
    part = word.split("*")
    operation = "*"

left_side = part[0]
right_side = part[1]
left_side = decode(left_side)
right_side = decode(right_side)
sum = 0

if operation == "+":
    sum = left_side + right_side
elif operation == "-":
    sum = left_side - right_side
else:
    sum = left_side * right_side

print(encode(sum))