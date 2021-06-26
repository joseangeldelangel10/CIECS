"""
-------------------- Python module to read mp3 files form a USB in a RaspberryPi 4- B ---------------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program is aimed to serve a multitouch graphic interface that runs in a RaspberryPi 4 - B and helps such
interface to store the directories of all the mp3 files in a USB stick in Raspbian OS, this programm also allows our
interface to obtain the name of each mp3 file instead of the directory itself. 
 
For further technical details check the report at:
https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing
"""
import os
import subprocess

def get_usb_name():
  rpistr = "ls ../../../../media/pi"
  proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
  line = proc.stdout.readline()
  return line.rstrip()

def get_mp3_files():
  res = []
  usb_name = get_usb_name()
  usb_name = usb_name.decode('ascii')
  dir_path = "../../../../media/pi/{usb_name}".format(usb_name=usb_name)
  for root, dirs, files in os.walk(dir_path):
      for file in files: 
          # change the extension from '.mp3' to 
          # the one of your choice.
          if file.endswith('.mp3'):
              res.append(root+'/'+str(file))
  return res

def dir_to_name(s):
  new_s = s[:-4]
  new_s = new_s[21:]
  i_slash = new_s.index('/')
  try:
    new_s = new_s[i_slash+1:]
    return new_s
  except IndexError:
    return new_s
  
