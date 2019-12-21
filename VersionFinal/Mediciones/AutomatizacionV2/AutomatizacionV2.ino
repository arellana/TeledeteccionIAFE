#include "MPU9250.h" //Controlador del IMU
#include "math.h" 


MPU9250 IMU(Wire,0x68);
int status;

//Motor paso a paso conectado entre los pines 8 y 11
//estos deben estar conectados de forma inversa desde la placa al controlador
int input1 = 8; 
int input2 = 9;
int input3 = 10;
int input4 = 11;
int ledPin = 13;

int pasos;

//Matriz de orden de encendido
int bobina[4][4] =
{
 {1, 1, 0, 0},
 {0, 1, 1, 0},
 {0, 0, 1, 1},
 {1, 0, 0, 1}
};

int estado;

void setup() {
  pinMode(input1, OUTPUT);
  pinMode(input2, OUTPUT);
  pinMode(input3, OUTPUT);
  pinMode(input4, OUTPUT);  
  pinMode(ledPin, OUTPUT);        
    
  // serial
  Serial.begin(9600); //Comunicacion con Serial a 9600 bps
  while(!Serial) {}

  // inicia comunicacion
  status = IMU.begin(); //Si inicio bien no devuelve nada, caso contrario devuelve error mas un numero menor a 0
  if (status < 0) {
    Serial.println("IMU no inicializado");
    Serial.println("Revisar conexion o alimentacion del IMU");
    Serial.print("Estado: ");
    Serial.println(status);
    while(1) {}
  }
} 


void loop() {
  
  while(Serial.available()){

    estado = Serial.parseInt();    //estado es el numero asignado a cada "funcion", este corre de 1 a 3, en caso de no ser así devuelve error.
    pasos = Serial.parseInt();

    Serial.print("Estado: ");
    Serial.print(estado);
    Serial.print("- Cantidad de pasos: ");
    Serial.print(pasos);
    Serial.print("\n");

    //estado 1: tomo valores del magnetometro
    if(estado == 1 & pasos == 0){


      digitalWrite(ledPin, HIGH);
      delay(300);
      digitalWrite(ledPin, LOW);
      delay(100);
      digitalWrite(ledPin, HIGH);
      delay(300);
      digitalWrite(ledPin, LOW);

      float x_c, y_c, z_c;

      //Estos valores deben cambiarse segun la calibracion del IMU
      //Correccion en cada eje
      x_c = 11; 
      y_c = 39;
      z_c = -31;

      int cantidad = 0;
    
      while(cantidad < 10){
  
        float x,y,z; 
        IMU.readSensor();
      
        x = IMU.getMagX_uT() - x_c;   //Intensidad del campo en cada eje 
        y = IMU.getMagY_uT() - y_c;
        z = IMU.getMagZ_uT() - z_c;
    
        cantidad++;
//        delay(1000);
        }    
      }

    //estado 2: muevo el motor de forma positiva
    else if(estado == 2){

      for (int i = 0; i < 1; i++){
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);
        delay(100);
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);

        delay(300);
      }

      if(pasos > 0){
        for (int i = 0; i < pasos; i++)
        {
          for (int i = 0; i < 4; i++)
          {
            digitalWrite(input1, bobina[i][0]);         //Encendido de bobina por bloques de pares
            digitalWrite(input2, bobina[i][1]);         //para maximizar el torque
            digitalWrite(input3, bobina[i][2]);
            digitalWrite(input4, bobina[i][3]);
            delay(15);
          }
        }

        digitalWrite(input1, LOW);      //Apagado de todos los campos
        digitalWrite(input2, LOW);      //para reducir consumo
        digitalWrite(input3, LOW);
        digitalWrite(input4, LOW);
      }
    }

    //estado 3: muevo el motor de forma positiva
    else if(estado == 3){

      for (int i = 0; i < 2; i++){
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);
        delay(100);
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);

        delay(300);
      }

      if(pasos > 0){
        for (int i = 0; i < pasos; i++)
        {
          for (int i = 0; i < 4; i++)
          {
            digitalWrite(input4, bobina[i][0]);         //Encendido de bobina por bloques de pares
            digitalWrite(input3, bobina[i][1]);         //para maximizar el torque
            digitalWrite(input2, bobina[i][2]);
            digitalWrite(input1, bobina[i][3]);
            delay(15);
          }
        }

        digitalWrite(input1, LOW);      //Apagado de todos los campos
        digitalWrite(input2, LOW);      //para reducir consumo
        digitalWrite(input3, LOW);
        digitalWrite(input4, LOW);
      }
    }

    else{
      Serial.print("\n");
      Serial.print("Error, no esta definido el estado");
      Serial.print("\n");
    }

    delay(100);         //Espera un milisegundo antes de recomenzar el ciclo
  }
}
