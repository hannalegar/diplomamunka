#region imports

import methods
import pandas as pd
import numpy as np

#endregion

df = pd.read_excel("original_df.xlsx", sheet_name="Sheet1")
df.drop(['Unnamed: 0'], axis = 1, inplace=True)

# df.fillna(-999).equals(original_df.fillna(-999))

#region modify dataframe

df.replace(np.NaN, "", inplace=True)

drop_indexes = df[df['erzelem'] == 'U'].index
df.drop(drop_indexes, inplace=True)

drop_indexes = df[df['erzelem'] == '_ANONYMIZED_'].index
df.drop(drop_indexes, inplace=True)

drop_indexes = df[df['erzelem'] == 'erzelem'].index
df.drop(drop_indexes, inplace=True)

df2 = df

# cols = list(df2.columns.values)

df2 = df2[['textGrid',
            "erzelem",
            'diszpecscer',
            'diszpecser',
            'diszpecser 2',
            'diszpecser 3',
            'diszpecser1',
            'diszpecser2',
            'diszpecser3',
            'szerelo',
            'ugyfel',
            'ugyfel1',
            'ugyfel2',
            'uygfeé']]

df = df2

df

#endregion

#region split original dataframe into two dataframe

ugyfel_df = df[['textGrid',
            "erzelem",
            'ugyfel',
            'ugyfel1',
            'ugyfel2',
            'uygfeé']]

diszpecser_df = df[['textGrid',
            "erzelem",
            'diszpecscer',
            'diszpecser',
            'diszpecser 2',
            'diszpecser 3',
            'diszpecser1',
            'diszpecser2',
            'diszpecser3',
            'szerelo']]

ugyfel_df
diszpecser_df

ugyfel_df["All"] = ugyfel_df[ugyfel_df.columns[2:]].apply(
    lambda x: '/'.join(x.dropna().astype(str)), axis = 1)
ugyfel_df["All"]

diszpecser_df["All"] = diszpecser_df[diszpecser_df.columns[2:]].apply(
    lambda x: '/'.join(x.dropna().astype(str)), axis = 1)
diszpecser_df["All"]

ugyfel_df = ugyfel_df[['textGrid', "erzelem", "All"]]
diszpecser_df = diszpecser_df[['textGrid', "erzelem", "All"]]

# ugyfel_df.head(10)
# diszpecser_df.head(10)

drop_indexes = ugyfel_df[ugyfel_df['All'] == '///'].index
ugyfel_df.drop(drop_indexes, inplace=True)
ugyfel_df.head(10)

drop_indexes = diszpecser_df[diszpecser_df['All'] == '///////'].index
diszpecser_df.drop(drop_indexes, inplace=True)
diszpecser_df.head(10)

replace_chars = ["/",
                 "(",
                 ")",
                 ","
                ]

for char in replace_chars:
    print(char)
    ugyfel_df['All'] = ugyfel_df['All'].str.replace(char,'')    
    diszpecser_df['All'] = diszpecser_df['All'].str.replace(char,'')

ugyfel_df
diszpecser_df

#endregion

#region make text and target list

ugyfelList = ugyfel_df['All'].tolist()
diszpecserList = diszpecser_df['All'].tolist()

texts = ugyfelList + diszpecserList

#make target list
ugyfelTargetList = ugyfel_df['erzelem'].tolist()
diszpecserTargetList = diszpecser_df['erzelem'].tolist() 

toDistinct = ['N\t\t\t', 'E ', 'N ', 'NN', ' N', 'N\t', 'N0']
expected = ['N', 'E', 'N', 'N', 'N', 'N', 'N']

for i in range(0, len(toDistinct)):
    diszpecserTargetList = replace_element(diszpecserTargetList, toDistinct[i], expected[i])
    ugyfelTargetList = replace_element(ugyfelTargetList, toDistinct[i], expected[i])

# ugyfelTargetList
# diszpecserTargetList
# 
# distinct_ugyfel = list(set(ugyfelTargetList))
# distinct_ugyfel
# 
# distinct_diszpecser = list(set(diszpecserTargetList))
# distinct_diszpecser

target = ugyfelTargetList + diszpecserTargetList
# target
# len(target)
# 
# len(target) == len(texts)

with open("texts.txt", "w") as texts_outfile:
    texts_outfile.write("\n".join(texts))

with open("target.txt", "w") as target_outfile:
    target_outfile.write("\n".join(target))

#endregion