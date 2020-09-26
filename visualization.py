import seaborn as sns
import pandas as pd
import methods

preprocessed_df = pd.read_excel("preprocessed.xlsx", sheet_name="Sheet1")
preprocessed_df.head(15)

sns.set(style="darkgrid")

labels_with_n = pd.DataFrame(preprocessed_df,  columns =['Label'])
labels_without_n = pd.DataFrame([i for i in preprocessed_df['Label'] if i != "N"], columns=['Label'])

methods.simple_barplot(labels_with_n, "Distribution of labels includes N")
methods.simple_barplot(labels_without_n, "Distribution of labels without N")


preprocessed_df.head(15)