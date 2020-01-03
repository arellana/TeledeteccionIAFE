import math
import glob
import numpy as np
from matplotlib import pyplot as plt


archivos = sorted(glob.glob('*/hydra\\19*.txt')) 


datos_todos = []
for filename in archivos:
    datos = open(filename, encoding="utf-8").read()
    datos = datos.split('\n')
    datos_todos.append(datos)

datos_juntos = []
for i in range(len(datos_todos)):
    datos_juntos_k =[]
    for k in range(len(datos_todos[i])):
        if datos_todos[i][k] == '':
            pass
        else:
            datos_juntos_k.append(datos_todos[i][k])
    datos_juntos.append(datos_juntos_k)


todos_eps = []
todos_std = []
for i in range(len(datos_juntos)):
    epsilons_i = []
    datos_medicion_i = datos_juntos[i]
    for k in range(len(datos_medicion_i)):
        linea_k_medicion_i = datos_medicion_i[k]
        n = 0
        for l in range(len(linea_k_medicion_i)):
            if linea_k_medicion_i[l] == ',':
                n=n+1
                if n == 7:
                    eps_ki = float(linea_k_medicion_i[l+2:l+8])
                    epsilons_i.append(eps_ki)
    eps_mean = np.mean(epsilons_i)
    eps_std = np.std(epsilons_i)
    todos_eps.append(eps_mean)
    todos_std.append(eps_std)

print('epsilons en cada medicion')
print(np.transpose([todos_eps,todos_std]))

