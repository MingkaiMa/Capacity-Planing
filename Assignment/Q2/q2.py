import math

lamda = 15
miu = 3

rou = lamda / miu

s = 4

N = 6

##P0 = 0
##part_1 = 1
##part_2 = 0
##for i in range(1, s + 1):
##    part_2 += rou ** i / math.factorial(i)
##
##part_3 = rou ** s / math.factorial(s)
##
##part_4 = 0
##for i in range(s + 1, N + 1):
##    part_4 += (rou / s) ** (i - s)
##
##
##P0 = (part_1 + part_2 + part_3 * part_4) ** -1
##
##P6 = rou ** 6/ (math.factorial(4) * 4 ** 2) * P0
##


def getP0(rou, s, N):
    part_1 = 1
    part_2 = 0
    for i in range(1, s + 1):
        part_2 += rou ** i / math.factorial(i)

    part_3 = rou ** s / math.factorial(s)
    part_4 = 0
    for i in range(s + 1, N + 1):
        part_4 += (rou / s) ** (i - s)

    P0 = (part_1 + part_2 + part_3 * part_4) ** -1
    return P0


def getPn(rou, n, P0, s):
    if n <= s:
        return rou ** n / math.factorial(n) * P0
    else:
        return rou ** n / (math.factorial(s) * s ** (n - s)) * P0
    



L = [11, 16, 21, 26]

for Nn in L:
    print(Nn)
    P0 = getP0(rou, s, Nn)
    print(f'P0 is: {P0}')
    print(getPn(rou, Nn, P0, s))
##    


##Wq = 0
##part_11 = 1 / (4 * miu * (1 - P6))
##part_22 = 0
##
##for i in range(s, N):
##    part_22 += getPn(rou, i, P0, s) * (i - s + 1)
##
##Wq = part_11 * part_22
    

##lamda = 15
##miu = 3
##c = 4
##
##rou = lamda / (miu * c)
##
##N = 6
##def getP0(c, rou, N):
##    part_1 = 0
##
##    for n in range(c):
##        part_1 += (c ** n / math.factorial(n) * rou ** n)
##
##    part_2 = 0
##    part_2 = c ** c / math.factorial(c)
##
##    part_2 *= ((rou ** c - rou ** (N + 1)) / (1 - rou))
##
##    return (part_1 + part_2) ** -1
##
##
##
##def getPn(n, c, rou, N):
##    
##    P0 = getP0(c, rou, N)
####    print(P0)
##    if n < c:
##        return c ** n / math.factorial(n) * rou ** n * P0
##
##    else:
##        return c ** c / math.factorial(c) * rou ** n * P0
##    
##
##
##def Lq(c, rou, N):
##    res = 0
##    for n in range(c + 1, N + 1):
##        Pn = getPn(n, c, rou, N)
##        print(n, Pn)
##        res += (n - c) * Pn
##
##    return res
