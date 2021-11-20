import torch
import torch.nn as nn
import torch.nn.functional as F


class BiLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output, device):
        super(BiLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.output = output
        self.device = device
        self.num_layers = num_layers
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True, bidirectional=True
        )
        self.fc = nn.Linear(hidden_size * 2, output)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)
        # print(h0.shape, c0.shape, x.shape)
        # return x
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


device = torch.device('cpu')

model = BiLSTM(
    input_size = 64,
    hidden_size = 256,
    num_layers = 2,
    output = 1,
    device = device
)

a1 = torch.randn(2394, 64)
a2 = torch.randn(4421, 64)
a3 = torch.randn(2558, 64)
a4 = torch.randn(1514, 64)
a5 = torch.randn(1984, 64)
a6 = torch.randn(2458, 64)
a7 = torch.randn(1875, 64)
a8 = torch.randn(1355, 64)

inp = torch.tensor([a1, a2, a3, a4, a5, a6, a7, a8])



print(model(inp).shape)


# # by default seq batch feature
# # if batch_first=true batch seq feature
# >>> rnn = nn.LSTM(10, 20, 2)
# >>> input = torch.randn(5, 3, 10)
# >>> h0 = torch.randn(2, 3, 20)
# >>> c0 = torch.randn(2, 3, 20)
# >>> output, (hn, cn) = rnn(input, (h0, c0))