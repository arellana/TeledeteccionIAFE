def filtpy(angElev, angAzim, intensidad, sat, cutoff_hz, ploteo, guardar):

    import numpy as np
    from scipy.signal import kaiserord, firwin, filtfilt
    from matplotlib import pyplot as plt
    # Genero los valores de "x" filtrados (En este caso, el angulo de elevación es la variable independdiente)    

    nsample= len(angElev)

    # Calculo la frecuencia de muestreo de mis datos, es decir, la cantidad de datos que se adquieren por angulo de elevación.
    same_ang=[] #Voy a llenar este vector con la cantidad de datos que tengan el mismo angulo, yendo del menor angulo al mayor.
    ang = angElev[0]
    last= 0
    i=0
    while ang < angElev[-1]:
        while angElev[i] == ang:
            i = i+1
        same_ang.append(i-last)
        last = i
        ang = ang+1
  
    sample_rate = np.round(np.mean(same_ang[1:-2]),0)
    angElev_filt = (np.arange(nsample) / sample_rate)+angElev[0]

    nyq_rate = sample_rate / 2.0 #es la frecuencia minima que debe tener una señal para que se pueda distinguir con esta frecuencia de sampleo
    width = 0.005/nyq_rate #Es el ancho de la banda de frecuencias de trasnición de las que se quieren filtrar y las que no

    ripple_db = 8 # Maxima desviación de la potencia deseada en el pasabanda en decibelios. Es la minima que me deja poner el programa.

    N, beta = kaiserord(ripple_db, width) #N el orden del filtro (coeficientes+1), y beta el parametro de la funcion kaiser correspondiente a este filtro
    print('cutoff_hz= '+str(cutoff_hz))
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta)) #coeficientes del filtro
    intensidad_filt0 = filtfilt(taps, 1, 10**(intensidad/20) ) #Adquirimos una señal en dB, por lo que hago el pasaje a voltaje para el filtrado
    intensidad_filt = 20*np.log10(intensidad_filt0)
    
    if ploteo == True:
        plt.figure()
        plt.plot(angElev_filt, intensidad, '#3CB371')
        plt.plot(angElev_filt, intensidad_filt, 'r', linewidth=2, label='señal filtrada') #Como el filtro trabaja con voltajes, vuelvo a pasar la señal a dB para que sea comparable con la original
        plt.xlabel('Angulo de Elevación (°)', fontsize= 13)
        plt.ylabel('snr (dB)', fontsize= 13)

    if guardar == True:
        np.savetxt('snrfiltrado_31.txt', intensidad_filt, delimiter=';')
        np.savetxt('angfiltrado_31.txt', angElev_filt, delimiter=';')

    return angElev_filt, intensidad_filt
