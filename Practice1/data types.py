user_input = input("Enter something: ")

try:
    value = int(user_input)
except ValueError:
    try:
        value = float(user_input)
    except ValueError:
        value = user_input

data_type = type(value)
print(f"Your data type for the number: {data_type}")
