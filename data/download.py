from __future__ import unicode_literals
from multiprocessing import Pool
import os
import pandas as pd 
import youtube_dl


class download_config():
    """ Configuration for the Download Parameters """

    input_file = 'test_file.csv'    # Input .csv file location

    start_point = 0                 # Selects the download start point. Replace `0` with the exact line number from the .csv file for the download that you want to start with. 
    # (Default Value: 0 - Starts at the start of the .csv file)

    stop_point = None               # Selects the download end point. Replace `None` with the exact line number from the .csv file for the download that you want to end with. 
    # (Default Value: None - Stops at the end of the values in the .csv file)
    
    # YouTubeDL Download Options
    options = {
        'postprocessors': [{
            'key': "FFmpegExtractAudio",
            'preferredcodec': "mp3",
            'preferredquality': "192",
            'nopostoverwrites': True,
        }],
        'outtmpl': f'train/%(title)s - %(id)s.%(ext)s',
        'nooverwrites': True,
        'sleep_interval': 2,
        'max_sleep_interval': 5, 
        'progress_hooks': [lambda download: print(f"ERROR: {download['filename'].replace(f'train/', '')}") if (download['status'] == 'error') else (print(f"DOWNLOAD SUCCESSFUL: {download['filename'].replace(f'train/', '')}") if (download['status'] == 'finished') else "")],
    }

    def start_from(df):
        """ Corrects for the intended value of starting download """

        start_point = download_config.start_point

        if start_point == 0: 
            start_point = 0
        elif start_point > 1 and start_point < (len(df)+2):
            start_point-=2
        else: 
            print("ERROR: Invalid starting value. Number greater than 1 and lesser than the length of the input .csv file expected!")

        return start_point
    
    def stop_at(df): 
        """ Corrects for the intended value of stopping download """
        stop_point = download_config.stop_point

        if stop_point is None: 
            stop_point = len(df)
        elif stop_point > 1 and stop_point < (len(df)+2):
            stop_point-=1
        else: 
            print("ERROR: Invalid stopping value. Number greater than 1 and lesser than the length of the input .csv file expected!")       

        return stop_point          
    
def youtube_downloader(url):
    """ Downloads the audio from YouTube as per configuration for each URL with the corresponding filename """

    try: 
        options['format'] = 'm4a'
        YouTubeDL = youtube_dl.YoutubeDL(options)
        YouTubeDL.download([url])
    except:
        options['format'] = 'bestaudio/best'
        YouTubeDL = youtube_dl.YoutubeDL(options)
        YouTubeDL.download([url])

def parallel_compute(download_list):
    """ Runs the youtube_downloader as parallel processes for each video """

    pool = Pool(processes=len(download_list))
    pool.map(youtube_downloader, download_list)


# Comment/Uncomment/Modify this line depending on whether the file is run as a Python Script or an .ipynb on Colab/Kaggle
# os.chdir('/content/drive/MyDrive/Colab Notebooks/Skipper/data')
df = pd.read_csv(download_config.input_file)

start_from, stop_at, options = download_config.start_from(df), download_config.stop_at(df), download_config.options
YouTubeDL = youtube_dl.YoutubeDL(options)
download_list = [download['Video Link'] for download in df.iloc[start_from:stop_at].to_dict('records') if download['[1] Start Time'] == download['[1] Start Time']]

if len(download_list) > 0: 
    parallel_compute(download_list)
else: 
    print("There are no files matching the specified configuration OR the files you are trying to download already exist. In that case, please delete the files, and try again.")