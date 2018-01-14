import os
import re

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

regex1 = re.compile(r'[^A-Za-z0-9\s]+')
regex2 = re.compile(r'\([^)]*\)')
# TODO if not found go to next 4 words
def format_string(strin):
    sentence = strin.lower()
    sentence = unicodetoascii(sentence)
    sentence = regex2.sub('', sentence)
    sentence = regex1.sub('', sentence)
    return sentence

def get_timestamp(subtext, to_search):
    try :
        x = [x for x in subtext if to_search in format_string(" ".join(x.split("\n")[2:]))][0]
        return x.split("\n")[1].split(" --> ")
    except:
        return ["-1", "-1"]
        
def search_words(sentence, subtext):
    sentence = format_string(sentence)
    init_timestamp, end_timestamp = "-1", "-1"
    word_count = 7
    words = sentence.split(" ")
    ending = ""
    while("-1" == init_timestamp and word_count > 1):
        starting = " ".join(words[:word_count])
        #print(" | ".join([sentence, starting, ending]), "\n\n")
        init_timestamp = get_timestamp(subtext, starting)[0]
        word_count -= 1

    word_count = 7
    words = sentence.split(" ")
    while("-1" == end_timestamp and word_count > 1):
        ending = " ".join(words[-word_count:])
        print(ending)
        end_timestamp = get_timestamp(subtext, ending)[1]
        word_count -= 1

    if(init_timestamp == "-1" or end_timestamp == "-1"):
        return "-1", "-1", -1, -1
    #init_timestamp, end_timestamp = init_timestamp.split(",")[0], end_timestamp.split(",")[0]
    start_ind = [subtext.index(x) for x in subtext if init_timestamp in x][-1]
    final_ind = [subtext.index(x) for x in subtext if end_timestamp in x][-1]

    return init_timestamp, end_timestamp, start_ind, final_ind

# CHANGE : subtitle -> text -> till text : subtitle
def transcripttimestamp(transpath, subpath, newpath):
    """Returns a dictionary of format dict[sentence] = [initial_timestamp, ending_timestamp, speaker]

       Keyword arguments:
       transpath - path to your transcript file
       subpath   - path to your subtitle file
       newpath   - path to store the info in the format
    """
    output = list()
    with open(transpath, "r") as trans:
        with open(subpath, "r") as sub:
            transtext = str(trans.read()).split("\n\n")
            subtext = str(sub.read()).split("\n\n")
            #init_timestamp, end_timestamp = "-1", "-1"
            new = open("./new.txt", "w+")
            for senti in transtext:
                if(":" not in senti):
                    continue
                sent = senti.split(":")[1].lstrip().rstrip()
                if(len(sent.split(" ")) <= 4):
                    pass
                else :
                    foo, bar, start_ind, final_ind = search_words(sent, subtext)
                    if(-1 in [start_ind, final_ind]):
                        continue
                    old_init, old_end = subtext[start_ind].split("\n")[1].split(" --> ")
                    reset, count, wholesent = 0, 0, " ".join([x for x in subtext[start_ind].split("\n")[2:] if x in sent])
                    speaker = senti.split(":")[0]
                    #print(senti, foo, bar, end="\n\n")
                    for i in range(start_ind + 1, final_ind + 1):
                        new_init, new_end = subtext[i].split("\n")[1].split(" --> ")
                        sec1, sec2 = int(new_init.split(":")[2].split(",")[0]), int(old_end.split(":")[2].split(",")[0])
                        if(sec1 - sec2 >= 1):
                            init_timestamp, end_timestamp = old_init, old_end
                            speaker = senti.split(":")[0]
                            to_put = [speaker, wholesent, init_timestamp, end_timestamp]
                            new.write("{}\n\n".format(to_put))
                            #output.append(to_put)
                            #print(to_put, speaker)
                            wholesent = " ".join(subtext[i].split("\n")[2:])
                            old_init, old_end = new_init, new_end
                        else :
                            wholesent += " " + " ".join(subtext[i].split("\n")[2:])
                            old_end = new_end
                    
                    init_timestamp, end_timestamp = old_init, old_end
                    speaker = senti.split(":")[0]
                    to_put = [speaker, wholesent, init_timestamp, end_timestamp]
                    new.write("{}\n\n".format(to_put))
                    #output.append()
                    wholesent = ""
            new.close()



    ##with open(newpath, "w+") as new:
    ##    new.write("\n\n".join([" | ".join(sent) for sent in output]))
            
    return output

if __name__ == '__main__':
    transpath = "./data/transcripts/FS02E02.txt"                                                                                                                
    subpath = "./data/subtitles/FS02E02.srt"                                                                                                                    
    newpath = "./new.txt"  
    os.system("rm -rf {}".format(newpath))                                                                                                                              
    transcripttimestamp(transpath, subpath, newpath)