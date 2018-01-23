import os
import re
import csv
import json
from utils import detect_laughter, format_string, get_sec, get_demo

count = 1
def modifylaugh(csvpath, newpath):
    with open(newpath, "w+") as new:
        fields = ['ID', 'SEASON', 'EPISODE', 'SPEAKER', 'SENTENCE', 'STARTING TIMESTAMP', 'ENDING TIMESTAMP', 'LAUGH']
        writer = csv.writer(new, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)                                                                                                                 
        writer.writerow(fields)
        laughfile, old_wav = None, ""
    
        with open(csvpath, "r") as cf:
            readCSV = csv.reader(cf, delimiter=',')
            previnit = ""
            for row in readCSV:
                _, season, episode, _, _, init_timestamp, end_timestamp = row
                init_t, end_t = get_sec(init_timestamp), get_sec(end_timestamp)
                wavpath = "./data/laughwav/BBTS0{}/{}x{}.wav".format(season, season, episode)
                if('ID' in row):
                    continue
                if(laughfile == None or old_wav != wavpath):
                    laughjson = detect_laughter(wavpath) #get_demo() 
                    laughfile = laughjson.split("\n")[1:]
                laugh = False

                if(previnit == ""):
                    previnit = init_t
                    continue

                for i in laughfile:
                    jsondat = json.loads(i)
                    start, end = float(jsondat['start']), float(jsondat['end'])
                    if((start > previnit and start < init_t) or (end > previnit and end < init_t)):
                        laugh = True
                        break

                row.append(laugh)
                writer.writerow(row)
                previnit = init_t
                old_wav = wavpath

def get_timestamp(subtext, to_search):
    try :
        x =  [x for x in subtext if to_search in format_string(" ".join(x.split("\n")[2:]))][0]
        return x.split("\n")[1].split(" --> ")
    except:
        return ["-1", "-1"]

def search_words(sentence, subtext):
    sentence = format_string(sentence)
    init_timestamp, end_timestamp = "-1", "-1"
    word_count = 7
    words = sentence.split(" ")
    ending = ""
    while("-1" in [init_timestamp, end_timestamp] and word_count > 1):
        starting = " ".join(words[:word_count])
        ending = " ".join(words[-word_count:])
        try :
            if(init_timestamp == "-1"):
                init_timestamp = get_timestamp(subtext, starting)[0]
            if(end_timestamp == "-1"):
                end_timestamp = get_timestamp(subtext, ending)[1]
            word_count -= 1
        except :
            return "-1", "-1", -1, -1

    if(init_timestamp == "-1" or end_timestamp == "-1"):
        return "-1", "-1", -1, -1

    start_ind = [subtext.index(x) for x in subtext if init_timestamp in x][-1]
    final_ind = [subtext.index(x) for x in subtext if end_timestamp in x][-1]

    return init_timestamp, end_timestamp, start_ind, final_ind

def transcripttimestamp(season, episode, newpath):
    """Returns a dictionary of format dict[sentence] = [initial_timestamp, ending_timestamp, speaker]

       Keyword arguments:
       transpath - path to your transcript file
       subpath   - path to your subtitle file
       newpath   - path to store the info in the format
    """
    global count
    output = list()
    print(season, episode)
    transpath = "./data/transcripts/raw_corpus/{}_{}.txt".format(season, episode)                                                                                                              
    subpath = "./data/subtitles/BBTS0{}/{}x{}.srt".format(season, season, episode) 
    with open(transpath, "r") as trans:
        with open(subpath, "r", encoding = "ISO-8859-1") as sub:
            transtext = str(trans.read()).split("\n")
            subtext = str(sub.read()).split("\n\n")
            new = open(newpath, "a+")
            writer = csv.writer(new, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            for senti in transtext:
                if(":" not in senti or 'scene' in senti.lower()):
                    continue
                sent = senti.split(":")[1].lstrip().rstrip()
                if(len(sent.split(" ")) <= 8):
                    pass
                else :
                    _, _, start_ind, final_ind = search_words(sent, subtext)
                    if(-1 in [start_ind, final_ind]):
                        continue
                    try :
                        old_init, old_end = subtext[start_ind].split("\n")[1].split(" --> ")
                        reset, wholesent = 0, " ".join([x for x in subtext[start_ind].split("\n")[2:] if x in sent])
                        speaker = senti.split(":")[0]
                        for i in range(start_ind + 1, final_ind + 1):
                            new_init, new_end = subtext[i].split("\n")[1].split(" --> ")
                            sec1, sec2 = int(new_init.split(":")[2].split(",")[0]), int(old_end.split(":")[2].split(",")[0])
                            if(sec1 - sec2 >= 1):
                                init_timestamp, end_timestamp = old_init, old_end
                                speaker = senti.split(":")[0]
                                to_put = [count, season, episode, speaker, wholesent, init_timestamp, end_timestamp]
                                writer.writerow(to_put)
                                count += 1
                                wholesent = " ".join(subtext[i].split("\n")[2:])
                                old_init, old_end = new_init, new_end
                            else :
                                wholesent += " " + " ".join(subtext[i].split("\n")[2:])
                                old_end = new_end
                    except :
                        continue
                    
                    init_timestamp, end_timestamp = old_init, old_end
                    speaker = senti.split(":")[0]
                    to_put = [count, season, episode, speaker, wholesent, init_timestamp, end_timestamp]
                    writer.writerow(to_put)
                    count += 1
                    wholesent = ""
            new.close()
    return output

if __name__ == '__main__':
    _SEASONS = 9
    _EPISODES = [17, 23, 23, 24, 24, 22, 24, 24, 24]
    fields = ['ID', 'SEASON', 'EPISODE', 'SPEAKER', 'SENTENCE', 'STARTING TIMESTAMP', 'ENDING TIMESTAMP']
    newpath = "./output/new_bbt.csv" 
    laughpath = "./output/new_bbt-laugh.csv" 
    
    with open(newpath, "w+") as new:
        writer = csv.writer(new, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)                                                                                                                 
        writer.writerow(fields)

    for season in range(1, _SEASONS + 1):
        for episode in range(1, _EPISODES[season - 1] + 1):                                                                                                                    
            transcripttimestamp(season, episode, newpath)

    modifylaugh(newpath, laughpath)

    '''
    # Demo
    fields = ['ID', 'SEASON', 'EPISODE', 'SPEAKER', 'SENTENCE', 'STARTING TIMESTAMP', 'ENDING TIMESTAMP']
    newpath = "./output/s08e01.csv"  
    path2 = "./output/s08e01-laugh.csv"
    
    with open(newpath, "w+") as new:
        writer = csv.writer(new, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)                                                                                                                 
        writer.writerow(fields)
    
    transcripttimestamp(8, 1, newpath)
    modifylaugh(newpath, path2)
    '''