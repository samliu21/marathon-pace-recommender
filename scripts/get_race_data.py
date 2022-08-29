import pandas as pd
import matplotlib.pyplot as plt

df_2014 = pd.read_csv('../data/2014-cleaned.csv')
df_2015 = pd.read_csv('../data/2015-cleaned.csv')
df_2016 = pd.read_csv('../data/2016-cleaned.csv')
df_2017 = pd.read_csv('../data/2017-cleaned.csv')
df_2018 = pd.read_csv('../data/2018-cleaned.csv')
df_2019 = pd.read_csv('../data/2019-cleaned.csv')

def create_key(df, df_idx):
	if df_idx >= df.shape[0]:
		return 'OUT_OF_RANGE'

	s = df.iloc[df_idx]
	return s['Name'] + s['City']

def increment_index(base_key, df, df_idx):
	key = create_key(df, df_idx)
	while key < base_key and key != 'OUT_OF_RANGE':
		df_idx += 1
		key = create_key(df=df, df_idx=df_idx)

	return df_idx

def time_to_seconds(t):
	nums = list(map(int, t.split(':')))
	return nums[0] * 3600 + nums[1] * 60 + nums[2]

def check_matching(base_key, df, df_idx, matching):
	df_idx = increment_index(base_key=base_key, df=df, df_idx=df_idx)
	key = create_key(df=df, df_idx=df_idx)

	if base_key == key:
		matching.append(df.iloc[df_idx])
	return df_idx

novel_races = []
poor_races = []

five, six, seven, eight, nine = 0, 0, 0, 0, 0
cnt = 0

for four in range(df_2014.shape[0]):
	four_key = create_key(df_2014, four) # Unique key to distinguish runners
	matching = []

	five = check_matching(base_key=four_key, df=df_2015, df_idx=five, matching=matching)
	six = check_matching(base_key=four_key, df=df_2016, df_idx=six, matching=matching)
	seven = check_matching(base_key=four_key, df=df_2017, df_idx=seven, matching=matching)
	eight = check_matching(base_key=four_key, df=df_2018, df_idx=eight, matching=matching)
	nine = check_matching(base_key=four_key, df=df_2019, df_idx=nine, matching=matching)
	
	if len(matching) >= 1:
		matching.insert(0, df_2016.iloc[six])
		finish_times = list(map(time_to_seconds, [year['Official Time'] for year in matching])) # Times in seconds

		if max(finish_times) - min(finish_times) > 600:
			cnt += 1
			if cnt % 100 == 0:
				print('Found {} matches...'.format(cnt))

			novel_races.append(matching[finish_times.index(min(finish_times))])
			poor_races.append(matching[finish_times.index(max(finish_times))])
	
	if seven >= df_2017.shape[0] and eight >= df_2018.shape[0] and nine >= df_2019.shape[0]:
		break

print('Number of novel and poor races:  {}'.format(len(novel_races)))
pd.DataFrame(novel_races).to_csv('../data/novel-races.csv', index=False)
pd.DataFrame(poor_races).to_csv('../data/poor-races.csv', index=False)

times = [time_to_seconds(race['Official Time']) / 60. for race in novel_races]
plt.hist(times)
plt.show()

