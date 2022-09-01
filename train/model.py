import torch

model = torch.nn.Sequential(
	torch.nn.Linear(1, 1),
	torch.nn.ReLU(),
	torch.nn.Linear(1, 16),
	torch.nn.ReLU(),
	torch.nn.Linear(16, 32),
	torch.nn.ReLU(),
	torch.nn.Linear(32, 10),
)

loss_func = torch.nn.MSELoss()
optimizer = torch.optim.Adam(params=model.parameters(),)
