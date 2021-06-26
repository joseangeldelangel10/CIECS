/*
----------------------------- Arduino program to control the car luxuries -------------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program is aimed to control the "car luxuries" designed for this proyect. We use the library FreeRTOS, and all the power Arduino Mega provides. The luxuries are things such as a sunroof, the intensisty of the front lights,a collision alarm, the turn signals and the emergency lights. 

For further technical details check the report at https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing 

right back light pins : 26, 24, 22
left back light pins : 23, 25, 27
front lights pins (left,right) : 3,2
front directions lights pins (left,right) : 28,29
directions buttons pins (left,right) : 30,31 
intensity of the lights bits (bit1,bit2)  : 32,33 (input)
emergency lights control pin : 34 (input)
sunroof control pin : 35 (input) 
Trigger pin : 5
Echo pin : 4
Buzzer pin : 6
Servo pin : 7


*/

#include <Arduino_FreeRTOS.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <task.h>
#include <semphr.h>
#include <Servo.h>

bool GoLeft = false;
bool GoRight = false;
Servo servoMotor;
SemaphoreHandle_t back_lights;

void setup()
{
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, INPUT);
  pinMode(6,OUTPUT); 
  servoMotor.attach(7); 
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  pinMode(27, OUTPUT);
  pinMode(28, OUTPUT);
  pinMode(29, OUTPUT);

  pinMode(30, INPUT);
  pinMode(31, INPUT);
  pinMode(32, INPUT);
  pinMode(33, INPUT);
  pinMode(34, INPUT);
  pinMode(35, INPUT);
  
  analogWrite(3,0);
  analogWrite(2,0);
  digitalWrite(5, LOW);
  digitalWrite(26,LOW);
  digitalWrite(24,LOW);
  digitalWrite(22,LOW);
  digitalWrite(29, LOW);
  digitalWrite(23,LOW);
  digitalWrite(25,LOW);
  digitalWrite(27,LOW);
  digitalWrite(28, LOW);

  back_lights = xSemaphoreCreateBinary();
  xTaskCreate(vTask_check_sunroof_status, "Sunroof status",700, NULL, 0 ,NULL );
  xTaskCreate(vTask_check_direction_status,"Direction_status",700,NULL,1,NULL);
  xTaskCreate(vTask_ultrasonico,"Ultrasonico",700,NULL,3,NULL);
  xTaskCreate(vTask_front_lights,"Front_lights",700,NULL,2,NULL);
  xTaskCreate(vTask_check_emergency_status,"Emergency_lights",700,NULL,1,NULL);
}

//------------------------------------------------ Funcionalidad de RTOS --------------------------------------------------------------------

void vTask_check_sunroof_status(void *parametros)
{
  const TickType_t xDelay = pdMS_TO_TICKS(100);
  for(;;)
  {
    check_sunroof_status();
    vTaskDelay (xDelay);
  } 
}

void vTask_check_direction_status(void *parametros)
{
  const TickType_t xDelay = pdMS_TO_TICKS(50);
  for(;;)
  {
    check_direction_status();
    vTaskDelay (xDelay);
  } 
}

void vTask_ultrasonico(void *parametros)
{
  const TickType_t xDelay = pdMS_TO_TICKS(50);
  for(;;)
  {
    ultrasonico();
    vTaskDelay (xDelay);
  } 
}

void vTask_front_lights(void *parametros)
{
  const TickType_t xDelay = pdMS_TO_TICKS(50);
  for(;;)
  {
    front_lights(true,digitalRead(32),digitalRead(33));
    vTaskDelay (xDelay);
  } 
}

void vTask_check_emergency_status(void *parametros)
{
  const TickType_t xDelay = pdMS_TO_TICKS(100);
  for(;;)
  {
    check_emergency_status();
    
    vTaskDelay (xDelay);
  } 
}


//---------------------------------------- Funcionalidad del Hardware ------------------------------------------------
void right(bool status){
  if(status == true){
    digitalWrite(29, HIGH);
    digitalWrite(26,HIGH);
    delay(150);
    digitalWrite(24,HIGH);
    delay(150);
    digitalWrite(22,HIGH);
    delay(150);
    digitalWrite(26,LOW);
    digitalWrite(24,LOW);
    digitalWrite(22,LOW);
    digitalWrite(29, LOW);
    delay(150);
  }
  else{
    digitalWrite(26,LOW);
    digitalWrite(24,LOW);
    digitalWrite(22,LOW);
    digitalWrite(29, LOW);
  }
}

