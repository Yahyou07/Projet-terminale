from math import *
s = 0
for i in range (0,4):
    s = s + 1/4 *((i/4)+2)*exp(-i/4)
print(s)