#include <math.h>

const int temp = A4 ; // temperature sensor port 
const int red_light_1 = 4;  //led light red
const int green_light_1 = 2;  //led light green
const int blue_light_1 = 3;  //led light blue

void setup() {
  pinMode(temp, INPUT);// takes the temp senspor's input
  pinMode(red_light_1, OUTPUT);// led red light
  pinMode(blue_light_1, OUTPUT);// led blue light
  pinMode(green_light_1, OUTPUT);// led green light
  Serial.begin(9600); // begins serial communication of this circuit
}

void loop() {
  double temperature = Thermister(analogRead(A4));
if ((temperature >= 30.00))
{
  RGB_color_1(255, 0, 0); // setting light to red to indicate fire
  Serial.println(temperature);
}
else 
  {
   RGB_color_1(0, 0, 0); //setting red light on bc spot is free
   Serial.println(temperature);

  }
  delay(2000);
}

double Thermister(int RawADC) {
double Temp;
Temp = log(((10240000/RawADC) - 10000));
Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );
Temp = Temp - 273.15; // Convert Kelvin to Celcius
return Temp;
}

void RGB_color_1(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_1, red_light_value);
  analogWrite(green_light_1, green_light_value);
  analogWrite(blue_light_1, blue_light_value);
}
