# TFY41xx Fysikk vaaren 2021.
#
# Programmet tar utgangspunkt i hoeyden til de 8 festepunktene.
# Deretter beregnes baneformen y(x) ved hjelp av 7 tredjegradspolynomer, 
# et for hvert intervall mellom to festepunkter, slik at baade banen y, 
# dens stigningstall y' = dy/dx og dens andrederiverte
# y'' = d2y/dx2 er kontinuerlige i de 6 indre festepunktene.
# I tillegg velges null krumning (andrederivert) 
# i banens to ytterste festepunkter (med bc_type='natural' nedenfor).
# Dette gir i alt 28 ligninger som fastlegger de 28 koeffisientene
# i de i alt 7 tredjegradspolynomene.

# De ulike banene er satt opp med tanke paa at kula skal 
# (1) fullfoere hele banen selv om den taper noe mekanisk energi underveis;
# (2) rulle rent, uten aa gli ("slure").

# Vi importerer noedvendige biblioteker:
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

import calculations as calc  # Importerer funksjoner fra formelarket
import handle_data as hd

# Horisontal avstand mellom festepunktene er 0.200 m
h = 0.200
xfast = np.asarray([0, h, 2 * h, 3 * h, 4 * h, 5 * h, 6 * h, 7 * h])

# Vi begrenser starthÃ¸yden (og samtidig den maksimale hÃ¸yden) til
# Ã¥ ligge mellom 250 og 300 mm
ymax = 300
# yfast: tabell med 8 heltall mellom 50 og 300 (mm); representerer
# hÃ¸yden i de 8 festepunktene
yfast = np.asarray(np.random.randint(50, ymax, size=8))
# konverter fra m til mm
yfast = yfast / 1000
yfast_konst = np.asarray([0.220, 0.143, 0.102, 0.0676, 0.08704, 0.137, 0.128, 0.05031])
# inttan: tabell med 7 verdier for (yfast[n+1]-yfast[n])/h (n=0..7); dvs
# banens stigningstall beregnet med utgangspunkt i de 8 festepunktene.
inttan = np.diff(yfast) / h
attempts = 1
# while-lÃ¸kken sjekker om en eller flere av de 3 betingelsene ovenfor
# ikke er tilfredsstilt; i sÃ¥ fall velges nye festepunkter inntil
# de 3 betingelsene er oppfylt
while (yfast[0] < yfast[1] * 1.04 or
       yfast[0] < yfast[2] * 1.08 or
       yfast[0] < yfast[3] * 1.12 or
       yfast[0] < yfast[4] * 1.16 or
       yfast[0] < yfast[5] * 1.20 or
       yfast[0] < yfast[6] * 1.24 or
       yfast[0] < yfast[7] * 1.28 or
       yfast[0] < 0.250 or
       np.max(np.abs(inttan)) > 0.4 or
       inttan[0] > -0.2):
    yfast = np.asarray(np.random.randint(0, ymax, size=8))

    # konverter fra m til mm
    yfast = yfast / 1000

    inttan = np.diff(yfast) / h
    attempts = attempts + 1

# Omregning fra mm til m:
# xfast = xfast/1000
# yfast = yfast/1000

# NÃ¥r programmet her har avsluttet while-lÃ¸kka, betyr det at
# tallverdiene i tabellen yfast vil resultere i en tilfredsstillende bane.

# Programmet beregner deretter de 7 tredjegradspolynomene, et
# for hvert intervall mellom to nabofestepunkter.


# Med scipy.interpolate-funksjonen CubicSpline:
cs = CubicSpline(xfast, yfast_konst, bc_type='natural')

xmin = 0.000
xmax = 1.401
dx = 0.001

x = np.arange(xmin, xmax, dx)

