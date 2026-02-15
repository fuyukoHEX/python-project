import math

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        print(f"({self.x}, {self.y})")
    def dist(self, other_point_x, other_point_y):
        l =math.sqrt((other_point_x - self.x)**2 + (other_point_y- self.y)**2)
        print(f"{l:.2f}")


init_coord = list(map(int, input().split()))
final_coord = list(map(int, input().split()))
sec_coord = list(map(int, input().split()))


p1 = Point(init_coord[0], init_coord[1])
p1.show()
p1.move(final_coord[0], final_coord[1])
p1.dist(sec_coord[0], sec_coord[1])