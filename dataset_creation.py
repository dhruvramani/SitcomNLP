import os
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp

def vidtomp3(filename):
    # SOURCE : https://stackoverflow.com/questions/33448759/python-converting-video-to-audio
    clip = mp.VideoFileClip(filename)
    clip.audio.write_audiofile("{}_audio.mp3".format(filename))
    return "{}_audio.mp3".format(filename)

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




