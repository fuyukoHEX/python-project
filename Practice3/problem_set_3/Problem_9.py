class Circle():
    def __init__(self, r):
        self.r = r
    def area(self):
        pi = 3.14159
        ans = pi * self.r * self.r
        print(f"{ans:.2f}")

obj = Circle(float(input()))
obj.area()