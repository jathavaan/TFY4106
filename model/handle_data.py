import numpy as np
from matplotlib import pyplot as plt

import calculations as cal

file = open("data.txt", "r")  # Åpnar fila

x_e = []
y_e = []  # Lagar tomme lister
t_e = []
v_e = []

count = 0
for line in file:  # For-løkke som går gjennom fila, linje for linje
    row = line.split()  # Splittar kvar linje inn i dei tre kolonnene

    if count > 1:
        t_e.append(float(row[0]))
        x_e.append(float(row[1]))  # Gjer om tekst til tal og legg dette
        y_e.append(float(row[2]))  # til i dei forskjellige listene
        try:
            v_e.append(float(row[3]))
        except Exception:
            pass

    count = count + 1

file.close()  # Lukkar fila!

print(t_e)
print(x_e)
print(y_e)

# Numerisk derivasjon

x_e = np.array(x_e)
y_e = np.array(y_e)
t_e = np.array(t_e)
v_e = np.array(v_e)

dy_e = np.zeros(len(x_e) - 2)

for i in range(len(dy_e)):
    dy_e[i] = (y_e[i + 2] - y_e[i]) / (x_e[i + 2] - x_e[i])

d2y_e = np.zeros(len(x_e) - 4)

for i in range(len(d2y_e)):
    d2y_e[i] = (dy_e[i + 2] - dy_e[i]) / (x_e[i + 3] - x_e[i + 1])

# Merk: De deriverte har nå to færre elementer! De mangler den første og siste verdien
# For å bruke disse i beregninger må vi derfor slice arraysene.

# baneformen hastighet (funk av x og t), akselelerasjon, krumning, f/N grafen plottet mot x

# Baneform med hensyn på x
plt.plot(x_e, y_e)
plt.title("Baneform")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.show()

# Hastighet med hensyn på x
plt.plot(x_e, v_e)
plt.title("Hastighet mhp. x")
plt.xlabel("x [m]")
plt.ylabel("v [m/s]")
plt.show()

# Hastighet med hensyn på t
plt.plot(t_e, v_e)
plt.title("Hastighet mhp. tid")
plt.xlabel("t [s]")
plt.ylabel("v [m/s]")
plt.show()

# Akselerasjon
a_e = []
for dx in dy_e:
    beta = np.arctan(dx)
    a_e.append(cal.acceleration(beta))

plt.plot(x_e[1:-1], a_e)
plt.title("Akselerasjon")
plt.xlabel("x [m]")
plt.ylabel("a [m/s^2]")
plt.show()

# f/N med hensyn på x
dy_e = dy_e[1:-1]
y_e = y_e[2:-2]
y_0 = y_e[0]

f_over_N = []
dy_lst = []
d2y_lst = []

for i in range(len(d2y_e)):
    dy = dy_e[i]
    d2y = d2y_e[i]
    beta = np.arctan(dy)
    y_1 = y_e[i]

    f_over_N.append(cal.friction(beta) / cal.normal_force(beta, y_0, y_1, dy, d2y))

plt.plot(x_e[2:-2], f_over_N)
plt.title("Friksjon over normalkraft")
plt.xlabel("x [m]")
plt.ylabel("f/N []")
plt.show()


