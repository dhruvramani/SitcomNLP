import os
import re
import glob
import time
import pickle
from datetime import datetime
import moviepy.editor as mp

regex1 = re.compile(r'[^A-Za-z0-9\s]+')
regex2 = re.compile(r'\([^)]*\)')

def vidtomp3(filename):
    # SOURCE : https://stackoverflow.com/questions/33448759/python-converting-video-to-audio
    clip = mp.VideoFileClip(filename)
    clip.audio.write_audiofile("{}_audio.mp3".format(filename))
    return "{}_audio.mp3".format(filename)

def vidtowav(season, episode):
    # SOURCE : https://stackoverflow.com/questions/26741116/python-extract-wav-from-video-file
    command = "ffmpeg -i ./data/videos/BBTS0{}/{}x{}.mp4 -ab 160k -ac 2 -ar 44100 -vn ./data/audio/BBTS0{}/{}x{}.wav".format(season, season, episode, season, season, episode)
    os.system(command)

def detect_laughter(wavpath):
    command = "python ./laughter-detection/segment_laughter.py {} ./laughter-detection/models/new_model.h5 ./data/dump > ./data/laugh/{}.txt".format(wavpath, wavpath.split(".")[0])
    os.system(command)
    with open("./data/laugh/{}.txt".format(wavpath.split(".")[0]), "r") as f:
        return str(f.read()).replace('\'', '\"')

def deletesub(path):
    for i in glob.glob("{}*.srt".format(path)):
        if("xor" in i.lower() or "dvdrip" in i.lower()):
            print(i)
            os.system("sudo rm {}".format("\ ".join(i.split(" "))))

def formatsub(path):
    for i in glob.glob("{}*.srt".format(path)):
        name = i.split(" - ")[1]
        print(name)
        os.system("sudo mv {} {}{}.srt".format("\ ".join(i.split(" ")), path, name))

def get_sec(time_str):
    h, m, s = time_str.split(',')[0].split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def unicodetoascii(text):
    TEXT = (text.
            replace('\xe2\x80\x99', "'").
            replace('\xc3\xa9', 'e').
            replace('\xe2\x80\x90', '-').
            replace('\xe2\x80\x91', '-').
            replace('\xe2\x80\x92', '-').
            replace('\xe2\x80\x93', '-').
            replace('\xe2\x80\x94', '-').
            replace('\xe2\x80\x94', '-').
            replace('\xe2\x80\x98', "'").
            replace('\xe2\x80\x9b', "'").
            replace('\xe2\x80\x9c', '"').
            replace('\xe2\x80\x9c', '"').
            replace('\xe2\x80\x9d', '"').
            replace('\xe2\x80\x9e', '"').
            replace('\xe2\x80\x9f', '"').
            replace('\xe2\x80\xa6', '...').#
            replace('\xe2\x80\xb2', "'").
            replace('\xe2\x80\xb3', "'").
            replace('\xe2\x80\xb4', "'").
            replace('\xe2\x80\xb5', "'").
            replace('\xe2\x80\xb6', "'").
            replace('\xe2\x80\xb7', "'").
            replace('\xe2\x81\xba', "+").
            replace('\xe2\x81\xbb', "-").
            replace('\xe2\x81\xbc', "=").
            replace('\xe2\x81\xbd', "(").
            replace('\xe2\x81\xbe', ")")
                 )
    return TEXT

def get_demo():
    with open("./data/laugh/s08e01.txt", "r") as f:
        return str(f.read())

def format_string(strin):
    sentence = strin.lower()
    sentence = unicodetoascii(sentence)
    sentence = regex2.sub('', sentence)
    sentence = regex1.sub('', sentence)
    return sentence

def setup():
    _SEASONS = 9
    os.system("mkdir ./data")
    os.system("mkdir ./output")
    os.system("mkdir ./data/videos")
    os.system("mkdir ./data/transcripts")
    os.system("mkdir ./data/audio")
    os.system("mkdir ./data/dump")
    os.system("mkdir ./data/laugh")
    os.system("sudo apt-get install ffmpeg")
    os.system("pip install moviepy")
    os.system("git clone https://github.com/dhruvramani/laughter-detection")

    for season in range(1, _SEASONS + 1):
        os.system("mkdir ./data/videos/BBTS0{}".format(season))
        os.system("mkdir ./data/transcripts/BBTS0{}".format(season))
        os.system("mkdir ./data/audio/BBTS0{}".format(season))


if __name__ == '__main__':
    setup()