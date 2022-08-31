import sys

import pandas as pd
import tensorflow as tf

from model import model 

df = pd.read_csv('../data/novel-races.csv')

# Convert time to seconds
def time_to_seconds(t):
	nums = list(map(int, t.split(':')))
	return nums[0] * 3600 + nums[1] * 60 + nums[2]

# Get the columns of df that represent times
# [5k, 10k, ..., Total time]
def extract_times(df):
	cols = df.columns[list(range(6, 15)) + [4]]

	dfp = df[cols].applymap(time_to_seconds)
	dfp = (dfp / 60).round(1)
	dfp.columns = cols 

	return dfp

# Calculate the pace travelled within a distance block
# E.g. the pace under 30k is the average pace between 25k and 30k
def convert_minutes_to_pace(s):
	dis = [5, 10, 15, 20, 21.0975, 25, 30, 35, 40, 42.195]

	for i in range(len(dis) - 1, -1, -1):
		s[i] = s[i] / dis[i] if i == 0 else (s[i] - s[i - 1]) / (dis[i] - dis[i - 1])
	return s 

time_df = extract_times(df)

pace_df = time_df.copy()
pace_df = pace_df.apply(convert_minutes_to_pace, axis=1)

# Remove people who went out too fast (e.g. fastest time is more than 1.25 km/min faster than slowest time)
SLOWED_DOWN_THRESHOLD = 1.25
for i in range(pace_df.shape[0] - 1, -1, -1):
	if pace_df.iloc[i].max() - pace_df.iloc[i].min() > SLOWED_DOWN_THRESHOLD:
		pace_df.drop([i], inplace=True)
		time_df.drop([i], inplace=True)

_stack = pace_df.stack() # Used to get mu and std of whole df
mu = _stack.mean()
std = _stack.std() 

x = time_df['time_full']
y = (pace_df - mu) / std
EPOCHS = 1000
early_stop = tf.keras.callbacks.EarlyStopping(
	patience=25, 
	restore_best_weights=True,
)

model.fit( # shuffle=True and batch_size=32 by default
	x=x,
	y=y, 
	epochs=EPOCHS,
	validation_split=0.1,
	callbacks=[early_stop],
)

model.save('model.h5', overwrite=True,)