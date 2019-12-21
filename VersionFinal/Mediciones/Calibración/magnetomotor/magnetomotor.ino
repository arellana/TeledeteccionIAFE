#include "MPU9250.h"
#include "math.h"


int input1 = 8; 
int input2 = 9;
int input3 = 10;
int input4 = 11;

int pasos;

int bobina[4][4] =
{
 {1, 1, 0, 0},
 {0, 1, 1, 0},
 {0, 0, 1, 1},
 {1, 0, 0, 1}
};

MPU9250 IMU(Wire,0x68);
int status;

void setup() {
  pinMode(input1, OUTPUT);
  pinMode(input2, OUTPUT);
  pinMode(input3, OUTPUT);
  pinMode(input4, OUTPUT);  

  Serial.begin(9600);
  while(!Serial) {}

  // Inicia comunicacion con el IMU 
  status = IMU.begin(); //Si inicio bien devuelve 1, caso contrario 0
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
}


void loop() {

  pasos = 2048;

  for (int i = 0; i < pasos; i++)
  {
    for (int i = 0; i < 4; i++)
    {
      int x,y,z;
      IMU.readSensor();

      digitalWrite(input1, bobina[i][0]);
      digitalWrite(input2, bobina[i][1]);
      digitalWrite(input3, bobina[i][2]);
      digitalWrite(input4, bobina[i][3]);

      x = IMU.getMagX_uT();
      y = IMU.getMagY_uT();
      z = IMU.getMagZ_uT();

      Serial.print(x,DEC);       
      Serial.print(";");
      Serial.print(y,DEC);
      Serial.print(";");
      Serial.print(z,DEC);
      Serial.print("\n");

      delay(20);
    }
  }
  digitalWrite(input1, LOW);
  digitalWrite(input2, LOW);
  digitalWrite(input3, LOW);
  digitalWrite(input4, LOW);
  delay(6000);

} 
