import tensorflow as tf

model = tf.keras.Sequential([ 
	tf.keras.layers.Normalization(),
	tf.keras.layers.Dense(1, activation='relu'),
	tf.keras.layers.Dense(32, activation='relu'),
	tf.keras.layers.Dense(64, activation='relu'),
	tf.keras.layers.Dense(10),
])

LR = 0.0001

model.compile(
	optimizer=tf.keras.optimizers.Adam(LR), 
	loss='mse',
)