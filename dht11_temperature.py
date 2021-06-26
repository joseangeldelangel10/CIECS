"""
----------------------------------- DHT11 python module to get temperature -------------------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program is aimed to serve a multitouch graphic interface that runs in a RaspberryPi 4 - B and helps such
interface to give user a real time ambient temperature in degrees celsius.
 
For further technical details check the report at https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing
 
"""
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

def get_temperature(pin_number):
  # read data using pin_number
  instance = dht11.DHT11(pin = pin_number)
  result = instance.read()

  if result.is_valid():
      string = "%-3.1f C" % result.temperature
  else:
      string = "Error: %d" % result.error_code
  
  return string
