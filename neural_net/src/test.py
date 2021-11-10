import pandas as pd

df = pd.read_csv("../../data/merged_df.csv", index_col="video_id")
print(df.loc["pq42IyO6Ah0"])