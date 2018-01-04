#mkdir data
mkdir data/videos
mkdir data/audio
mkdir data/dump
#mkdir data/testi
#touch data/testi/laughtime.txt
#touch data/testi/transtime.txt
mkdir data/subtitles

sudo apt-get install ffmpeg
pip install moviepy
git clone https://github.com/dhruvramani/laughter-detection
git clone https://github.com/lowerquality/gentle
echo "Save videos in data/videos, subtitles in data/subtitles and transcripts in data/transcripts"