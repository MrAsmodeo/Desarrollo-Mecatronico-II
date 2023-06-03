#include <SoftwareSerial.h>
#include <Arduino.h>
SoftwareSerial BTSerial(16, 17); // RX, TX

const int pinA1 = 27;
const int pinA2 = 14;
const int pinB1 = 12;
const int pinB2 = 13;
const int pinC1 = 3;
const int pinC2 = 21;
const int pinD1 = 19;
const int pinD2 = 18;
 int ENA = 26;
 int ENB = 25;
 int ENA1 = 1;
 int ENB1 = 5;
void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);  // Configura la velocidad del puerto serie Bluetooth
  pinMode(pinA1, OUTPUT);
  pinMode(pinA2, OUTPUT);
  pinMode(pinB1, OUTPUT);
  pinMode(pinB2, OUTPUT);
  pinMode(pinC1, OUTPUT);
  pinMode(pinC2, OUTPUT);
  pinMode(pinD1, OUTPUT);
  pinMode(pinD2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(ENA1, OUTPUT);
  pinMode(ENB1, OUTPUT);
}
void analogWrite(int pin, int value) {
  // Código para generar señal PWM
}

void loop() {
  if (BTSerial.available()) {    // Verifica si hay datos disponibles en el puerto serie Bluetooth
    char command = BTSerial.read();    // Lee el comando enviado por Bluetooth
    Serial.print("Command received: ");
    Serial.println(command);

    switch(command) {    // Ejecuta la acción correspondiente según el comando recibido
      case 'A':
        Serial.println("Left");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, HIGH);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, HIGH);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, HIGH);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, HIGH);
          digitalWrite(pinD2, LOW);
          analogWrite(ENB1, 100);
        break;
      case 'W':
        Serial.println("Forward");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, HIGH);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, HIGH);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, HIGH);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, HIGH);
          analogWrite(ENB1, 100);
        break;
      case 'X':
        Serial.println("Backward");
          digitalWrite(pinA1, HIGH);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, HIGH);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, LOW);
        break;
      case 'Z':
        Serial.println("Backward");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, HIGH);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, HIGH);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, LOW);
        break;
      case 'C':
        Serial.println("Backward");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, HIGH);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, HIGH);
          digitalWrite(pinD2, LOW);
        break;
      case 'b':
        Serial.println("Backward");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, HIGH);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, HIGH);
        break;
      case 'S':
        Serial.println("Backward");
          digitalWrite(pinA1, HIGH);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, HIGH);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, HIGH);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, HIGH);
          digitalWrite(pinD2, LOW);
        break;
      case 'D':
        Serial.println("Right");
          digitalWrite(pinA1, HIGH);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, HIGH);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, HIGH);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, HIGH);
          analogWrite(ENB1, 100);
        break;
      case 'Q':
        Serial.println("Rotate1");
          digitalWrite(pinA1, HIGH);
          digitalWrite(pinA2, LOW);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, HIGH);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, HIGH);
          digitalWrite(pinC2, LOW);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, HIGH);
          digitalWrite(pinD2, LOW);
          analogWrite(ENB1, 100);
        break;
      case 'E':
        Serial.println("Rotate2");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, HIGH);
          analogWrite(ENA, 100);
          digitalWrite(pinB1, HIGH);
          digitalWrite(pinB2, LOW);
          analogWrite(ENB, 100);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, HIGH);
          analogWrite(ENA1, 100);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, HIGH);
          analogWrite(ENB1, 100);
        break;
        
      case ' ':
        Serial.println("STOP");
          digitalWrite(pinA1, LOW);
          digitalWrite(pinA2, LOW);
          digitalWrite(pinB1, LOW);
          digitalWrite(pinB2, LOW);
          digitalWrite(pinC1, LOW);
          digitalWrite(pinC2, LOW);
          digitalWrite(pinD1, LOW);
          digitalWrite(pinD2, LOW);
        break;
      default:
        Serial.println("Invalid command");
        break;
    } 
}
}