import numpy as np
import torch

from model import model

def predict(data, elevation=None, unit='ft'):
	model.load_state_dict(torch.load('model/model.pt'))

	with open('model/mu+std.txt') as f:
		mu = float(f.readline())
		std = float(f.readline())

	data = torch.tensor(data).unsqueeze(-1)
	predictions = model(data)
	predictions = (predictions * std + mu).detach().numpy() 

	dis_km = np.array([5, 5, 5, 5, 1.0975, 3.9025, 5, 5, 5, 2.195])
	dis_ft = dis_km * 3280.84
	CHANGE_PER_INCLINE = 13 / 60 # 13s per 1% incline

	if elevation:
		elevation = np.array(elevation)
		per = elevation / dis_km * 100 if unit == 'km' else elevation / dis_ft * 100

		speed_delta = per * CHANGE_PER_INCLINE
		predictions += speed_delta 
	
	# Scale predictions so total is under desired time
	total_times = np.sum(predictions * dis_km, axis=1)

	data = np.squeeze(data.numpy())
	scale_factor = np.expand_dims((data - 1) / total_times, axis=-1)
	predictions = np.multiply(predictions, scale_factor)
	
	return predictions 

def decimal_to_minutes(decimal):
	seconds = np.round((decimal * 60) % 60).astype(np.int8)
	minutes = np.floor(decimal).astype(np.int8)

	return minutes, seconds

data = [180.]
predictions = predict(data=data, elevation=[27, 39, -51, 20, 0, 8, -6, 2, -50, 40], unit='ft')

print(predictions)
print(decimal_to_minutes(predictions))
