#region imports

import pandas as pd

#endregion

text_and_label_df2 = pd.read_excel("text_and_label_df.xlsx", sheet_name="Sheet1")
text_and_label_df2.drop(['Unnamed: 0'], axis = 1, inplace=True)

# text_and_label_df.equals(text_and_label_df2)