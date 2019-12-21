#Lee datos del magnetometro, este corre sobre el programa de arduino "magnetometro.ino". Si se usa como calibrador, debe correrse sobre el programa "magnetomotor.ino" y adquirir datos sobre una vuelta completa.
"""
El argumento de la funcion es un booleano, donde muestra los datos en tiempo real si es True
"""
def magneto(plot)

    import serial, time
    
    try:
        arduino = serial.Serial("/dev/ttyACM0", 9600)
        time.sleep(1)
    except:
        arduino = serial.Serial("/dev/ttyACM1", 9600)
        time.sleep(1)
    
    name = 'calibracion.out'    
    f = open(same, 'w')
    
    i = 0
    cantidad = 500
    while i<cantidad:
        linea = arduino.readline().decode('utf-8') 
        if plot == True:
            print(linea) #Si quiero que me lo muestre en vivo o no.

        f.write(linea) #Guarda la linea en el archivo generado
        i+=1
    
    f.close() #cierra el archivo creado
    return name
