from ModeloRecortado import SPM_GPS
import numpy as np
from parspyfunc import parspy
from filtpyfunc_v2 import filtpy
import scipy.signal as sp


#Desplazamiento cuadratico medio:
def DCM(zMed, zSim):
    dcm = []
    for i in range(len(zMed)):
        dcm.append((zMed[i] - zSim[i])**2)
    dcm = np.sqrt(np.sum(dcm)/len(zMed))    
    return dcm

#Señal medida
angElev, angAzim, intensidad, cantidad = parspy('191108prn06.out', ploteo = False, guardar = True)

angElevFilt, snr = filtpy(angElev, angAzim, intensidad, ploteo = False, guardar = False)

fraccion = 2
n = int((len(angElevFilt)/fraccion - len(angElevFilt)%fraccion)) #Recorto a la mitad de la tira de datos

angElevFilt = angElevFilt[:n]
angElevFilt = sp.decimate(angElevFilt, 10)


#Me paro en un entorno del notch para analizar
cotin = 400 #Cota inicial
cotfi = -1  #Cota final
angElevFilt = angElevFilt[cotin:cotfi]
snr = snr[cotin:cotfi]


snr = snr[:n]
snr = sp.decimate(snr,10)


#Grilla de barrido
alt = np.linspace(2,3.5,5) #2
lon = np.linspace(0.05,0.15,5)
rms = np.linspace(0.005,0.01,5) #0.006
eps = np.linspace(20,30,5) 

#simu = []
target = np.zeros((len(eps),len(rms),len(lon),len(alt)))
i=0
total = len(eps)*len(rms)*len(lon)*len(alt)
for e in range(len(eps)):
    for r in range(len(rms)):
        for l in range(len(lon)):
            for a in range(len(alt)):
                i += 1
                porcentaje = i*100/total
                print('cargando: ',porcentaje,'%')
                out = []
                for ang2 in ang:
                    th = 90-ang2
                    out.append(SPM_GPS(th, th, eps[e], rms[r], lon[l], alt[a], 3e8/(1.57549e9),  50))
                target[e,r,l] = DCM(snr,out)
#        simu.append(out)   

print(target)

result = np.where(target == np.amin(target))
#print(result)

cord = list(zip(result[0], result[1],result[2],result[3]))
cord = np.asarray(cord)
cord = cord[0]
print(cord)

print('minimo: ', target[cord[0],cord[1],cord[2]], 'eps: ', eps[cord[0]], 'rms: ', rms[cord[1]], 'lon: ', lon[cord[2]], 'alt: ', alt[cord[3]])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

X, Y = np.meshgrid(eps, rms)
plot = plt.pcolor(X, Y, target, cmap='seismic')

fig.colorbar(plot)
plt.show()

fig = plt.figure()
fig1 = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(eps, rms)
plot = fig1.plot_surface(X.T, Y.T, target, cmap='gnuplot')
fig.colorbar(plot)
plt.show()

#Simulacion de señal
#input: (angElev, angElev, eps, alt_rms, long_corr, alt_ant, long de onda, apertura, ordenCuadratura)

for ang in ang:
    th = 90-ang
    out.append(SPM_GPS(th, th, 21, 0.017, 0.05, 3.145, 3e8/(1.57549e9), 90, 50))


import matplotlib.pyplot as plt
plt.plot(ang, out, label = 'simulacion')
plt.plot(ang, snr, label = 'medicion')
plt.legend()
plt.show()

