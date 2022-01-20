import torch
from torch.utils.data import DataLoader
from torch import optim, nn

from dataset import FetchAudio
from models import BiLSTM


# setting the seeds for reproducing the results 
def seed_everything(seed):
	random.seed(seed)
	os.environ["PYTHONHASHSEED"] = str(seed)
	np.random.seed(seed)
	torch.manual_seed(seed)
	torch.cuda.manual_seed(seed)
	torch.backends.cudnn.deterministic = True
	torch.backends.cudnn.benchmark = False
seed_everything(CONFIG.seed)


class cnf:
	input_size = 64
	epochs = 5
	criterion = nn.MSELoss()
	optimizer = optim.Adam(model.parameters(), lr=CONFIG.cnn.learning_rate)
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


model = BiLSTM(
	input_size = 64, 
	hidden_size = 256, 
	num_layers = 2, 
	num_classes = 1,
	device = cnf.device,
).to(device=cnf.device)


for epoch in range(cnf.epochs):
	pass