# funksjonen arange returnerer verdier paa det "halvaapne" intervallet
# [xmin,xmax), dvs slik at xmin er med mens xmax ikke er med. Her blir
# dermed x[0]=xmin=0.000, x[1]=xmin+1*dx=0.001, ..., x[1400]=xmax-dx=1.400,
# dvs x blir en tabell med 1401 elementer
Nx = len(x)
y = cs(x)  # y=tabell med 1401 verdier for y(x)
dy = cs(x, 1)  # dy=tabell med 1401 verdier for y'(x)
d2y = cs(x, 2)  # d2y=tabell med 1401 verdier for y''(x)

# Eksempel: Plotter banens form y(x)
baneform = plt.figure('y(x)', figsize=(12, 6))
plt.plot(x, y, xfast, yfast_konst, '*')
plt.title('Banens form')
plt.xlabel('$x$ (m)', fontsize=20)
plt.ylabel('$y(x)$ (m)', fontsize=20)
plt.ylim(0.0, 0.40)
plt.grid()
plt.show()
# Figurer kan lagres i det formatet du foretrekker:
# baneform.savefig("baneform.pdf", bbox_inches='tight')
# baneform.savefig("baneform.png", bbox_inches='tight')
# baneform.savefig("baneform.eps", bbox_inches='tight')


print('Antall forsøk', attempts)
print('Festepunkthøyder (m)', yfast_konst)
print('Banens høyeste punkt (m)', np.max(y))


def distance_to_time(x_pos, v_lst):
    t_lst = []
    time = 0

    for i in range(len(x_pos) - 1):
        current_x = x_pos[i]
        next_x = x_pos[i + 1]
        v = v_lst[i + 1]
        dx = next_x - current_x
        t = dx / v
        time += t
        t_lst.append(time)

    return t_lst


curvature_lst = []
speed_lst = []
ca_lst = []
normal_force_lst = []
acceleration_lst = []
friction_lst = []

y_0 = y[0]

for x_pos in x:
    d1y = cs(x_pos, 1)
    d2y = cs(x_pos, 2)
    y_1 = cs(x_pos)

    # Fart
    v_x = calc.speed_x(y_0, cs(x_pos))
    speed_lst.append(v_x)

    # Krumning
    k = calc.curvature(d1y, d2y)
    curvature_lst.append(k)

    # Sentripetalakselerasjon
    ca = calc.centripetal_acceleration(v_x, k)
    ca_lst.append(ca)

    # Beta
    beta = np.arctan(d1y)

    # Normalkraft
    N = calc.normal_force(beta, y_0, y_1, d1y, d2y)
    normal_force_lst.append(N)

    # Akselerasjon
    a = calc.acceleration(beta)
    acceleration_lst.append(a)

    # Friksjon
    f = calc.friction(beta)
    friction_lst.append(f)
"""
plt.plot(x, curvature_lst)
plt.xlabel("x [m]")
plt.ylabel("Krumning")
plt.show()
"""

hd.vel_x()
plt.plot(x, speed_lst, label="Numerisk")
plt.legend()
plt.grid()
plt.show()

"""
plt.plot(x, ca_lst)
plt.xlabel("x[m]")
plt.ylabel("Sentripetalakselerasjon")
plt.show()

plt.plot(x, normal_force_lst)
plt.xlabel("x[m]")
plt.ylabel("Normalkraft")
plt.show()
"""

hd.acceleration()
plt.plot(x, acceleration_lst, label="Numerisk")
plt.legend()
plt.grid()
plt.show()

"""
plt.plot(x, friction_lst)
plt.xlabel("x[m]")
plt.ylabel("Friksjon")
plt.show()
"""

# Plotter fartsgrafen mot tiden
t = distance_to_time(x, speed_lst)

hd.vel_t()
plt.plot(t, speed_lst[1:], label="Numerisk")
plt.legend()
plt.grid()
plt.show()

# Plotter friksjon over normalkraft mhp. posisjonen
f_over_N = []
for i in range(len(friction_lst)):
    f = friction_lst[i]
    N = normal_force_lst[i]
    f_over_N.append(f / N)

hd.friction_over_N()
plt.plot(x, f_over_N, label="Numerisk")
plt.legend()
plt.grid()
plt.show()