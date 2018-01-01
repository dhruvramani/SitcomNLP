import os
import time
import pickle
from datetime import datetime
#from pydub import AudioSegment
#from pydub.playback import play
import moviepy.editor as mp

def get_subsentence(timestep, filepath):
    with open(filepath, "r") as f:
        text = f.read().split("\n\n")
        for i in text:
            contents = i.split("\n")
            times = i[1].split(" --> ")
            timestr1, timestr2 = times[0].split(',')[0], times[1].split(',')[0]
            time1, time2 = datetime.strptime(timestr1, "%H:%M:%S"), datetime.strptime(timestr2, "%H:%M:%S")
            if(time1 <= timestep and timestep <= time2):
                return contents[2:]

def get_sentence(subsentence, filepath):
    with open(filepath, "r" ) as f:
        text = f.read().split("\n\n")
        return [sent for sent in text if subsentence in sent][0]


def vidtomp3(filename):
    # SOURCE : https://stackoverflow.com/questions/33448759/python-converting-video-to-audio
    clip = mp.VideoFileClip(filename)
    clip.audio.write_audiofile("{}_audio.mp3".format(filename))
    return "{}_audio.mp3".format(filename)

def vidtowav(filename):
    # SOURCE : https://stackoverflow.com/questions/26741116/python-extract-wav-from-video-file
    command = "ffmpeg -i ./data/videos/{}.mp4 -ab 160k -ac 2 -ar 44100 -vn ./data/audio/{}_audio.wav".format(filename, filename)
    os.system(command)
    return "./data/audio/{}_audio.wav".format(filename)

'''
def remvocal(filename):
    # SOURCE : https://stackoverflow.com/questions/3673042/algorithm-to-remove-vocal-from-sound-track
    myAudioFile = AudioSegment.from_mp3(filename)
    sound_stereo = AudioSegment.from_file(myAudioFile, format="mp3")
    sound_monoL = sound_stereo.split_to_mono()[0]
    sound_monoR = sound_stereo.split_to_mono()[1]
    sound_monoR_inv = sound_monoR.invert_phase()
    sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)
    sound_CentersOut.export("{}_novocal".format(filename), format="mp3")
    return "{}_novocal.mp3".format(filename)
'''

def detect_laughter(wavfilepath):

    return timesteps

def main(datasetpath, vidfilepath, subfilepath, transpath):
    wavpath = vidtowav(vidfilepath)
    timesteps = detect_laughter(wavfilepath)
    sentences = list()
    for timestep in timesteps:
        subsentences = get_subsentence(timestep, subfilepath)
        sentence = get_sentence(subsentences, transpath)
        sentences.append(sentence)

    with open(datasetpath, "w") as datf:
        with open(transpath, "r") as transf:
            for line in transf:
                if(line in sentences):
                    line = line.rstrip()
                    line += " LAUGH LAUGH\n"
                datf.write(line)

if __name__ == '__main__':
    wavpath = vidtowav("S08E01")