void left(bool status){
  
  if(status == true){
    digitalWrite(28, HIGH);
    digitalWrite(23,HIGH);
    delay(150);
    digitalWrite(25,HIGH);
    delay(150);
    digitalWrite(27,HIGH);
    delay(150);
    digitalWrite(23,LOW);
    digitalWrite(25,LOW);
    digitalWrite(27,LOW);
    digitalWrite(28, LOW);
    delay(150);
  }
  else{
    digitalWrite(23,LOW);
    digitalWrite(25,LOW);
    digitalWrite(27,LOW);
    digitalWrite(28, LOW);
  }
}

void emergency(bool status){
  if(status == true){
    digitalWrite(29, HIGH);
    digitalWrite(26,HIGH);
    digitalWrite(28, HIGH);
    digitalWrite(23,HIGH);
    delay(50);
    digitalWrite(24,HIGH);
    digitalWrite(25,HIGH);
    delay(50);
    digitalWrite(22,HIGH);
    digitalWrite(27,HIGH);
    delay(50);
    digitalWrite(26,LOW);
    digitalWrite(24,LOW);
    digitalWrite(22,LOW);
    digitalWrite(29, LOW);
    digitalWrite(23,LOW);
    digitalWrite(25,LOW);
    digitalWrite(27,LOW);
    digitalWrite(28, LOW);
    delay(50);
  }
  else{
    digitalWrite(26,LOW);
    digitalWrite(24,LOW);
    digitalWrite(22,LOW);
    digitalWrite(29, LOW);
    digitalWrite(23,LOW);
    digitalWrite(25,LOW);
    digitalWrite(27,LOW);
    digitalWrite(28, LOW);
    
  }
}

void front_lights(bool status,bool bit1,bool bit2){
  delay(100);
  if (status == true){
      if (bit1 == LOW  && bit2 == LOW){
        analogWrite(3,0);
        analogWrite(2,0);
      }
      else if (bit1 == LOW  && bit2 == HIGH){
        analogWrite(3,25);
        analogWrite(2,25);
      }
      else if (bit1 == HIGH  && bit2 == LOW){
        analogWrite(3,100);
        analogWrite(2,100);
      }
      else if (bit1 == HIGH  && bit2 == HIGH){
        analogWrite(3,224);
        analogWrite(2,224);
      }
      else{
        analogWrite(3,0);
        analogWrite(2,0);
        }
    }
  else{
    analogWrite(3,0);
    analogWrite(2,0);
    }
}


void check_direction_status(){
  if (digitalRead(31) == HIGH && xSemaphoreTake(back_lights,pdMS_TO_TICKS(50)) == pdTRUE ){
    right(true);
    xSemaphoreGive(back_lights);
  }
  else if (digitalRead(30) == HIGH && xSemaphoreTake(back_lights,pdMS_TO_TICKS(50)) == pdTRUE){
    left(true);
    xSemaphoreGive(back_lights);
  }
  
} 

void check_emergency_status(){
  if (digitalRead(34) == HIGH){
    xSemaphoreTake(back_lights,pdMS_TO_TICKS(50));
    emergency(true);
  }
  else 
  {
    xSemaphoreGive(back_lights);
  }
} 

void check_sunroof_status(){
  if (digitalRead(35) == HIGH){
    servoMotor.write(0);
  }
  else{
    servoMotor.write(180); 
  }
} 

void ultrasonico(){
  long t; 
  long d; 
  long b;

  digitalWrite(5, HIGH);
  delayMicroseconds(10);          
  digitalWrite(5, LOW);
  
  t = pulseIn(4, HIGH); 
  d = t/59;             
  if (d < 11){
    b = b_freq(d);
    tone(6,b);
    delay(25);
    noTone(6);
    delay(25);
  }
  else{
    noTone(6);
  }
  delay(50);
  
}

int b_freq(int d){
    if (d >= 5) {
      return (5)*500;
    }
    else{
      return (10)*500;
    }
}

void loop(){}
