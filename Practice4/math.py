import math

def degree_to_radian(degree):
    return degree * (math.pi / 180)

def trapezoid_area(height, base1, base2):
    return ((base1 + base2) / 2) * height

def regular_polygon_area(n, s):
    return (n * (s ** 2)) / (4 * math.tan(math.pi / n))

def parallelogram_area(base, height):
    return base * height


print("Write a Python program to convert degree to radian.")
degree = float(input())
print(degree_to_radian(degree))

print("Write a Python program to calculate the area of a trapezoid.")
height = float(input())
base1 = float(input())
base2 = float(input())
print(trapezoid_area(height, base1, base2))

print("Write a Python program to calculate the area of regular polygon.")
n = int(input())
s = float(input())
print(regular_polygon_area(n, s))

print("Write a Python program to calculate the area of a parallelogram.")
base = float(input())
height = float(input())
print(parallelogram_area(base, height))