import os
import glob
import time
import pickle
from datetime import datetime
import moviepy.editor as mp

def get_subsentence(timestep, subfilepath, laugh=False):
    with open(subfilepath, "r") as f:
        text = f.read().split("\n\n")
        for i in text:
            contents = i.split("\n")
            times = i[1].split(" --> ")
            timestr1, timestr2 = times[0].split(',')[0], times[1].split(',')[0]
            time1, time2 = datetime.strptime(timestr1, "%H:%M:%S"), datetime.strptime(timestr2, "%H:%M:%S")
            if(time1 <= timestep and timestep <= time2):
                return contents[2:]

def get_sentence(subsentence, transpath,laugh=False):
    with open(transpath, "r" ) as f:
        text = f.read().split("\n\n")
        sentence = [sent for sent in text if subsentence in sent][0]
        return sentence

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

def detect_laughter(wavpath):
    command = "python ./laughter-detection/segment_laughter.py {} ./laughter-detection/models/new_model.h5 ./data/dump > ./data/laugh/{}.txt".format(wavpath, wavpath.split(".")[0])
    os.system(command)
    with open("./data/laugh/{}.txt".format(wavpath.split(".")[0]), "r") as f:
        return str(f.read())

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


'''
def main(datasetpath, vidfilepath, subfilepath, transpath):
    wavpath = vidtowav(vidfilepath)
    timesteps = detect_laughter(wavpath)
    trans_time = timefortans(transpath, wavpath)
    sentences = list()
    for timestep in timesteps:
        subsentences = get_subsentence(timestep, subfilepath)
        sentence = get_sentence(subsentences, transpath)
        sentences.append(sentence)

    with open(datasetpath, "w") as datf:
        with open(transpath, "r") as transf:
            for line in transf:
                line = line.rstrip()
                #line +
                if(line in sentences):
                    line += " LAUGH"
                #line += 
                datf.write(line)
'''
if __name__ == '__main__':
    wavpath = vidtowav("S08E01")
    timefortrans("./data/transcripts/S08E01.txt", wavpath)
