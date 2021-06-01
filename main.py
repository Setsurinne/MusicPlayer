from math import nan
import tkinter
import random
import music
import OS_File
'''
from tkinter import ttk
from tkinter import Entry
from tkinter import messagebox
from tkinter import PhotoImage
import threading
import sys
import time
import re
import os
'''


music_dir_file = "MusicPlayer\\music_dir.txt"
music_dir = []
music_dir_updated = False

musics = []
index_of_music = nan

play_list = []
index_in_list = nan

play_mode = 0

track = music.music()
on_play = False
paused = False



## ----------------------------------------------------------------------------
# Music play list operation
def update_play_list(music_index):
    global play_list
    if (len(play_list) >= 20):
        play_list.pop(0)

    play_list.append(music_index)

# Find next music index due to different mode and push into playlist
def push_music_tolist():
    global musics
    global play_list

    next_index = 0
    if (play_mode == 0):
        if (len(play_list) == 0):
            next_index = 0

        else:
            if (play_list[-1] == len(musics) - 1):
                next_index = 0
            else:
                next_index = play_list[-1] + 1 

    elif (play_mode == 1):
        next_index = random.randint(0, len(musics))
    
    update_play_list(next_index)
    return

def go_next():
    global index_in_list
    global index_of_music
    if (index_in_list == len(play_list) - 1 or len(play_list) == 0):
        push_music_tolist()
        index_in_list = len(play_list) - 1

    else:
        index_in_list += 1

    index_of_music = play_list[index_in_list]
    return True

def go_prev():
    global index_in_list
    global index_of_music
    if (len(play_list) == 0 or index_in_list == 0):
        return False
    else:
        index_in_list -= 1
        index_of_music = play_list[index_in_list]
    return True

## ----------------------------------------------------------------------------
# Music play operation
def show_Playingmusic_inlist():
    global index_of_music
    music_list.activate(index_of_music)
    music_list.see(index_of_music)


# Play music
#   Will do:
#       1. Play the music in Musics[index_of_music]
#       2. Check the state of 'prev' buttom
#       3. Scroll down the list_box of musics
#       4. Show name of current music
def play_Music():
    global on_play
    global paused
    on_play = True
    paused = False

    paused_text.set('')
    play_button_info.set('Pause')  

    if(len(play_list) == 0):
        go_next()

    print(play_list)
    print(index_of_music)

    music_path = musics[index_of_music]
    parse_Music_Info(music_path)
    check_prev_state()
    show_Playingmusic_inlist()
    track.play(music_path)


# Command when click play buttom
    # Call Play or Pause due to different situation
def play_on_click():
    if (not on_play):
        play_Music()
    else:
        show_pause()


# Pause the music and show information
def show_pause():
    global paused
    global on_play
    if paused:
        track.unpause()
        play_button_info.set('Pause')      
        paused_text.set('')
    else:
        track.pause()
        play_button_info.set('Continue')  
        paused_text.set('Paused')
    paused = not paused


# Play the music when double click music name in ListBox
def play_By_click(self):
    global index_of_music
    global index_in_list
    global play_list
    index_of_music = music_list.curselection()[0]

    if (len(play_list) != 0):
        play_list = play_list[ : index_in_list + 1]
        update_play_list(index_of_music)
        index_in_list = len(play_list) - 1
    else:
        play_list = [index_of_music]
        index_in_list = 0

    play_Music()


# Play next music
#   Will update index and play_list first and call play function
def play_Next():
    go_next()
    play_Music()


def play_Prev():
    if (go_prev() == False):
        pass
    else:
        play_Music()



def scale_Volume(self):
    track.setVolume(float(vol_scale.get())/100.00)

# Change the mode of playing
def change_Mode():
    global play_mode
    global mode_info

    MODE = ["Normal","Random"]
    if (play_mode == len(MODE) - 1):
        play_mode = 0
    else:
        play_mode += 1
    
    mode_info.set(MODE[play_mode])


def parse_Music_Info(path):
    global music_name
    music_name.set(path[path.find('\\') + 1 : ])
    '''
    global music_length
    info = MediaInfo.parse(path).to_json()
    rst=re.search('other_duration.*?(.*?)min(.*?)s.*?',info)
    min=int(rst.group(0)[19:20])
    sec=int(rst.group(0)[-4:-2])
    music_length.set(str(min) + ':' + str(sec))
    total_time = (min*60+sec)*1000
    '''



