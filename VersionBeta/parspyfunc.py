"Este programa ordena datos en formato NMEA-183 y grafica los parametros de interes de un satelite GPS seleccionado."

#Paramentros:
#   filename: nombre de la tira de datos a analizar en formato NMEA-183
#   satelite: identificacion de satelite a analizar
#   ploteo: booleano, True grafica, False no lo hace.
#   guardar: booleano, True guarda los datos en un archivo llamado "datpars.txt"
#            donde ordena angulo de elevacion, angulo azimut e intensidad en una
#            matriz de 3 columnas.
def parspy(filename, ploteo, guardar):


    satelite = int(filename[9:11])
    print('Satelite: ', satelite)

    import matplotlib.pyplot as plt
    
    data = open(filename, encoding="utf-8").read() #Agregar direccion del archivo a leer

#info contiene las primeras 2 filas del archivo, fecha, hora, etc
#pie es el pie del archivo, no se si importa pero por las dudas lo guardo
#data2 son todos los datos a analizar. Creo una lista que contiene en cada elemento una fila de data2
#    info, data2, pie =  data[0:90], data[92:len(data)-36].replace('*',',').split('\n'), data[-34:]


    data2=data.replace('*',',').split('\n')


#De la lista separo a su vez los elementos tambien delimitados por ','
    medicion = []
    for i in range(0,len(data2)): 
        n = len(data2[i])
        m = 0
        for j in range(0,n):
            if data2[i][j] == ',':
                medicion.append(data2[i][m+1:j])
                m = j


#Separo en sublistas (dentro de la lista original), donde c/u contiene una fila ya separada por columnas
    medicion2 = []
    v=0
    for k in range(1,len(medicion)):
    
        if medicion[k] == '':
            pass

        else:
            if medicion[k][0] == 'G':
                medicion2.append(medicion[v:k])
                v = k
    medicion2.append(medicion[v:len(medicion)])



#Selecciono solo los datos tipo "GPGSV"
    GPGSV = []
    for i2 in range(len(medicion2)):
        if medicion2[i2][0] == 'GPGSV':
            GPGSV.append(medicion2[i2])
        
################### Fin del ordenamiento ####################

    " Seleccion del satelite "
    satSelec = satelite #Numero de entrada manual del satelite analizado
    intensidad, angElev, angAzim = [],[],[]
    muestras = 1

    for x in range(len(GPGSV)): #Elimino la etiqueta "GPSGV"
        del GPGSV[x][0]

#Relleno de ceros los espacios vacios y convierto a enteros
    for x1 in range(len(GPGSV)): 
        for x2 in range(len(GPGSV[x1])):
            if len(GPGSV[x1][x2]) == 0:
                GPGSV[x1][x2] = '0'
            GPGSV[x1][x2] = int(GPGSV[x1][x2])

    
#Creo los vectores de intensidad, y angulos
    for L in range(0,len(GPGSV)):    
        if len(GPGSV[L]) == 7:
            satPlace = [3]
        elif len(GPGSV[L]) == 11:
            satPlace = [3,7]
        elif len(GPGSV[L]) == 15:
            satPlace = [3,7,11]
        elif len(GPGSV[L]) == 19:
            satPlace = [3,7,11,15]
        for L2 in satPlace:
            if GPGSV[L][L2] == satSelec:
                intensidad.append(GPGSV[L][L2+3])
                angAzim.append(GPGSV[L][L2+2])
                angElev.append(GPGSV[L][L2+1])
                muestras = muestras + 1

    

    import numpy as np

    if guardar == True:
        np.savetxt('angulo.txt', np.c_[angElev, angAzim, intensidad], delimiter = ';')#, fmt='%i')

    angElev = np.asarray(angElev)
    angAzim = np.asarray(angAzim)
    intensidad = np.asarray(intensidad)   
    

    if angElev[0] < angElev[-1]:
        pass
    else:
        angElev = angElev[::-1]
        angAzim = angAzim[::-1]
        intensidad = intensidad[::-1]
    
#Ploteo
#En otro momento hago que grafique mas lindo, ahora no es una prioridad
    cantidad1 = range(1,muestras,1)

    if ploteo == True:    
        plt.plot(cantidad1,intensidad, label='C/No')
        plt.plot(cantidad1,angAzim, label='Angulo Azimutal')
        plt.plot(cantidad1,angElev, label='Angulo de Elevacion')
        plt.legend()
        plt.show()
    
    return angElev, angAzim, intensidad, cantidad1
