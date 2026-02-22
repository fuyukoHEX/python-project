import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

def dist(x, y):
    return math.hypot(x, y)

OA = dist(x1, y1)
OB = dist(x2, y2)

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

D = b*b - 4*a*c

intersects = False
if a != 0 and D >= 0:
    sqrtD = math.sqrt(D)
    t1 = (-b - sqrtD) / (2*a)
    t2 = (-b + sqrtD) / (2*a)
    if (0 <= t1 <= 1) or (0 <= t2 <= 1):
        intersects = True

if not intersects:
    result = math.hypot(dx, dy)
else:
    AT = math.sqrt(OA*OA - R*R)
    BT = math.sqrt(OB*OB - R*R)

    dot = x1*x2 + y1*y2
    
    cos_theta = max(-1.0, min(1.0, dot / (OA*OB)))
    theta = math.acos(cos_theta)

    alpha = math.acos(R / OA)
    beta = math.acos(R / OB)

    phi = theta - alpha - beta

    arc = R * phi

    result = AT + BT + arc

print(f"{result:.10f}")