Aquí te paso una versión estilizada como **README.md** de GitHub para tu proyecto. Le di formato con Markdown, jerarquías claras de títulos y secciones, bloques de código para nombres de archivos y una estructura típica de documentación de software.


# 🌱 Software: Estimación de la Constante Dieléctrica del Suelo

**Autores:**  
- [arellana.javier.e@gmail.com](mailto:arellana.javier.e@gmail.com)  
- [eugenianoelg@gmail.com](mailto:eugenianoelg@gmail.com)  

**Grupo de Teledetección**  
Instituto de Astronomía y Física del Espacio (IAFE) - UBA / CONICET  

---

⚠️ **IMPORTANTE:**  
La versión estable del software se encuentra en la carpeta:  

```bash
/VersionFinal/
```
Este documento describe en detalle la **funcionalidad** y la **forma de utilización** del software.

---

## 📂 Estructura de la carpeta `VersionFinal`

### 1. Mediciones

#### Programas principales

* **`antena_v5.py`**
  Programa base de adquisición de datos.

  * Controla el hardware y guarda los datos del satélite:

    * Intensidad
    * Ángulo azimutal
    * Ángulo de elevación
  * Guarda además el ángulo azimutal en forma separada.
  * **Requisitos de conexión**:

    * Receptor GPS con antena (USB).
    * Sistema de automatización basado en **Arduino UNO** (USB).

  **Funcionamiento**:

  1. Se indica el satélite a seguir.
  2. Llama a la función `reorientacion` → mide el ángulo polar del satélite y reorienta hacia el norte con `motorNorte`.
  3. Las líneas a medir del receptor GPS se configuran en el programa (se recomienda un número mayor al necesario).
  4. En cada iteración del loop compara:

     * Ángulo en tiempo real del satélite.
     * Ángulo actual de la antena.
     * Si la diferencia > **3°**, reorienta automáticamente.

  ✅ El proceso puede abortarse en cualquier momento sin pérdida de datos.

---

* **`parpyfunc_v2.py`**
  Procesa las líneas del formato **NMEA-183**.

  * Extrae datos de mensajes `GPGSV`.
  * Filtra la información del satélite de interés.
  * Guarda:

    * Ángulo de elevación
    * Ángulo azimutal

---

* **`programa2_v3.py`**
  Contiene dos funciones principales:

  * `reorientacion()`

    * Enciende el magnetómetro.
    * Calcula el ángulo actual de la antena (promedio sobre cada eje).
    * Devuelve el ángulo redondeado.

  * `motornorte(arg1, arg2)`

    * Recibe:

      * `arg1`: ángulo actual del satélite.
      * `arg2`: ángulo azimutal de la antena.
    * Se comunica con el programa `AutomatizacionV2.ino` en Arduino.
    * Envía instrucciones vía **serial** en el formato:

      ```text
      "1,0"  
      "i,j"   # con i = {2,3} y j un entero
      ```

---

### 2. Calibración

* **`/magnetomotor/magnetomotor.ino`**
  Programa para cargar en la **Arduino UNO** con el fin de calibrar el magnetómetro **AK8963** integrado en el módulo **MPU9250**.

  * Hace girar de forma continua el motor paso a paso **28BYJ-48**.
  * Registra cada 100 ms la intensidad en los ejes del magnetómetro.

---

* **`magneto.py`**

  * Se conecta al Arduino.
  * Recibe mediciones de `magnetomotor.ino`.
  * Guarda los datos en el archivo:

    ```bash
    calibracion.out
    ```

---

* **`calibracion2.py`**

  * Grafica los planos XY, XZ e YZ a partir de los datos de `magneto.py`.
  * Muestra ángulo azimutal en función del número de medición.
  * Aplica la **corrección por eje** y vuelve a graficar.
  * Ajusta el azimut para que se mida como una brújula convencional:

    * Intervalo: `[0°, 360°)`
    * En lugar de: `[-π/2, π/2]` (rad).

---

### 3. Programa Arduino

* **`AutomatizacionV2.ino`**

  * Controla el motor paso a paso **28BYJ-48** con su controlador **ULN2003**.
  * Integra el magnetómetro **MPU9250**.
  * Comunica las órdenes de movimiento con la PC.

---

## 🚀 Uso típico

1. **Configurar el hardware**:

   * Conectar GPS + Arduino UNO vía USB.
   * Verificar conexión del motor paso a paso y magnetómetro.

2. **Calibración inicial (opcional)**:

   ```bash
   arduino-cli upload -p <puerto> magnetomotor/magnetomotor.ino
   python magneto.py
   python calibracion2.py
   ```

3. **Ejecutar adquisición de datos**:

   ```bash
   python antena_v5.py
   ```

4. **Procesar datos GPS**:

   ```bash
   python parpyfunc_v2.py
   ```

---
