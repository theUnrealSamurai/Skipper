import pandas as pd 
from glob import glob


def time_difference(start, end):
	"""Returns the time difference between 2 times.
	Start and end should be string formatted in mm:ss"""
	def str_to_sec(time):
		a, b = time.split(":")
		return (int(a)*60) + int(b)
	start = start.apply(str_to_sec)
	end = end.apply(str_to_sec)
	return end-start


def preprocess(df_path):
	"""Dropping the empty rows and a little Feature Engineering"""
	df = pd.read_csv(df_path)
	df = df[["Video Link", "[1] Start Time", "[1] End Time"]]
	df.dropna(inplace=True)
	#  Any new feature to be added goes here in this function.
	df["time_diff"] = time_difference(df["[1] Start Time"], df["[1] End Time"])
	df["Video_id"] = df["Video Link"].apply(lambda x: x.split('=')[-1])
	return df



if __name__ == '__main__':
	
	"""The program loops through all the csv's in the folder,
	Adds few features,
	then merges all the csv's into one single file.
	"""
	csvs = glob("*.csv")
	merged_df = pd.DataFrame()


	for df in csvs:
		if df == "merged_df.csv": continue
		df = preprocess(df)
		if not merged_df.empty:
			merged_df = merged_df.append(df)
		else:
			merged_df = df

	merged_df.to_csv("merged_df.csv", index=False)

