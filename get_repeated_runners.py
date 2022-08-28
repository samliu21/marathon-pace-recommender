import pandas as pd

df_2016 = pd.read_csv('2016-sorted.csv')
df_2017 = pd.read_csv('2017-sorted.csv')
df_2018 = pd.read_csv('2018-sorted.csv')
df_2019 = pd.read_csv('2019-sorted.csv')

def sort_and_save(df, name):
	df.sort_values(by=['Name', 'City', 'Age'], inplace=True)
	df.drop(columns=['Bib', 'Country', 'Projected Time', 'Gender', 'Division'], inplace=True)

	df.to_csv(name, index=False)

def check_unique_name_city(df):
	for i in range(df.shape[0] - 1):
		s = df.iloc[i]
		sp = df.iloc[i + 1]

		if s['Name'] == sp['Name'] and s['City'] == sp['City']:
			raise Exception('Non-unique at index {}'.format(i))

def get_repeated_runners():
	def create_key(df, idx):
		s = df.iloc[idx]
		return s['Name'] + s['City']

	def increment_index(six_key, df, idx):
		key = create_key(df, idx)
		while key < six_key:
			idx += 1
			key = create_key(df, idx)

		return idx

	repeated_runners = []
	seven, eight, nine = 0, 0, 0

	for six in range(df_2016.shape[0]):
		six_key = create_key(df_2016, six) # Unique key to distinguish runners
		matching = []

		seven = increment_index(six_key, df_2017, seven)
		if six_key == create_key(df_2017, seven):
			matching.append(7)
		
		eight = increment_index(six_key, df_2018, eight)
		if six_key == create_key(df_2018, eight):
			matching.append(8)	

		nine = increment_index(six_key, df_2019, nine)
		if six_key == create_key(df_2019, nine):
			matching.append(9)

sort_and_save(df_2016, name='2016-sorted.csv')

if __name__ == '__main__':
	pass
