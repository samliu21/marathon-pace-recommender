import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

ndf = pd.read_csv('../data/novel-races.csv')
pdf = pd.read_csv('../data/poor-races.csv')

def time_to_seconds(t):
	nums = list(map(int, t.split(':')))
	return nums[0] * 3600 + nums[1] * 60 + nums[2]

def extract_times(df):
	cols = df.columns[list(range(5, 14)) + [15]]
	print(cols)

	dfp = df[cols].applymap(time_to_seconds)
	dfp = (dfp / 60).round(1)

	dfp.columns = cols 
	return dfp

novel = extract_times(ndf)
poor = extract_times(pdf)

poor = poor.mul(1 / poor['Official Time'], axis=0).mul(novel['Official Time'], axis=0)
poor = poor.round(1)

print(novel.mean())
print(poor.mean())
