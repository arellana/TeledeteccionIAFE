#Grafica los planos XY, XZ e YZ de la intensidad medida sobre cada eje mediante los datos levantados con el progama "magneto.py", así como el angulo azimutal en función del numero de medicion. Realiza la corrección de cada eje y vuelve a graficar los planos y azimut.
#El angulo azimut está desplazado para medir como una brujula convencional en el intervalo [0°,360°) en vez del pre-set [-pi/2, pi/2] en radianes.

import numpy as np
import matplotlib.pyplot as plt
from magneto import magneto

name = magneto(True)
datos = np.loadtxt(name, delimiter=';')

x, y, z = datos[:,0], datos[:,1], datos[:,2] 

plt.plot(x, y, 'ob', label = 'Plano xy')
plt.plot(x, z, 'or', label = 'Plano xz')
plt.plot(y, z, 'og', label = 'Plano yz')
plt.title('Medicion sin calibrar')
plt.legend()
plt.show()

n = len(datos[:,0])

azimut_bef, azimut2_bef = np.zeros(n), np.zeros(n)


for i in range(n):
    azimut_bef[i] = np.rad2deg(np.arctan2(y[i], x[i]))
    azimut2_bef[i] = np.rad2deg(np.arctan2(x[i], y[i]))

for i in range(n):
    if azimut_bef[i] < 0:
        azimut_bef[i] = azimut_bef[i] + 360

for i in range(n):
    if azimut2_bef[i] < 0:
        azimut2_bef[i] = azimut2_bef[i] + 360


eje = np.linspace(0,n,n)





n = len(datos[:,0])

x_m = np.sum(x)/n
y_m = np.sum(y)/n
z_m = np.sum(z)/n
print('xm: ', x_m)
print('ym: ', y_m)
print('zm: ', z_m)
x_c, y_c, z_c = np.zeros(n), np.zeros(n), np.zeros(n)
azimut, azimut2 = np.zeros(n), np.zeros(n)

for i in range(n):
    x_c[i] = x[i] - x_m 
    y_c[i] = y[i] - y_m
    z_c[i] = z[i] - z_m

for i in range(n):
    azimut[i] = np.rad2deg(np.arctan2(y_c[i], x_c[i]))
    azimut2[i] = np.rad2deg(np.arctan2(x_c[i], y_c[i]))

for i in range(n):
    if azimut[i] < 0:
        azimut[i] = azimut[i] + 360

for i in range(n):
    if azimut2[i] < 0:
        azimut2[i] = azimut2[i] + 360


plt.plot(x_c, y_c, 'ob', label = 'Plano xy')
plt.plot(x_c, z_c, 'or', label = 'Plano xz')
plt.plot(y_c, z_c, 'og', label = 'Plano yz')
plt.title('Medicion calibrada')
plt.legend()
plt.show()


eje = np.linspace(0,n,n)

plt.plot(eje, azimut_bef, 'or', label = 'azimut')
#plt.plot(eje, azimut2_bef, 'ob', label = 'azimut2')
plt.title('Azimut dado por el plano XY')
plt.legend()
plt.show()



plt.plot(eje, azimut, 'darkorange', label = 'Medicion calibrada')
plt.plot(eje, azimut_bef, 'blue', label = 'Medicion sin calibrar')
plt.style.use('ggplot')
plt.xlim(0,2000)
plt.xlabel('Pasos')
plt.ylabel('Angulus (deg)')
plt.legend()
plt.show()


