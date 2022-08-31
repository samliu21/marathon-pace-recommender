import pandas as pd
import matplotlib.pyplot as plt

df_2010 = pd.read_csv('../data/berlin-2010-cleaned.csv')
df_2011 = pd.read_csv('../data/berlin-2011-cleaned.csv')
df_2012 = pd.read_csv('../data/berlin-2012-cleaned.csv')
df_2013 = pd.read_csv('../data/berlin-2013-cleaned.csv')
df_2014 = pd.read_csv('../data/berlin-2014-cleaned.csv')
df_2015 = pd.read_csv('../data/berlin-2015-cleaned.csv')
df_2016 = pd.read_csv('../data/berlin-2016-cleaned.csv')
df_2017 = pd.read_csv('../data/berlin-2017-cleaned.csv')
df_2018 = pd.read_csv('../data/berlin-2018-cleaned.csv')
df_2019 = pd.read_csv('../data/berlin-2019-cleaned.csv')

# Create unique key based on individual's name and nationality
def create_key(df, df_idx):
	if df_idx >= df.shape[0]:
		return 'OUT_OF_RANGE'

	s = df.iloc[df_idx]
	return s['first_name'] + s['last_name'] + str(s['nationality'])

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
one, two, three, four, five, six, seven, eight, nine = 0, 0, 0, 0, 0, 0, 0, 0, 0
cnt = 0

for zero in range(df_2010.shape[0]):
	zero_key = create_key(df_2010, zero) # Unique key to distinguish runners
	matching = []

	one = check_matching(base_key=zero_key, df=df_2011, df_idx=one, matching=matching)
	two = check_matching(base_key=zero_key, df=df_2012, df_idx=two, matching=matching)
	three = check_matching(base_key=zero_key, df=df_2013, df_idx=three, matching=matching)
	four = check_matching(base_key=zero_key, df=df_2014, df_idx=four, matching=matching)
	five = check_matching(base_key=zero_key, df=df_2015, df_idx=five, matching=matching)
	six = check_matching(base_key=zero_key, df=df_2016, df_idx=six, matching=matching)
	seven = check_matching(base_key=zero_key, df=df_2017, df_idx=seven, matching=matching)
	eight = check_matching(base_key=zero_key, df=df_2018, df_idx=eight, matching=matching)
	nine = check_matching(base_key=zero_key, df=df_2019, df_idx=nine, matching=matching)
	
	if len(matching) >= 1:
		matching.insert(0, df_2010.iloc[zero])
		finish_times = list(map(time_to_seconds, [year['time_full'] for year in matching])) # Times in seconds

		if max(finish_times) - min(finish_times) > 1800:
			cnt += 1
			if cnt % 100 == 0:
				print('Found {} matches...'.format(cnt))

			novel_races.append(matching[finish_times.index(min(finish_times))])

print('Number of novel races:  {}'.format(len(novel_races)))
pd.DataFrame(novel_races).to_csv('../data/novel-races.csv', index=False)

times = [time_to_seconds(race['time_full']) / 60. for race in novel_races]
plt.hist(times)
plt.show()
