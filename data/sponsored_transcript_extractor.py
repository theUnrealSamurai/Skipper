import os 
import json
from re import sub
import numpy as np
import pandas as pd


sponsor_times = pd.read_csv("drive/MyDrive/sponsorTimes.csv")
transcripts = os.listdir("drive/MyDrive/transcripts")


### Filtering the videos for which transcripts and  sponsor times are available ###

transcripted_videoIDs = set([filename.strip(".json") for filename in transcripts])
sponsored_videoIDs = set(sponsor_times["videoID"])
transcripted_sponsored_videoIDs = list(sponsored_videoIDs.intersection(transcripted_videoIDs))

transcripted_sponsor_times = sponsor_times[sponsor_times["videoID"].isin(transcripted_sponsored_videoIDs)]


### Filtering sponsor times to have a single best submission instead of repeated submissions for a sponsor on a video ###

unique_videoID = transcripted_sponsor_times["videoID"].unique()

for videoID in unique_videoID:
    sponsor_segments = transcripted_sponsor_times[transcripted_sponsor_times["videoID"] == videoID].sort_values("startTime")
    pop_list = []
    best_submission = 0; 

    for iter in range(0, sponsor_segments.shape[0] - 1):
        if ((sponsor_segments.iloc[iter + 1]["startTime"] - sponsor_segments.iloc[best_submission]["startTime"]) < 6.0) or ((sponsor_segments.iloc[iter + 1]["endTime"] - sponsor_segments.iloc[best_submission]["endTime"]) < 6.0):
            if sponsor_segments.iloc[best_submission]["votes"] == sponsor_segments.iloc[iter + 1]["votes"]:
                if sponsor_segments.iloc[best_submission]["reputation"] == sponsor_segments.iloc[iter + 1]["reputation"]:
                    pop_list.append(best_submission)
                    best_submission = iter + 1
                else: 
                    if sponsor_segments.iloc[best_submission]["reputation"] > sponsor_segments.iloc[iter + 1]["reputation"]: 
                        pop_list.append(iter + 1)
                    else: 
                        pop_list.append(best_submission)
                        best_submission = iter + 1
            else: 
                if sponsor_segments.iloc[best_submission]["votes"] > sponsor_segments.iloc[iter + 1]["votes"]: 
                    pop_list.append(iter + 1)
                else: 
                    pop_list.append(best_submission)
                    best_submission = iter + 1
        else:
            best_submission = iter + 1 

    transcripted_sponsor_times.drop(sponsor_segments.index[pop_list], inplace=True)


### Transcript extraction for each segment on each video and file dump ###

sponsor_transcripts = []

for videoID in unique_videoID:
    transcript_item = {'videoID': videoID}
    transcript = pd.read_json(f"drive/MyDrive/transcripts/{videoID}.json")
    transcript['start'] = round(transcript['start'])
    sponsor_transcript_for_video = []

    for index in transcripted_sponsor_times[transcripted_sponsor_times["videoID"] == videoID].index:
        start_time = round(transcripted_sponsor_times["startTime"][index])
        end_time = round(transcripted_sponsor_times["endTime"][index])
        
        sponsor_transcript_for_video.append("".join(transcript[(transcript['start'] >= start_time) & (transcript['start'] < end_time)]['text']).replace("\n", " "))

    transcript_item['sponsorTranscripts'] = sponsor_transcript_for_video
    sponsor_transcripts.append(transcript_item)    

with open("sponsor_transcripts.json", "w") as json_file:
    json.dump(sponsor_transcripts, json_file)