import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

D = b*b - 4*a*c

segment_length = math.hypot(dx, dy)
result = 0.0

if D < 0:
    if x1*x1 + y1*y1 <= R*R and x2*x2 + y2*y2 <= R*R:
        result = segment_length
    else:
        result = 0.0
else:
    sqrtD = math.sqrt(D)
    t1 = (-b - sqrtD) / (2*a)
    t2 = (-b + sqrtD) / (2*a)

    left = max(0.0, min(t1, t2))
    right = min(1.0, max(t1, t2))

    if right < 0 or left > 1:
        if x1*x1 + y1*y1 <= R*R and x2*x2 + y2*y2 <= R*R:
            result = segment_length
        else:
            result = 0.0
    else:
        overlap = max(0.0, right - left)
        result = overlap * segment_length

print(f"{result:.10f}")