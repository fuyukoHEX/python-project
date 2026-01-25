def count_letter(text, char):
    count = 0
    text = text.lower()
    for current_char in text:
        if current_char == char:
            count += 1
    return count

input_text = str(input())
target_char = input()

print(count_letter(input_text, target_char))

