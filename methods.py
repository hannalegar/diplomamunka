import re

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

def process(line, f, next_name, index, lists):
        l = line
        while l and next_name not in l:
            if 'text' in l:
                lists[index].append(re.findall(r'"([^"]*)"', l)[0])
            l = f.readline()
        return l

def find_texts(path, names, lists):
        f = open(path, "r")
        line = f.readline()

        i = 0
        while names[i] != "vege" and i < len(names):
            line = process(line, f, names[i+1], i, lists)
            i += 1    

        f.close()

def read(path):
        names_results = interval_names(path)
        names_results.append("vege")

        lists = list()

        for name in names_results:
            l = list()
            l.append(name)
            lists.append(l)

        find_texts(path, names_results, lists)

        return lists, names_results

def to_dataframe(df, interval_names, lista, name):  
        index = 0
        for i in range(0, len(interval_names)):
            if interval_names[i] != 'vege':
                df.insert(i, interval_names[i], lista[i], True)
            index = i
        df.insert(index, "textGrid", name, False)
        return df