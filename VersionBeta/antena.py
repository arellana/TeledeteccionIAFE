import serial
import time
import numpy as np

#Realiza la interfaz con el receptor GPS conectado al puerto USB
# En caso de no funcionar, cambiar por puerto USBX
try:
    ser = serial.Serial(port='/dev/ttyUSB0', 9600)
except:
    ser = serial.Serial(port='/dev/ttyUSB1', 9600)


timestr = time.strftime("%y%m%d")
timestr2 = time.strftime("%H:%M:%S")

f = open(timestr+'prn15'+timestr2+'.out', 'w') #Crea un archivo con el horario en que se inicio el programa

i = 0
cantidad = 70000
while i<cantidad: #para cada iteracion, lée una linea nueva
    linea = ser.readline().decode('utf-8') 
    print(linea) #Si quiero que me lo muestre en vivo o no.
    f.write(linea) #Guarda la linea en el archivo generado
    i+=1

f.close()

