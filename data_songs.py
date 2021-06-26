"""
------------------ Python module to get the data of an mp3 file (Album, artist and release date) --------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program is aimed to serve a multitouch graphic interface that runs in a RaspberryPi 4 - B and helps such
interface to get the Album, artist and release date of a song using eyed3 library.
 
For further technical details check the report at https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing
 
"""
import eyed3

def get_data_song(song):
    song = eyed3.load(str(song))
    data =  str(song.tag.album)+"-"+str(song.tag.artist)+"-"+str(song.tag.getBestDate())
    return (str(data))

def split_midspace(string):
    res = ""
    if " " in string:
        mid_s = string.count(" ")//2
        list_s = string.split()
        for i in range(len(list_s)):
            if i == mid_s:
                res += "\n"
            res += list_s[i] + " "
    else:
        res = string
        
    return res
