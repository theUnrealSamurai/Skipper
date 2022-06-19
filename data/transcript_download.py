import json
import pandas as pd
from tqdm import tqdm
import time
from youtube_transcript_api import YouTubeTranscriptApi

df = pd.read_csv('sponsorTimes.csv')

videoIds = df['videoID'].unique()

for video_id in tqdm(videoIds):
    try:
        #time.sleep(0.25)
        json_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        with open(f'transcripts/{video_id}.json', 'w') as f:
            json.dump(json_transcript,f)
        print(video_id)
    except:
        pass
