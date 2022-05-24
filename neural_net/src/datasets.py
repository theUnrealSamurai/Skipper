import torch
import torchaudio
import pandas as pd
from torch.utils.data import Dataset
from glob import glob


class FetchAudio(Dataset):
	"""docstring for FetchAudio"""
	def __init__(self, 
			path_to_csv = '../../data/merged_df.csv', 
			path_to_dir = "../../data/train",
			SAMPLE_RATE = 22050,
		):

		super(FetchAudio, self).__init__()
		self.audio_paths = glob(path_to_dir + "/*.mp3")
		self.df = pd.read_csv(path_to_csv, index_col="video_id")
		self.SAMPLE_RATE = SAMPLE_RATE
		self.transformation = torchaudio.transforms.MelSpectrogram(
			sample_rate=SAMPLE_RATE,
			n_fft=1024,
			hop_length=512,
			n_mels=64)


	def __len__(self):
		return len(self.audio_paths)


	def __getitem__(self, idx):
		audio_path = self.audio_paths[idx]
		audio_id = audio_path.split(" - ")[-1].split('.')[-2]
		signal, sr = torchaudio.load(audio_path)

		if sr != self.SAMPLE_RATE:
			resampler = torchaudio.transforms.Resample(sr, self.SAMPLE_RATE)
			signal = resampler(signal)

		if signal.shape[0] > 1:
			signal = torch.mean(signal, dim=0, keepdim=True)

		mel_spectrogram = self.transformation(signal)

		return {"spectrogram": mel_spectrogram[0], 
				"start_seconds": self.df.loc[audio_id].start_seconds,
				"end_seconds": self.df.loc[audio_id].end_seconds,
				"time_difference": self.df.loc[audio_id].time_diff
				}


if __name__ == "__main__":
	dset = FetchAudio()
	print(dset[0])		