from langdetect import detect
import pandas as pd

df = pd.read_csv('/home/jd/work/skipper/data/videoInfo.csv')

title = df['title']

print(title.head())