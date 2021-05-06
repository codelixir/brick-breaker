import os
import platform

path = '../assets/sound_effect.mp3'


def play_sound():
    if platform.system() == 'Linux':
        os.system('aplay -q' + path + ' &')
    elif platform.system() == 'Darwin':
        os.system('afplay ' + path + ' &')
