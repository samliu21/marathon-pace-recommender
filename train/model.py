import tensorflow as tf

model = tf.keras.Sequential([ 
	tf.keras.layers.Normalization(),
	tf.keras.layers.Dense(1, activation='relu'),
	tf.keras.layers.Dense(16, activation='relu'),
	tf.keras.layers.Dense(32, activation='relu'),
	tf.keras.layers.Dense(10),
])

model.compile(
	optimizer='adam',
	loss='mse',
)