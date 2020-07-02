import pandas as pd

df = pd.read_excel("original_df.xlsx", sheet_name="Sheet1")
df.drop(['Unnamed: 0'], axis = 1, inplace=True)

# df.fillna(-999).equals(original_df.fillna(-999))