import tensorflow as tf

model = tf.keras.models.load_model('model/model.h5')
with open('model/mu+std.txt') as f:
	mu = float(f.readline())
	std = float(f.readline())

data = [180, 240]

predictions = model.predict(data)
predictions = predictions * std + mu

dis = [5, 5, 5, 5, 1.0975, 3.9025, 5, 5, 5, 2.195]
times = predictions * dis
final_times = times.sum(axis=1)

print('Paces')
print(predictions)

print('\n\nFinal Times')
print(final_times)

model.summary()
