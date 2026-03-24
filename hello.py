#print
print("Hello")
# var
a = 123
b = 54534
c = a + b
print(c)
print(type(c))
print(type("Hello"))
print(type(3.14))

import decimal

getcontext().prec = 20

print(Decimal(10)/Decimal(7))

print(10/7)

print(Decimal(10)/7)

print(10/Decimal(7))

import *

frac1 = Fraction(10,30)
frac2 = Fraction(13,23)

print(frac1 + frac2)

c = complex(1,7)
print(c)
print(c.real)
print(c.imag)


c=10//3
print(c)

c=10**3
print(c)