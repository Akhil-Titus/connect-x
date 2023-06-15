
#include "TFT_eSPI.h"
#define TFT_GREY 0x7BEF
#include <ESP32Servo.h>

Servo myservox; // Create a servo object
Servo myservoy;

TFT_eSPI tft; // Invoke custom library
void setup()
{
myservox.attach(32); // Attach the servo to a pin
myservoy.attach(33);
Serial.begin(9600);
// pinMode(SD_CS, OUTPUT);
// Initialize the TFT display
tft.init();
tft.setRotation(1);
myservox.write(90);
myservoy.write(90);
boot();
// Fill the screen with light blue color
tft.fillScreen(0x264);
title();
fpsmetercard();
ssidcard();
identifycard();
takendowncard();
identifyvalue(); //remove it
ipcard();
showIP();
}
void loop()
{
if (Serial.available()) { // Check if there is any data available to read
int value = Serial.parseInt(); // Read the value from the serial monitor
// Pass the value to a function
fpsvalue(value);
}
sweep();
}
void title()
{

tft.setCursor(22,30);
tft.setTextSize(2);
tft.setTextColor(0xFFFF);
tft.print("CONNECT-X");
}
void fpsmetercard()
{
tft.fillRoundRect(210, 20, 90, 90, 16, 0xFFFF);
tft.setCursor(225,25);
tft.setTextSize(1);
tft.setTextColor(0x0000);
tft.print("FPS METER");
}
void fpsvalue(int x)
{
tft.setCursor(225,50);
tft.setTextSize(2);
tft.fillRoundRect(210, 40, 80, 50, 10, 0xFFFF);
tft.print(x);
}
void ssidcard()
{
tft.fillRoundRect(210, 130,90, 90, 15, 0xFFFF);
tft.setCursor(240,135);
tft.setTextSize(1);
tft.setTextColor(0x0000);
tft.print("SSID");
}

void boot()
{
//tft.setFreeFont(&FreeSerifBold5pt7b);
tft.fillScreen(0x0000);
tft.setCursor(80,100);
tft.setTextColor(0x08F61);
tft.setTextSize(3);
tft.print("C");
delay(300);
tft.print("0");
delay(300);
tft.print("N");
delay(300);
tft.print("N");
delay(100);
tft.print("E");
delay(100);
tft.print("C");
delay(100);
tft.print("T");
delay(100);
tft.print("-");
delay(100);

tft.print("X");
delay(500);
tft.fillScreen(0x45A);
delay(500);
//tft.fillScreen(0x0000);
tft.setCursor(80,100);
tft.setTextColor(0xFFFF);
tft.setTextSize(3);
tft.print("WELCOME...");
delay(1000);
}
void identifycard()
{
tft.fillRoundRect(20, 70, 80, 70, 15, 0xFFFF);
tft.setCursor(28,76);
tft.setTextSize(1);
tft.setTextColor(0x0000);
tft.print("Identified");
}
void identifyvalue()
{
tft.setCursor(40,100);
tft.setTextSize(3);
tft.setTextColor(0xBB123);
//tft.setFreeFont(&FreeMono9pt7b);
tft.print("3");
//tft.setFreeFont();
}
void takendowncard()
{
tft.fillRoundRect(110, 70, 80, 70, 15, 0xFFFF);
tft.setCursor(117,75);
tft.setTextSize(1);
tft.setTextColor(0x0000);
tft.print("Taken Down");
}
void ipcard()
{
tft.fillRoundRect(20, 160, 160, 60, 15, 0xFFFF);
tft.setCursor(30,170);
tft.setTextSize(1);
tft.setTextColor(0x0000);
tft.print("IP ADDRESS");
}
void showIP()
{
tft.setCursor(25,190);
tft.print("192.168.1.1:80/stream");
}

void loading()
{
}
void sweep()
{
for(int i=30;i<100;i++)
{
tft.fillRoundRect(210, 40, 80, 50, 10, 0xFFFF);
// Set text color to white
tft.setTextColor(0x0000);
// Set text size
tft.setTextSize(2);
// Set cursor position
tft.setCursor(225,50);
// Display the value
tft.print(i);
//myservox.write(i);
//myservoy.write(i);
// Delay for a short duration to control the sweep speed
delay(50);
}
}