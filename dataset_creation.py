import os
import pickle
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp
from sound_classification import SoundClassification

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

def detect_laughter(wavfile, train=False):
    
    _SOUND_OBJ = "./models/sco.sav"
    _DATSET_PATH = "./data/laugh_dataset"

    if(train == False):
        sco = pickle.load(open(_SOUND_OBJ), "rb")
    else:
        file_regexp = os.path.join(_DATSET_PATH, '*.wav')
        files = glob.glob(file_regexp)
        sco = SoundClassification(wav_file_list=files, calibrate_score=True)
        sco.learn()
        pickle.dump(sco, open(_SOUND_OBJ, "wb"))

    res = sco.processed_wav(wavfile)
    print([x for x in res])

if __name__ == '__main__':
    wavpath = vidtowav("S08E01")
    detect_laughter(wavpath, True)