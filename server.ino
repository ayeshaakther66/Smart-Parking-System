#include <Servo.h>
Servo servo;


// pins numbers
const int u1_trigger_point = 3; //ultrasonic 1 sensor trig
const int u1_echo_detector = 2; //ultrasonic 1 sensor echoer

const int u2_trigger_point = 5; //ultrasonic 2 sensor trig
const int u2_echo_detector = 4; //ultrasonic 2 sensor echoer


// defining the variables here
long time_interval1;
int length1;

long time_interval2;
int length2;

bool manual = false;

void setup() {
  pinMode(u1_trigger_point, OUTPUT); // Setting the trigger_point of u1 as an Output
  pinMode(u1_echo_detector, INPUT); // Setting the echo_detector of u1 as an Input

  pinMode(u2_trigger_point, OUTPUT); // Setting the trigger_point of u2 as an Output
  pinMode(u2_echo_detector, INPUT); // Setting the echo_detector of u2 as an Input

  servo.attach(9);
  closeGate();
  Serial.begin(9600);
}
void loop() {
  
  /// 
//ULTRASONIC 1
// clearing the trigger_point
digitalWrite(u1_trigger_point, LOW);
delayMicroseconds(2);

// Sets the trigger_point on HIGH state for 10 micro seconds
digitalWrite(u1_trigger_point, HIGH);
delayMicroseconds(10);
digitalWrite(u1_trigger_point, LOW);

// Reading the echo_detector that returns the sound wave travel time in microseconds
time_interval1 = pulseIn(u1_echo_detector, HIGH);

// Calculating the length
length1 = time_interval1*0.034/2;

////
////ULTRASONIC 2
// clearing the trigger_point
digitalWrite(u2_trigger_point, LOW);
delayMicroseconds(2);

// Sets the trigger_point on HIGH state for 10 micro seconds
digitalWrite(u2_trigger_point, HIGH);
delayMicroseconds(10);
digitalWrite(u2_trigger_point, LOW);

// Reading the echo_detector that returns the sound wave travel time in microseconds
time_interval2 = pulseIn(u2_echo_detector, HIGH);

// Calculating the length
length2 = time_interval2*0.034/2;

int value;
if (Serial.available() > 0)
{
  value = Serial.read();

}
if (!manual)
{
   if (value == '4')
    {
      manual = true;
    }

  if ((length1 <= 10) |(length2 <= 10) )
  {
    Serial.print("DETECTED");
    Serial.print(" ");
    Serial.println("OPEN");
    openGate(); 
  }
  else
  {
    Serial.print("EMPTY");
    Serial.print(" ");
    Serial.println("CLOSE");
    closeGate();
  }
}
else
{
   
  if (value == '1')
  {
    Serial.print("EMPTY");
    Serial.print(" ");
    Serial.println("CLOSE");
    closeGate();
  }
  else if (value == '2')
  {
    Serial.print("DETECTED");
    Serial.print(" ");
    Serial.println("OPEN");
    openGate();
  }
  else if (value == '5')
  {
    manual = false;
    }
}
  delay(1000);
}

void openGate(){
  servo.write(50);
}

void closeGate(){
  servo.write(135);
}
