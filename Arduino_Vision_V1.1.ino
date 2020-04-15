/* 
 * Latest Update: 15.04.2020 
 * Developer:     Emre Albayrak Istanbul/TURKEY
 * This code written for control the arduino based pan-tilt mechanism. 
 * It uses Arduino CNC shield to control stepper motors of pan-tilt mechanism.
 * For more https://github.com/EmreAlbayrak/Face-Tracking-Pan-Tilt.
*/

#define stepPin_z     4 
#define dirPin_z      7
#define stepPin_x     2 
#define dirPin_x      5 
#define enable        8
char serialdata[3]; //an array for serial read data package
void setup() {
  pinMode(stepPin_z,OUTPUT); 
  pinMode(dirPin_z,OUTPUT);
  pinMode(stepPin_x,OUTPUT); 
  pinMode(dirPin_x,OUTPUT);
  pinMode(enable,OUTPUT);
  digitalWrite(enable, LOW); 
  Serial.begin(9600);
}
//--------------------------------------------------------------------------- Infinite Loop
void loop() {
 if(Serial.available()>0){
    Serial.readBytes(serialdata,4);
  }
  motormove(serialdata[0]);
}
//--------------------------------------------------------------------------- Functions
void motormove(int parameter){ 
  if(parameter == '1'){
    digitalWrite(dirPin_x,HIGH);
    digitalWrite(stepPin_x,HIGH); 
    delayMicroseconds(8000); 
    digitalWrite(stepPin_x,LOW); 
    delayMicroseconds(8000); 
  }
  if(parameter == '2'){
    digitalWrite(dirPin_x,LOW);
    digitalWrite(stepPin_x,HIGH); 
    delayMicroseconds(8000); 
    digitalWrite(stepPin_x,LOW); 
    delayMicroseconds(8000);
  }
  if(parameter == '3'){
    digitalWrite(dirPin_z,LOW); 
    digitalWrite(stepPin_z,HIGH); 
    delay(10); 
    digitalWrite(stepPin_z,LOW); 
    delay(50); 
  }
  if(parameter == '4'){
    digitalWrite(dirPin_z,HIGH);
    digitalWrite(stepPin_z,HIGH);
    delay(10);
    digitalWrite(stepPin_z,LOW);
    delay(50);
  }
  if(parameter == '5'){
    //a-axis and y-axis adjusted or no face found
  }
}
