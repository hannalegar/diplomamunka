import re
import keras
import seaborn as sns
from keras.preprocessing import sequence 
from nltk.corpus import stopwords

stop_words = set(stopwords.words("Hungarian"))

def write_to_file(path, text):
        f = open("files/" + path,"w") 

        for i in text:
            for j in i:
                f.write(j + '\n')

        f.close()

def interval_names(path):
        f = open(path, "r")
        lines = f.readlines()
        
        names = [re.findall(r'"([^"]*)"', l)[0] for l in lines if "name" in l]
        
        f.close()

        return names

def read(path):
        names_results = interval_names(path)
        names_results.append("vege")

        text_lists = list()
        min_list = list()
        max_list = list()

        for name in names_results:
            l = list()
            l.append(name)
            text_lists.append(l)

        find_texts(path, names_results, text_lists, min_list, max_list)
        min_list, max_list = normalize_intervals(text_lists, min_list, max_list)

        return text_lists, names_results, min_list, max_list

def find_texts(path, names, text_lists, min_list, max_list):
        f = open(path, "r")
        line = f.readline()

        i = 0
        while names[i] != "vege" and i < len(names):
            line = process(line, f, names[i+1], i, text_lists, min_list, max_list)
            i += 1    

        f.close()

def process(line, f, next_name, index, text_lists, min_list, max_list):
        l = line
        while l and next_name not in l:
            if 'text' in l:
                text_lists[index].append(re.findall(r'"([^"]*)"', l)[0])
            if 'xmin' in l:
                length = len(l.split())
                min_list.append(l.split()[length-1])
            if 'xmax' in l:
                length = len(l.split())
                max_list.append(l.split()[length-1])
            l = f.readline()
        return l

def normalize_intervals(text_list, min_list, max_list):
    normalized_mins = list()
    normalized_maxs = list()
    for i in range(len(text_list[0]) -1):
        normalized_mins.append(min_list[i+2])
        normalized_maxs.append(max_list[i+2])

    return normalized_mins, normalized_maxs

def to_dataframe(df, interval_names, lista, name, mins, maxs):  
        index = 0
        for i in range(0, len(interval_names)):
            if interval_names[i] != 'vege':
                df.insert(i, interval_names[i], lista[i], True)
            index = i
        df.insert(index, "textGrid", name, False)

        mins.insert(0, 'xmin')
        maxs.insert(0, 'xmax')

        df.insert(1, "xmin", mins, True)
        df.insert(2, "xmax", maxs, True)

        return df

def replace_element(my_list, old_value, new_value):
        for n, i in enumerate(my_list):
            if i == old_value:
                my_list[n] = new_value
        return my_list

def split_senteces_into_words(text):
    return keras.preprocessing.text.text_to_word_sequence(text,
                                               filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                               lower=True,
                                               split=" ")    

def stop_word_filtering(sentence):
    filtered = []
    for w in sentence:
        if w not in stop_words:
            filtered.append(w)
    return filtered

def encode(text, tokenizer):
    return [tokenizer.word_index[i] for i in text]

def decode(encoded_text, rwm):
    print(' '.join(rwm[id] for id in encoded_text))

char_toNum_switcher = {
        "S" : 0,
        "N" : 1,
        "P" : 2
}

num_toChar_switcher = {
         0: "S",
         1: "N",
         2: "P"
}

def simple_barplot(label, title):
    sns.countplot(x="Label", data=label).set(title=title)

def stringarray_to_array(st):
    # print(st)
    res = st[st.find("[")+1:st.rfind("]")].translate({ord('\''): None}).split(',')

    # print(len(res))
    return res

def to_array(s):
    res = [int(i) for i in  stringarray_to_array(s)]
    return res

def to_float_array(s):
    res = [float(i) for i in stringarray_to_array(s)]
    return res