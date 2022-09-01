import torch

from model import model

model.load_state_dict(torch.load('model/model.pt'))

with open('model/mu+std.txt') as f:
	mu = float(f.readline())
	std = float(f.readline())

data = [180., 240.,]
data = torch.tensor(data).unsqueeze(-1)

predictions = model(data)
predictions = predictions * std + mu 
print(predictions)