# Check if exists previous music to play
#   If yes, the pre buttom will be set state = 'normal' otherwise 'disabled'
def check_prev_state():
    if (len(play_list) == 0 or index_in_list < 1):
        prev_button['state'] = 'disabled'
    else:
        prev_button['state'] = 'normal'

# Function that check if current music end
#   If yes, automatically play next music
def auto_next():
    if(on_play == True and track.onPlay() == False):
        print("Next...")
        play_Next()
    interface.after(1000,auto_next)

## ----------------------------------------------------------------------------
# Interface
interface = tkinter.Tk()
interface.title("Setsurinne's Music Player!")

interface_length = 1000
interface_height = 600
interface.geometry('{:d}x{:d}'.format(interface_length, interface_height))


musicPath = "C:/Users/15253/Desktop/PY/MusicPlayer/music.mp3"
musicFolder = "E:/CloudMusic"
musics += OS_File.readMusicFromFolder(musicFolder)


# Music Name Label
music_name = tkinter.StringVar()
music_name.set('No music playing...')
music_name_label = tkinter.Label(interface, font = ('Arial', 14), textvariable = music_name)
music_name_label.place(x = interface_length * 1 / 3, y = interface_height * 10 / 12)

# Paused Label; rightcorner
paused_text = tkinter.StringVar()
paused_label = tkinter.Label(interface, font =  ('Arial', 9), textvariable = paused_text)
paused_label.place(rely=1.0, relx=1.0, x = 0, y = 0, anchor='se')


# Play/Pause/Continue Buttom
play_button_info = tkinter.StringVar()
play_button_info.set('Play Music')
play_button = tkinter.Button(interface, 
                            textvariable = play_button_info, 
                            font = ('Arial', 12), 
                            fg = 'DarkCyan',
                            width = 10, height = 1, 
                            command = play_on_click)
play_button.place(x = interface_length / 2, y = interface_height * 9/10)

# Next Buttom
next_button = tkinter.Button(interface, 
                            text = "next", 
                            font = ('Arial', 12), 
                            fg = 'DarkCyan',
                            width = 10, height = 1, 
                            command = play_Next)
next_button.place(x = interface_length * 2 / 3, y = interface_height * 9/10)

# Prev Buttom
prev_button = tkinter.Button(interface, 
                            text = "prev", 
                            font = ('Arial', 12), 
                            fg = 'DarkCyan',
                            state = 'disabled',
                            width = 10, height = 1, 
                            command = play_Prev)

prev_button.place(x = interface_length / 3, y = interface_height * 9/10)

# Mode Buttom
mode_info = tkinter.StringVar()
mode_info.set("Normal")
#random_img = tkinter.PhotoImage("Images\\Random.png", height = 50, width=50)
#normal_img = tkinter.PhotoImage("Images\\Normal.png", height = 50, width=50)
mode_button = tkinter.Button(interface, 
                            textvariable = mode_info, 
                            font = ('Arial', 12),
                            fg = 'DarkCyan',
                            relief="solid", 
                            
                            command = change_Mode)
mode_button.place(x = interface_length / 6, y = interface_height * 9/10)

# Volume Bar
vol_scale = tkinter.Scale(interface, 
                            label = "Volume", 
                            from_= 100, to = 0, 
                            resolution = 1, 
                            orient = tkinter.VERTICAL, 
                            length = interface_height / 3, 
                            command = scale_Volume)
vol_scale.set(50)
vol_scale.place(x = interface_length * 1 / 20, y = interface_height * 3/5)

# Frame for the Music list
music_list_frame = tkinter.Frame()
music_list_frame.pack()

# Scroll for the List
music_list_scroll = tkinter.Scrollbar(music_list_frame)
music_list_scroll.pack(side = 'right', fill = 'y')


# List of Music
music_list = tkinter.Listbox(music_list_frame, 
                            width = int(interface_length * 1/12), 
                            height = int(interface_height * 1/22), 
                            yscrollcommand = music_list_scroll.set)
music_list.bind('<Double-Button-1>', play_By_click)
for item in musics:
    music_list.insert("end", item[item.find('\\') + 1 : ])

music_list.pack()
music_list_scroll.config(command = music_list.yview)


interface.after(1000,auto_next)
interface.mainloop()