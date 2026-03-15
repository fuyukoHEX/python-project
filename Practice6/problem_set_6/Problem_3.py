n = int(input())
words = input()

array = []
for index, word in enumerate(words):
    array.append(f"{index}:{word}")

print(" ".join(array))
