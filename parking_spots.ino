// pins numbers
const int u1_trigger_point = 3; //ultrasonic 1 sensor trig
const int u1_echo_detector = 2; //ultrasonic 1 sensor echoer
const int red_light_1 = 4;  //led light red
const int green_light_1 = 5;  //led light green
const int blue_light_1 = 6;  //led light blue

const int u2_trigger_point = 8; //ultrasonic 2 sensor trig
const int u2_echo_detector = 7; //ultrasonic 2 sensor echoer
const int red_light_2 = 9;  //led light red
const int green_light_2 = 11;  //led light green
const int blue_light_2 = 10;  //led light blue

// defining the variables here
long time_interval1;
int length1;
bool booked1= false;

long time_interval2;
int length2;
bool booked2= false;


void setup() {

pinMode(u1_trigger_point, OUTPUT); // Setting the trigger_point of u1 as an Output
pinMode(u1_echo_detector, INPUT); // Setting the echo_detector of u1 as an Input
pinMode(red_light_1, OUTPUT);// led red light
pinMode(blue_light_1, OUTPUT);// led blue light
pinMode(green_light_1, OUTPUT);// led green light

pinMode(u2_trigger_point, OUTPUT); // Setting the trigger_point of u2 as an Output
pinMode(u2_echo_detector, INPUT); // Setting the echo_detector of u2 as an Input
pinMode(red_light_2, OUTPUT);// led red light
pinMode(blue_light_2, OUTPUT);// led blue light
pinMode(green_light_2, OUTPUT);// led green light

Serial.begin(9600); // begins serial communication of this circuit
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
if (!booked1)
{
    if (value == '0')
    {
      booked1 = true;
    }
  
  if (length1 <= 6)
  {
    Serial.print("DETECTED");
    Serial.print(" ");
    RGB_color_1(255, 0, 0); //setting red light on bc spot is free
  }
  else
  {
    RGB_color_1(0, 255, 0); // setting green light on bc spot is free
    Serial.print("EMPTY");
    Serial.print(" ");
  }
}
else 
{
  if (value == '1')
  {
      RGB_color_1(0, 255, 0);
      Serial.print("EMPTY");
      Serial.print(" ");
      booked1 = false;
  }
  else
  {
  Serial.print("BOOKED");
  Serial.print(" ");
  
  }

  RGB_color_1(90, 50, 60);
  
}

if (!booked2)
{
    if (value == '2')
    {
    booked2 = true;
    }
  
  if (length2 <= 6)
  {
    Serial.println("DETECTED");
    RGB_color_2(255, 0, 0); //setting red light on bc spot is free
  }
  else
  {
    RGB_color_2(0, 255, 0); // setting green light on bc spot is free
    Serial.println("EMPTY");
  }
}
else 
{
  
  
    if (value == '3')
    {
    RGB_color_2(0, 255, 0);
    Serial.println("EMPTY");
    booked2 = false;
    }
    else
    {
    Serial.println("BOOKED");
    RGB_color_2(200, 200, 200);
    }
    
  
}


delay(1000);

}

void RGB_color_1(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_1, red_light_value);
  analogWrite(green_light_1, green_light_value);
  analogWrite(blue_light_1, blue_light_value);
}

void RGB_color_2(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_2, red_light_value);
  analogWrite(green_light_2, green_light_value);
  analogWrite(blue_light_2, blue_light_value);
}
