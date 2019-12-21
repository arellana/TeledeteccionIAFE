def parspy(linea, satelite):

    linea2 = linea.replace('*',',').split('\n')

    #De la lista separo a su vez los elementos tambien delimitados por ','
    medicion = []
    for i in range(0,len(linea2)): 
        n = len(linea2[i])
        m = 0
        for j in range(0,n):
            if linea2[i][j] == ',':
                medicion.append(linea2[i][m+1:j])
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

    #Seleccion del satelite
    angElev, angAzim = [],[]
    for x in range(len(GPGSV)): #Elimino la etiqueta "GPSGV"
        del GPGSV[x][0]

    #Relleno de ceros los espacios vacios y convierto a enteros
    for x1 in range(len(GPGSV)): 
        for x2 in range(len(GPGSV[x1])):
            if len(GPGSV[x1][x2]) == 0:
                GPGSV[x1][x2] = '0'
            GPGSV[x1][x2] = int(GPGSV[x1][x2])

    #Creo los vectores de angulos
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
            if GPGSV[L][L2] == satelite:
                angAzim = GPGSV[L][L2+2]
                angElev = GPGSV[L][L2+1]

    return angElev, angAzim


