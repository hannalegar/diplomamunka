#region imports

import methods
import re
import ftplib
import io
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

#endregion

#region download texts

hostname = 'berber.tmit.bme.hu'
username = 'mtuba'
passw = 'BA5qKB'

ftp = ftplib.FTP(hostname)
ftp.login(username, passw)

for d in ftp.nlst():
    if d == '10':
        for f in ftp.nlst(d):
            if f.endswith("425.TextGrid") or f.endswith("447.TextGrid") or f.endswith("448.TextGrid"):
                continue
            if f.endswith(".TextGrid"):
                r = io.BytesIO()
                print(f.split('/')[1])
                ftp.retrbinary('RETR ' + f, r.write)
                info = r.getvalue().decode(encoding="utf-8")            
                splits = info.split('\n')
                methods.write_to_file(f.split('/')[1], [s.split('\n') for s in splits])
                r.close()

#endregion

#region merge into dataframe

path = "files/"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlyfiles

original_df = pd.DataFrame()

wrong_files = ["0160.TextGrid",
        "0167.TextGrid",
        "0185.TextGrid",
        "0191.TextGrid",
        "0205.TextGrid",
        "0331.TextGrid",
        "0413.TextGrid",
        "0551.TextGrid",
        "0605.TextGrid",
        "0617.TextGrid",
        "0619.TextGrid",
        "0662.TextGrid",
        "0760.TextGrid"
        ]

for i in onlyfiles:
    print(i)
    if i in wrong_files:
        continue
    
    l, names, mins, maxs = methods.read(path + i)
    temp_df = pd.DataFrame()

    temp_df = methods.to_dataframe(temp_df, names, l, i, mins, maxs)
    original_df = pd.concat([original_df, temp_df]).reset_index(drop = True)

original_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
original_df

original_df.to_excel("original_df.xlsx") 

#endregion