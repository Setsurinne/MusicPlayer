from music import music
import OS_File

import tkinter
from tkinter import messagebox
from tkinter import filedialog

music_dir_file = "MusicPlayer\\music_dir.txt"
music_dir = []
music_dir_updated = False

## ----------------------------------------------------------------------------
# Read music and modify music dir
def initialize():
    global music_dir
    global musics
    music_dir = OS_File.readDir(music_dir_file)
    if (music_dir == []):
        result = messagebox.askquestion(title = 'No musiic', message = "Add some dir of music to play?") 
        if (result == 'no'):
            exit()   
        mod_Music_Dir()
    else:
        musics = OS_File.readMusicFromList(music_dir)


def read_music():
    global music_dir
    global musics
    music_dir = OS_File.readDir(music_dir_file)
    musics = OS_File.readMusicFromList(music_dir)


def add_Dir():
    global music_dir
    global music_dir_updated

    folder_path = filedialog.askdirectory()
    print(folder_path)
    if folder_path in music_dir:
        messagebox.showinfo(message = "Dir already existed!")        
    else:
        music_dir.append(folder_path)
        music_dir_updated = True


def mod_Music_Dir():
    global music_dir_updated

    top = tkinter.Toplevel()
    top.title("modify dir of music")

    dir_list_box = tkinter.Listbox(top)    
    dir_list_box.pack()

    for dir in music_dir:
        dir_list_box.insert(dir, 'end')

    dir_button = tkinter.Button(top, text = "Find dir", command = add_Dir)

    dir_button.pack()

    return