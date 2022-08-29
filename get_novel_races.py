import pandas as pd
import matplotlib.pyplot as plt

df_2016 = pd.read_csv('data/2016-sorted-notnull.csv')
df_2017 = pd.read_csv('data/2017-sorted-notnull.csv')
df_2018 = pd.read_csv('data/2018-sorted-notnull.csv')
df_2019 = pd.read_csv('data/2019-sorted-notnull.csv')

def get_repeated_runners():
	def create_key(df, idx):
		if idx >= df.shape[0]:
			return 'OUT_OF_RANGE'

		s = df.iloc[idx]
		try:
			return s['Name'] + s['City']
		except:
			print(s)
			raise

	def increment_index(six_key, df, idx):
		key = create_key(df, idx)
		while key < six_key and key != 'OUT_OF_RANGE':
			idx += 1
			key = create_key(df, idx)

		return idx

	def time_to_seconds(t):
		nums = list(map(int, t.split(':')))
		return nums[0] * 3600 + nums[1] * 60 + nums[2]

	novel_races = []
	seven, eight, nine = 0, 0, 0
	cnt = 0

	for six in range(df_2016.shape[0]):
		six_key = create_key(df_2016, six) # Unique key to distinguish runners
		matching = []

		seven = increment_index(six_key, df_2017, seven)
		if six_key == create_key(df_2017, seven):
			matching.append(df_2017.iloc[seven])
		
		eight = increment_index(six_key, df_2018, eight)
		if six_key == create_key(df_2018, eight):
			matching.append(df_2018.iloc[eight])	

		nine = increment_index(six_key, df_2019, nine)
		if six_key == create_key(df_2019, nine):
			matching.append(df_2019.iloc[nine])

		if len(matching) > 1:
			matching.insert(0, df_2016.iloc[six])
			finish_times = list(map(time_to_seconds, [year['Official Time'] for year in matching])) # Times in seconds

			for i in range(len(finish_times)):
				if finish_times[i] - min(finish_times) > 600:
					cnt += 1
					if cnt % 100 == 0:
						print('Found {} matches...'.format(cnt))

					novel_races.append(matching[i])
		
		if seven >= df_2017.shape[0] and eight >= df_2018.shape[0] and nine >= df_2019.shape[0]:
			break

	print('Number of repeat runners (3+):  {}'.format(len(novel_races)))
	pd.DataFrame(novel_races).to_csv('data/novel_races.csv', index=False)

	times = [time_to_seconds(race['Official Time']) / 60. for race in novel_races]
	plt.hist(times)
	plt.show()

if __name__ == '__main__':
	get_repeated_runners()
