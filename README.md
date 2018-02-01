# SitcomnNLP

## Dataset Creation Setup
Run `utils.py` to create the respective directories, and unzip the `subtitles`, and put it in the data folder. 

All the data goes into the `data/` folder.
Put all the videos in `data/videos/`, transcripts in `data/transcripts/` and subtitles in `data/subtitles/`. Aditionally, create directories `data/audio/`, `data/dump`, `data/laugh`.

All the data (videos, transcripts and subtitles) are to be seperated by seasons, and each season has a directory of the name `BBTS0{seasonNumber}` in each of the folders. And all of the content has to be stored in the format `{SeasonNumber}x{EpisodeNumber}.{FileFormat}`.

```
data 
|__ subtitles
|   |___ BBTS01
|   |    |___ 1x1.srt
|   |    |___ 1x2.srt
|   |         .......
|   |__ BBTS02
|   |    |___ 2x1.srt
|   |    |___ 2x2.srt
|   |         .......
|   ......
|
|_ transcripts
|  |___ BBTS01
|  |      |___ 1x1.txt
|  |      |___ 1x2.txt
|  |          .......
|  | ......
|
|_ videos
|  |___ BBTS01
|       ......
|_ audio
|  |___ BBTS01
|       ......
|_ dump
```

Create directory `output/` .

## Dataset Creation
To create the dataset, run main.py
```shell
python(3?) main.py
```
The output is : `./output/new_bbt-laugh.csv`.