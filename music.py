from os import error
import pygame
import Message

class music(object):

    def __init__(self):
        pygame.mixer.init()
    
    def play(self, music_path):
        try:
            pygame.mixer.music.load(music_path)
            if(pygame.mixer.music.get_busy()):
                return Message.BUSY

            pygame.mixer.music.play()
            return Message.PLAY

        except Exception as error:
            print(type(error))
            print(error)
            return Message.PATHERROR
    
    def pause(self):
        pygame.mixer.music.pause()
        return Message.PAUSE

    def unpause(self):
        pygame.mixer.music.unpause()
        return Message.UNPAUSE

    def stop(self):
        pygame.mixer.music.stop()
        return 

    def setVolume(self, vol):
        pygame.mixer.music.set_volume(vol)
        return Message.SET_VOL
    
    def onPlay(self):
        return pygame.mixer.music.get_busy()
    
    def step(self, sec):
        pygame.mixer.music.set_pos(sec)
        return
    
    def playTime(self):
        return pygame.mixer.music.get_pos()