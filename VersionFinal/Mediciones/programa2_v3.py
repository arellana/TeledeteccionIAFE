""" 
Esta version esta pensado en 2 programas principales: reorientacion y motorNorte.

*reorientacion no tiene argumento. Solo enciende el magnetometro, toma un promedio sobre cada eje y calcula el angulo actual de la antena. Devuelve este ultimo redondeado.
 
*motornorte(arg1,arg2):
motor recibe en arg1 el angulo actual del satelite a analizar y en arg2 el angulo
azimutal de la antena.
Este funciona con "AutomatizacionV2.ino" montado sobre dicha plaqueta.
No tiene valor de retorno.

Esta funcion deberia correrse en un loop mientras el antena.py este corriendo.
Probablemente no sean necesarias las lineas de coneccion a serial.

Las instrucciones son enviada por serial como una cadena del estilo "1,0" y "i,j" con i = 2,3 y j un entero.

"""

import numpy as np
import serial, time
import re

#Correcion sobre grados calculados
def trunc(entrada):
    flot = entrada - int(entrada)
    if flot < 0.5:
        salida = int(entrada)
    elif flot >= 0.5:
        salida = int(entrada) + 1
    return salida


def reorientacion(arduino):
    #Inicia conexion con la plaqueta mediante USB:
    arduino.write(bytes('1,0', 'utf-8'))    
    data = ""
    
    print("Escribiendo  datos de la magnetización del IMU...")
    for i in range(10):
        print(i)
        linea = arduino.readline().decode('utf-8')
        data = data +linea
    print("terminado")


    data2=data.replace(';', '\n').split('\n')
    x = []
    y = []
    z = []

    rango = np.arange(0, len(data2), 3) 
    rango = rango[0:-1]
    for j in rango:
        x =np.append(x, [float(data2[j])])
        y= np.append(y, [float(data2[j+1])])
        z= np.append(z, [float(data2[j+2])])

    print("Resultados (microTesla):")

    mean_x =np.mean(x)
    mean_y =np.mean(y)
    print(mean_x,mean_y)
    print("Midiendo posicion relativa al norte")

    import math
    fi_rad = math.atan(mean_x/mean_y)
    fi_grad_1 = fi_rad*180/math.pi     
    if mean_x < 0:
        if mean_y> 0:
            fi_grad = fi_grad_1
        if mean_y < 0:
            fi_grad = fi_grad_1-180
    if mean_x > 0:
        if mean_y  < 0:
            fi_grad = fi_grad_1+180
        if mean_y > 0:
            fi_grad = fi_grad_1

    print("El norte esta a ", str(round(fi_grad)), "° respecto del eje x del IMU")

    return trunc(fi_grad)



def motorNorte(angSat, angAct, arduino):

    unidad = 512/360
    deltaGrado = angSat - angAct    
    grado = trunc(deltaGrado * unidad)

    if deltaGrado  < 0: #Si el satelite se movio positivamente
        orden = '2,'+str(grado)
        print(orden) 
        arduino.write(bytes(orden, 'utf-8'))

    elif deltaGrado > 0: #Si el satelite se movio negativamente
        orden = '3,'+str(grado) 
        print(orden)
        arduino.write(bytes(orden, 'utf-8'))


        time.sleep(3)
        print('Reorientando...')

#Estos son lineas de prueba, se pueden descomentar y correr simplemente este programa sin ningun otro

#azimut =  reorientacion()
#print('azimut actual: ', azimut)
#motorNorte(0, azimut)
#motorNorte(50,60)

