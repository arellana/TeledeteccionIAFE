#Metodo SPM-2

def SPM_GPS(th, ths, eps_in, s_in, l_in, z_ant, lamb, ordenCuadratura):

    import numpy as np
    
    
    ###Parametros iniciales###
    eps = eps_in
    s = s_in #escalar
    l = l_in #escalar
    ths = ths*np.pi/180
    th = th*np.pi/180
    ph, phs = 0, 0

    k_min = -2399/10
    k_max = 2400/10
    
    #Modelo
    
    #Onda incidente
    k0 = 2*np.pi/lamb
    
    #Componentes x,y,z en esfericas
    kix= k0*np.cos(ph)*np.sin(th)
    kiy = k0*np.sin(ph)*np.sin(th)
   
    kiz = k0*np.cos(th)
    kperp_i = np.sqrt((kix**2) + (kiy**2))
    
    #Onda dispersada
    ksx = k0*np.cos(phs)*np.sin(ths)
    ksy = k0*np.sin(phs)*np.sin(ths)
    kperp_s = np.sqrt((ksx**2) + (ksy**2))
    ksz = np.sqrt((k0**2) - (kperp_s**2)) #Etiquetado como "Consultar"
    
    #Onda transmitida
    k1 = np.sqrt(eps)*k0
    kiz1 = np.sqrt(eps*(k0**2) - kperp_i**2)
    ktz = np.sqrt(eps*(k0**2) - kperp_s**2)
    
    #Coeficientes de Fresnel
    Rh = (np.cos(th) - np.sqrt(eps - np.sin(th)**2))/(np.cos(th)+np.sqrt(eps-np.sin(th)**2));
    Rv = (eps*np.cos(th) - np.sqrt(eps - np.sin(th)**2))/(eps*np.cos(th) + np.sqrt(eps - np.sin(th)**2))
    
    #Funcion de correlacion
    def corrGauss(k1,k2):
        w = ((s**2)*(l**2)/(4*np.pi))*(np.exp(-0.25*(l**2)*(k1**2 + k2**2)))
        return w
        
    #Amplitudes campo dispersado
    
     
    #modo TM# De ahora en mas, los _v
    alpha0_v = 0
    beta0_v = Rv
    
    ##Orden 1##
    c_is = (kix*ksx + kiy*ksy)/(kperp_i*kperp_s)
    s_is = (kix*ksy - kiy*ksx)/(kperp_i*kperp_s)    
    
    
    alpha1_v = (-2*1j*kiz*(k0**2 - k1**2)/((ksz+ktz)*(eps*kiz+kiz1)))*(kiz1/k0)*s_is 
    beta1_v = -2*1j*kiz*(k0**2 - k1**2)/((eps*ksz+ktz)*(eps*kiz+kiz1))*(eps*kperp_i*kperp_s/(k0**2) - kiz1*ktz*c_is/(k0**2))
    
    ##Orden 2##
    def c_ri(krx, kry):
        return (krx*kix + kry*kiy)/(kperp_i*(np.sqrt(krx**2 + kry**2)))
    def c_rs(krx, kry):
        return (krx*ksx + kry*ksy)/(kperp_s*(np.sqrt(krx**2 + kry**2)))
    def s_ri(krx, kry):
        return (krx*kiy - kry*kix)/(kperp_i*(np.sqrt(krx**2 + kry**2)))
    def s_rs(krx, kry):
        return (krx*ksy - kry*ksx)/(kperp_s*(np.sqrt(krx**2 + kry**2)))

    
    def kappa1(krx,kry):
        return np.sqrt(k0**2 - krx**2 - kry**2)-np.sqrt(k1**2 - krx**2 - kry**2)
    def kappa2(krx,kry):
        return np.sqrt(k0**2 - krx**2 - kry**2)*(np.sqrt(k1**2 - krx**2 - kry**2))*(k0**2 - k1**2)/((k0**2)*(eps*(np.sqrt(k0**2 - krx**2 - kry**2)) + np.sqrt(k1**2 - krx**2 - kry**2)))
    def kappa3(krx,kry):
        return np.sqrt(krx**2 + kry**2)*(k0**2)/(np.sqrt(krx**2 + kry**2)**2 + np.sqrt(k0**2 - krx**2 - kry**2)*np.sqrt(k1**2 - krx**2 - kry**2))
        

    def TM2(krx, kry):
        alpha2_v = ((-2*kiz*(k0**2 - k1**2)/((ksz+ktz)*(eps*kiz+kiz1)))* (-c_rs(krx, kry)*s_ri(krx, kry)*(kiz1/k0)*(kappa1(krx,kry) + ktz) + s_rs(krx, kry)*c_ri(krx, kry)*(kiz1/k0)*(kappa2(krx,kry)+ktz) - s_rs(krx, kry)*(eps*kperp_i/k0)*kappa3(krx,kry) - 0.5*s_is*(eps*k0 - ktz*kiz1/k0)))
        return alpha2_v 

    
    def TM(krx, kry):
        beta2_v = -2*kiz*(k0**2-k1**2)/((eps*ksz+ktz)*(eps*kiz+kiz1))*(-s_rs(krx,kry)*s_ri(krx,kry)*(kiz1/k0)*(eps*k0+ktz*kappa1(krx,kry)/k0)-c_rs(krx,kry)*c_ri(krx,kry)*(kiz1/k0)*(eps*k0+ktz*kappa2(krx,kry)/k0) + c_rs(krx,kry)*(eps*kperp_i*ktz/k0**2)*kappa3(krx,kry) +(eps*kperp_s*kappa3(krx,kry)/k0**2)*(kiz1*c_ri(krx,kry)+np.sqrt(k0**2-krx**2-kry**2)*kperp_i*kappa1(krx,kry)/k0**2)+0.5*c_is*(eps*kiz1-eps*ktz))
        return beta2_v

    ## Campos dispersados ##

    def arg1(k1, k2):
        return corrGauss(k1, k2)
    def arg2(k1,k2):
        return TM(k1, k2)*(corrGauss(k1-kix, k2-kiy))
    def arg3(k1,k2):
        return np.real(TM(k1,k2)*corrGauss(k1-kix, k2-kiy))



    #Integrar por cuadratura gaussiana

    n = ordenCuadratura
    k_lim = 600    
    beta = np.zeros(n)
    for i in range(1,n):
        beta[i] = 0.5/(np.sqrt(1 - (2*i)**(-2)))
    beta = beta[1:]
    
    diagPos = np.diagflat(beta,1)
    diagNeg = np.diagflat(beta, -1)
    
    T = diagPos + diagNeg
    x, V = np.linalg.eig(T) #vector - matriz
    #x: vector de autovalores, V: matriz de autovec en columna

    #Utilizar el indicesSort para reordenar los eV de menor a mayor
    indicesSort = np.argsort(x)
    xsort = np.sort(x)    
        
    Vaux = V[0,indicesSort] #primer ek
    wCuad = np.multiply(Vaux,Vaux)
    wCuad = np.multiply(2,wCuad)
    wt = np.kron(wCuad,wCuad).reshape((n,n))
    
    "Expando el mesh en los bordes"    
    xsort = np.multiply(xsort, k_lim).astype(complex) 
    X, Y = np.meshgrid(xsort,xsort)
    
      
    #Cuadratura Gaussiana

    int1 = np.multiply(arg1(X,Y),wt)    
    int1 = (k_lim**2)*(np.abs(beta1_v)**2)*np.sum(int1)
    #print('int1: ', int1)
    
    int2 = np.multiply(arg2(X,Y),wt)
    int2 = np.real(np.exp(1j*2*kiz*z_ant)*np.conjugate((k_lim**2)*np.sum(int2)))
    #print('int2: ', int2)
    
    int3 = np.multiply(arg3(X,Y),wt)
    int3 = (k_lim**2)*np.sum(int3)    
    #print('int3: ', int3)
    
    
    VV_inc = 1 + beta0_v*2*np.cos(2*kiz*z_ant) + np.abs(beta0_v)**2 + int1 + 2*int2 + 2*beta0_v*int3
    
    VV = VV_inc# - VV_coh
    
    VV2 = 1 + beta0_v*2*np.cos(2*kiz*z_ant) + np.abs(beta0_v)**2
    
    apertura = 90
    
    A1 = 0
    s0_VV = np.real(A1 + 20*np.log10(VV))
    
        
    
    return(s0_VV)
    
