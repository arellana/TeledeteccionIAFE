import serial
import time
from parspyfunc_v2 import parspy
from programa2_v3 import motorNorte
from programa2_v3 import reorientacion

try:
    arduino = serial.Serial("/dev/ttyACM0", 9600)
    acm = 0
except:
    arduino = serial.Serial("/dev/ttyACM1", 9600)
    acm = 1
    
try:
    ser = serial.Serial(port='/dev/ttyUSB0')
    print('Conectado con ACM', acm, ' - USB0')
except:
    ser = serial.Serial(port='/dev/ttyUSB1')
    print('Conectado con ACM', acm, ' - USB1')


anteultimo =  reorientacion(arduino)
motorNorte(0, anteultimo, arduino)
satint = 17
satstr = str(satint)

timestr = time.strftime("%y%m%d")
timestr2 = time.strftime("%H,%M,%S")

#Crea las tiras de datos con los valores medidos
f = open(timestr+'prn'+satstr+timestr2+'.out', 'w') 
g = open(timestr+'prn'+satstr+timestr2+'_Azim.out', 'w') 


i = 0
l = 0
a = 0
cantidad = 50000
anteultimo = 0
while i<cantidad: 
    linea = ser.readline()
    try:
        linea = linea.decode('utf-8')
        print(linea)
        f.write(linea)

        if linea[1:6] == 'GPGSV':
            angElev, angAzim = parspy(linea, satint)  

            if angAzim == []: 
                pass
            else:
                print(angAzim)
                g.write(str(angAzim))
                
                if angAzim > 180: #Convercion a escala (-180,180)
                    angAzim = angAzim-360
                else:
                    pass                

                variacion = abs(anteultimo-angAzim)
                if  variacion > 0:
#En el primer paso que es de reorientacion muevo al motor lo que corresponde                    
                    if l == 0:
                        motorNorte(angAzim, anteultimo,arduino)
                        time.sleep(10)

#Se fija que efectivamente se movio al lugar indicado
                        posicion_nueva = reorientacion(arduino)
                        time.sleep(2)
                        desplazamiento = abs(posicion_nueva-angAzim)
                        print('desplazamiento: ', desplazamiento)

#Si el motor no llego a la posicion deseada lo mueve otra vez
                        while desplazamiento > 3:
                            motorNorte(angAzim, posicion_nueva, arduino)
                            time.sleep(5)
                            posicion_nueva = reorientacion(arduino)
                            time.sleep(5)
                            desplazamiento = abs(posicion_nueva-angAzim)
                            print('desplazamiento: ', desplazamiento)
                        anteultimo = angAzim
                    else:

#Si la variacion es de 3 grados, el motor se mueva 4 pasos (= 2.8°)        
                        if (a % 2) == 0 and variacion == 3 :
                            print('Tratando de mover 3 grados')
                            motorNorte(angAzim, anteultimo, arduino)
                            print('Revisando 1..')
                            posicion_nueva = reorientacion(arduino)
                            time.sleep(5)
                            desplazamiento = abs(posicion_nueva-angAzim)
                            print('Desplazamiento: ', desplazamiento)

#Chequeo en este paso que el motor se este moviendo efectivamente
                            while desplazamiento > 3:
                                motorNorte(angAzim, posicion_nueva,arduino)
                                time.sleep(5)
                                print('Revisando 1..')
                                posicion_nueva = reorientacion(arduino)
                                time.sleep(2)
                                desplazamiento = abs(posicion_nueva-angAzim)                                
                                print('Desplazamiento: ', desplazamiento)
                            a= a+1
                            anteultimo = angAzim

#Si la variacion es de 4 grados, el motor se mueve 6 pasos (= 4.2°)
                        if (a % 2) != 0 and variacion == 4:
                            print('Tratando de mover 4 grados')
                            motorNorte(angAzim, anteultimo, arduino)
                            time.sleep(5)
                            print('Revisando 2..')
                            posicion_nueva = reorientacion(arduino)
                            time.sleep(2)
                            desplazamiento = abs(posicion_nueva-angAzim)
                            print('Desplazamiento: ', desplazamiento)

#Chequeo en este paso que el motor se este moviendo efectivamente
                            while desplazamiento > 3:
                                motorNorte(angAzim, posicion_nueva,arduino)
                                time.sleep(5)
                                print('Revisando 2..')
                                posicion_nueva = reorientacion(arduino)
                                time.sleep(5)
                                desplazamiento = abs(posicion_nueva-angAzim)                                
                                print('Desplazamiento: ', desplazamiento)
                            a= a+1
                            anteultimo = angAzim
                                             
#Si la variacion es menor a 3 grados, pasa.
                        else:
                            pass
                l = l+1
        else:
            pass
    except:
        print("Error en la linea, pasando a la siguiente")
        pass
    i+=1

f.close()
g.close()
ser.close()

