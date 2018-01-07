import os
from __future__ import print_function

# TODO if not found go to next 4 words
def get_timestamp(subtext, to_search):
    try :
        return [x for x in subtext if to_search in x][0].split("\n")[1].split(" --> ")
    except :
        return ["-1", "-1"]
        
def search_words(sentence):
    init_timestamp, end_timestamp = "-1", "-1"
    words = sent.split(" ")
    word_count = 4
    while("-1" in [init_timestamp, end_timestamp]):
        starting, ending = " ".join(words[:word_count]), " ".join(words[-word_count:])
        init_timestamp = get_timestamp(subtext, starting)[0]
        end_timestamp = get_timestamp(subtext, ending)[1]
        word_count -= 1
    return init_timestamp, end_timestamp

def transcripttimestamp(transpath, subpath, newpath):
    """Returns a dictionary of format dict[sentence] = [initial_timestamp, ending_timestamp, speaker]

       Keyword arguments:
       transpath - path to your transcript file
       subpath   - path to your subtitle file
       newpath   - path to store the info in the format
    """
    output = dict()
    with open(transpath, "r") as trans:
        with open(subpath, "r") as sub:
            transtext = str(trans.read()).split("\n\n")
            subtext = str(sub.read()).split("\n\n")
            init_timestamp, end_timestamp = "-1", "-1"

            for sent in transtext:
                sent = sent.split(":")[1].lstrip().rstrip()
                speaker = sent.split(":")[0]
                if(len(sent) <= 4):
                    init_timestamp, end_timestamp = get_timestamp(subtext, sent)
                    output[sent] = [init_timestamp, end_timestamp, speaker]
                elif(len(sent) < 250):
                    init_timestamp, end_timestamp = search_words(sent)
                    output[sent] = [init_timestamp, end_timestamp, speaker]
                else :
                    subsentences = sent.split(".")
                    old_init, old_end = search_words(subsentences[0])
                    wholesent, reset = subsentences[0], 0
                    for subsent in subsentences[1:]:
                        new_init, new_end = search_words(subsent)
                        if(reset == 1):
                            old_init, old_end = new_init, new_end
                            wholesent = subsent
                            reset = 0
                        if(int(new_init.split(":")[2]) - int(old_end.split(":")[2]) >= 1):
                            init_timestamp, end_timestamp = old_init, new_end
                            output[wholesent] = [init_timestamp, end_timestamp, speaker]
                            reset = 1
                        else :
                            old_end = new_end
                            wholesent += ". " + subsent

    with open(newpath, "w+") as new:
        for key, values in output.items():
            new.write("{} : {} | {} | {}".format(values[2], key, values[0], values[1]))
            
    return output
