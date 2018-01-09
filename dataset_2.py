import os

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

# TODO if not found go to next 4 words
def get_timestamp(subtext, to_search):
    try :
        x =  [x for x in subtext if unicodetoascii(to_search) in " ".join(x.split("\n")[2:])][0]
        return x.split("\n")[1].split(" --> ")
    except :
        return ["-1", "-1"]
        
def search_words(sentence, subtext):
    sentence = unicodetoascii(sentence)
    init_timestamp, end_timestamp = "-1", "-1"
    word_count = 7
    words = sentence.split(" ")
    ending = ""
    while("-1" in [init_timestamp, end_timestamp] and word_count > 1):
        starting = " ".join(words[:word_count])
        ending = " ".join(words[-word_count:])
        if(init_timestamp == "-1"):
            init_timestamp = get_timestamp(subtext, starting)[0]
        if(end_timestamp == "-1"):
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

            for sent in transtext:
                speaker = sent.split(":")[0]
                sent = sent.split(":")[1].lstrip().rstrip()
                if(len(sent.split(" ")) <= 4):
                    pass
                else :
                    _, _, start_ind, final_ind = search_words(sent, subtext)
                    if(-1 in [start_ind, final_ind]):
                        continue
                    old_init, old_end = subtext[start_ind].split("\n")[1].split(" --> ")
                    reset, count, wholesent = 0, 0, " ".join([x for x in subtext[start_ind].split("\n")[2:] if x in sent])
                    for i in range(start_ind + 1, final_ind + 1):
                        new_init, new_end = subtext[i].split("\n")[1].split(" --> ")
                        sec1, sec2 = int(new_init.split(":")[2].split(",")[0]), int(old_end.split(":")[2].split(",")[0])
                        if(sec1 - sec2 >= 1):
                            init_timestamp, end_timestamp = old_init, old_end
                            output.append([speaker, wholesent, init_timestamp, end_timestamp])
                            wholesent = " ".join(subtext[i].split("\n")[2:])
                            old_init, old_end = new_init, new_end
                        else :
                            wholesent += " " + " ".join(subtext[i].split("\n")[2:])
                            old_end = new_end
                    
                    init_timestamp, end_timestamp = old_init, old_end
                    output.append([speaker, wholesent, init_timestamp, end_timestamp])
                    wholesent = ""



    with open(newpath, "w+") as new:
        new.write("\n\n".join([" | ".join(sent) for sent in output]))
            
    return output

if __name__ == '__main__':
    transpath = "./data/transcripts/S08E01.txt"                                                                                                                
    subpath = "./data/subtitles/s08e01.srt"                                                                                                                    
    newpath = "./new.txt"  
    os.system("rm -rf {}".format(newpath))                                                                                                                              
    transcripttimestamp(transpath, subpath, newpath)