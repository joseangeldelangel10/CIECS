"""
----------------------------- Guided User Interface for a car info-entretainment system -------------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program uses python 3, along with kivy framework to generate a multitouch graphic interface that runs 
in a RaspberryPi 4 - B, such graphic interface allows the user to read mp3 files from a USB card and reproduce, pause
and change them at will. Additionaly this code interacts with sensors such as DHT11 to give user more information
regarding the car status.   

Apart from generating the functionality of the app the following program works as the main controller of the app for
music reproduction and sensor controlling. 

Most of the static grapichs in the app are generated in a separate .kv file that is instanced in this code. This 
programm only handles dynamic graphics. 

For further technical details check the report at https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing 

"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import *
from kivy.clock import *
from functools import partial
import dht11_temperature as Temp
import usb_songs
from PlayMp3 import PMP3
import data_songs
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT) #Bit 1 is sent to the arduino in order to control the intensity of front lights
GPIO.setup(18,GPIO.OUT) #Bit 2 is sent to the arduino in order to control the intensity of front lights
GPIO.setup(13,GPIO.OUT) #Bit sent to the arduino in order to control the emergency lights
GPIO.setup(15,GPIO.OUT) #Bit sent to the arduino in order to control the sunroof
GPIO.setup(22,GPIO.OUT)
GPIO.output(13,False)
GPIO.output(15,True)
GPIO.output(16,False)
GPIO.output(18,False)
GPIO.output(22,True)
time.sleep(0.5)

class Main_menu_buttons(Screen):
    pass

class Main_menu(Screen): 
    pass

class Lights_and_sunroof(Screen):
    pass

class Light_options(Screen):
    
    def front_lights(self,bit1 = False,bit2 = False):
        GPIO.output(16,bit1)
        GPIO.output(18,bit2)
        

class Sunroof_button(Screen):
    
    def sunroof_control(self):
        App.get_running_app().sunroof = not App.get_running_app().sunroof  
        GPIO.output(15,App.get_running_app().sunroof)
        

class Song_buttons(Screen):
    ''' Description: class that generates the buttons from every song in the sd card '''
    def __init__(self, **kwargs):
        super(Song_buttons, self).__init__(**kwargs)
        ''' we declare a GridLayout instance that will be then added as 
        a child of Song_buttons class '''
        b = GridLayout()
        b.rows = 6
        b.cols = 1
        b.padding = 5
        b.spacing = 5

        ''' We assign an id to the grid layout in order to reference it at
        will, we also create song_list (a list of the directories where 
        each of the mp3 songs are found) and names_list (a list of al the names of the 
        songs in the sd card list[strings] ), we declare the class atrubutte 
        i that will indicate the index of the last sd song displayed in the screen and
        finally we declare the atribute scrolls that stores the number of scrolls that 
        user has given'''
        self.ids['b'] = b
        self.songs_list = usb_songs.get_mp3_files()
        self.names_list = list(map(usb_songs.dir_to_name, self.songs_list))
        self.i = 0
        self.scrolls = 0
        ''' We add to the GridLayout instance each of its elements, wich are:
        - A label
        - 4 song buttons (for the first 4 songs in the sd in case there are
        less than 4 songs in the SD only n buttons will be created)
        - A scroll button to see the rest of the songs 

        We also create an Error_label to display it in case there are no mp3
        files in the SD or in case there is no SD conected'''

        label = Label(text = "Songs in your SD_card:")
        Error_label = Label(text = "No mp3 files found :,( ")
        b.add_widget( label )
        
        while self.i < len(self.names_list) and self.i < 4:
            button1 = Button( text= self.names_list[self.i]) #create a button with the name of the song
            b_callback = partial( self.play_song, self.songs_list[self.i], self.names_list[self.i] ) #create a callback to the play song function with the song directory as argument
            b.ids[ 'button' + str(self.i) ] = button1 # we assign to each button a different id
            button1.on_press = b_callback 
            b.add_widget( button1 )
            self.i += 1
            
        self.num_song_buttons = self.i  # variable that will store the number of buttons generated
        scroll_down_butt = Button( background_normal = "images/scroll.png", background_color = [0.95,0.61,0.07,0.8] )
        scroll_down_butt.bind(on_press = self.scroll_down_songs)
        b.add_widget(scroll_down_butt)

        ''' Finally if there are no songs in the SD or if there is no SD connected we append to 
        Song_buttons the error label and in any other case we append the grid layout with the song buttons'''
        if len(self.songs_list) > 0:
            self.add_widget(b)
        else:
            self.add_widget(Error_label)
          
    def update_songs_buttons(self, *args):
        self.remove_widget(self.children[0])
        ''' we declare a GridLayout instance that will be then added as 
        a child of Song_buttons class '''
        b = GridLayout()
        b.rows = 6
        b.cols = 1
        b.padding = 5
        b.spacing = 5

        ''' We assign an id to the grid layout in order to reference it at
        will, we also create song_list (a list of the directories where 
        each of the mp3 songs are found) and names_list (a list of al the names of the 
        songs in the sd card list[strings] ), we declare the class atrubutte 
        i that will indicate the index of the last sd song displayed in the screen and
        finally we declare the atribute scrolls that stores the number of scrolls that 
        user has given'''
        self.ids['b'] = b
        self.songs_list = usb_songs.get_mp3_files()
        self.names_list = list(map(usb_songs.dir_to_name, self.songs_list))
        self.i = 0
        self.scrolls = 0

        ''' We add to the GridLayout instance each of its elements, wich are:
        - A label
        - 4 song buttons (for the first 4 songs in the sd in case there are
        less than 4 songs in the SD only n buttons will be created)
        - A scroll button to see the rest of the songs 

        We also create an Error_label to display it in case there are no mp3
        files in the SD or in case there is no SD conected'''

        label = Label(text = "Songs in your SD_card:", font_size = 25)
        Error_label = Label(text = "No mp3 files found :,( ")
        b.add_widget( label )
    
        while self.i < len(self.names_list) and self.i < 4:
            button1 = Button( text= self.names_list[self.i]) #create a button with the name of the song
            b_callback = partial( self.play_song, self.songs_list[self.i], self.names_list[self.i] ) #create a callback to the play song function with the song directory as argument
            b.ids[ 'button' + str(self.i) ] = button1 # we assign to each button a different id 

            button1.on_press = b_callback 
            b.add_widget( button1 )
            self.i += 1
        self.num_song_buttons = self.i  # variable that will store the number of buttons generated

        scroll_down_butt = Button( background_normal = "images/scroll.png", background_color = [0.95,0.61,0.07,0.8] )
        #scroll_down_butt = Button( text = "scroll")
        scroll_down_butt.bind(on_press = self.scroll_down_songs)
        b.add_widget(scroll_down_butt)

        ''' Finally if there are no songs in the SD or if there is no SD connected we append to 
        Song_buttons the error label and in any other case we append the grid layout with the song buttons'''
        if len(self.songs_list) > 0:
            self.add_widget(b)
        else:
            self.add_widget(Error_label)

    def play_song(self, *args):
        print("playing " + args[0])
        wm = App.get_running_app().root
        wm.current = "Media_menu"
        reproduction = App.get_running_app().rep
        reproduction.queue = self.songs_list[self.songs_list.index(args[0]):] + self.songs_list[:self.songs_list.index(args[0])] 
        reproduction.start_playing(args[0])
        reproduction.i = 0
        song_name = usb_songs.dir_to_name(reproduction.queue[0])
        if len(song_name) >= 20:
            song_name = data_songs.split_midspace(song_name)
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[2].text = song_name
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[1].text = data_songs.get_data_song(reproduction.queue[0]) + " SR: 44100 - Stereo - mp3"

        

    def scroll_down_songs(self, *args):
        for j in range(self.num_song_buttons):
            self.ids['b'].ids['button' + str(j)].text = self.names_list[ (self.scrolls + j+1)%(len(self.names_list)) ] 
            # we make every button in the grid layout to have the name of the following song in names_list in case we reach the last
            # song the name in the button will be the name of the first song inthe list  
            b_callback = partial( self.play_song, self.songs_list[ (self.scrolls + j+1)%(len(self.songs_list)) ], self.names_list[ (self.scrolls + j+1)%(len(self.songs_list)) ] )
            self.ids['b'].ids['button' + str(j)].on_press = b_callback
            # we make every button in the grid layout to have a callback to the following song in songs_list in case we reach the last
            # song the callback in the button will be a callback to the first song in the list
        self.i = (self.scrolls + j+1)%(len(self.names_list))
        self.scrolls += 1



class Media_menu(Screen):
    pass

class Calls_menu(Screen):
    pass

class Car_control_menu(Screen):
    pass

class Bluetooth_menu(Screen):
    pass

class Menu_tabs(Screen):
    pass

class Media_menu_device_select(Screen):
    def display_sd_songs(*args):
        print(["song1","song2","song3"])

class Media_menu_media_info_controls(Screen):
    
    def Rewind(self, *args):
        reproduction = App.get_running_app().rep
        rew = reproduction.Rewind()
        wm = App.get_running_app().root
        if rew == -1 and len(reproduction.queue) > 0:
            song_name = usb_songs.dir_to_name(reproduction.queue[reproduction.i])
            if len(song_name) >= 20:
                song_name = data_songs.split_midspace(song_name)    
            wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[2].text = song_name
            wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[1].text = data_songs.get_data_song(reproduction.queue[reproduction.i]) + " SR: 44100 - Stereo - mp3"    


    def play_pause(self, *args):
        reproduction = App.get_running_app().rep
        reproduction.play_pause()


    def Forward(self, *args):
        reproduction = App.get_running_app().rep
        fw = reproduction.Forward()
        wm = App.get_running_app().root
        if fw == 1 and len(reproduction.queue) > 0:
            song_name = usb_songs.dir_to_name(reproduction.queue[reproduction.i])
            if len(song_name) >= 20:
                song_name = data_songs.split_midspace(song_name)    
            wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[2].text = song_name
            wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[1].text = data_songs.get_data_song(reproduction.queue[reproduction.i]) + " SR: 44100 - Stereo - mp3"   


class Media_menu_media_info(Screen):

    def __init__(self, **kwargs):
        super(Media_menu_media_info, self).__init__(**kwargs)
        ''' we declare a GridLayout instance that will be then added as 
        a child of Song_buttons class '''
        self.name = "Media_menu_media_info"
        self.state = "Not playing"
        self.song_name = "Nothing is playing right now"
        self.album = "Abum"
        self.singer = "Singer"
        self.year = "Year"
        GL = GridLayout()
        GL.rows = 3
        GL.padding = 5
        GL.spacing = 5
        self.ids['GL'] = GL
        song_label = Label(text = self.song_name, font_size = 32, size_hint = (1,0.3))
        album_label = Label(text = self.album + "-" + self.singer + "-" + self.year, size_hint = (1,0.3))
        GL.add_widget(song_label)
        GL.add_widget(album_label)
        controls = Media_menu_media_info_controls()
        GL.add_widget(controls)
        GL.ids['song_label'] = song_label
        self.add_widget(GL)

    def update_song_info(self,*args):
        self.song_name = args[0]
        self.ids['GL'].ids['song_label'].text = args[0]



class Media_menu_sd_songs(Screen):
    pass

class Media_menu_gui_sd_songs(Screen):
    pass
    
class Calls_menu_info(Screen):
    pass

class Calls_menu_recents(Screen):
    pass
    
class Media_menu_gui(Screen):
    pass

class Calls_menu_gui(Screen):
    pass

class Car_control_menu_gui(Screen):

    def emergency_lights(self):
        App.get_running_app().Emergency_lights = not App.get_running_app().Emergency_lights   
        GPIO.output(13,App.get_running_app().Emergency_lights)


class Bluetooth_menu_gui(Screen):
    pass

class Bt_menu_info(Screen):
    pass

class Bt_menu_device_select(Screen):
    pass
    
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("car_gui31.kv")

def update_temp(dt):
    wm = App.get_running_app().root
    new_temp = Temp.get_temperature(36)
    if "Error" not in new_temp:
        wm.ids.Main_menu_id.children[0].children[1].text = "Welcome to CIECS info center the temperature is {}".format(new_temp)

def check_reproduction_status(dt):
    reproduction = App.get_running_app().rep
    wm = App.get_running_app().root
    if reproduction.paused or not reproduction.reproducing:
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[1].background_normal = "images/play.png"
    else:
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[1].background_normal = "images/pause.png"

    fw = reproduction.check_status()
    

    if fw == 1 and len(reproduction.queue) > 0:
        song_name = usb_songs.dir_to_name(reproduction.queue[reproduction.i])
        if len(song_name) >= 20:
            song_name = data_songs.split_midspace(song_name)   
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[2].text = song_name
        wm.ids.Media_menu_id.children[0].children[0].children[0].children[0].children[0].children[1].text = data_songs.get_data_song(reproduction.queue[reproduction.i]) + " SR: 44100 - Stereo - mp3"        


def update_songs(dt):
    wm = App.get_running_app().root
    wm.ids.Media_menu_sd_songs_id.children[0].children[0].children[0].children[0].update_songs_buttons()

class MyApp(App):
    def build(self):
        Clock.schedule_interval(update_temp, 2)
        Clock.schedule_interval(update_songs,30)
        Clock.schedule_interval(check_reproduction_status, 1)
        self.rep = PMP3()
        self.Emergency_lights = False
        self.sunroof = False
        return kv


if __name__ == "__main__":
    MyApp().run()
    GPIO.output(13,False)
    GPIO.output(15,False)
    GPIO.output(16,False)
    GPIO.output(18,False)
    GPIO.output(22,False)
    time.sleep(0.5)

