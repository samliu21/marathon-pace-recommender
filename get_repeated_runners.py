import pandas as pd

df_2016 = pd.read_csv('2016-sorted.csv')
df_2017 = pd.read_csv('2017-sorted.csv')
df_2018 = pd.read_csv('2018-sorted.csv')
df_2019 = pd.read_csv('2019-sorted.csv')

def save(df, name):
	"""
	Saves df to csv file with name "name"
	"""
	df.to_csv(name, index=False)

def sort_and_drop(df):
	"""
	Sorts rows of the df by name, then city in place
	Then, drops unnecessary columns
	"""
	df.sort_values(by=['Name', 'City'], inplace=True)
	df.drop(columns=['Bib', 'Country', 'Projected Time', 'Gender', 'Division'], inplace=True)

def check_unique_name_city(df):
	"""
	Checks whether the athletes in a sorted df can be uniquely represented by their name and city
	If so, does nothing
	If not, throws exception with the iloc of the first of the two runners, then returns
	"""
	for i in range(df.shape[0] - 1):
		s = df.iloc[i]
		sp = df.iloc[i + 1]

		if s['Name'] == sp['Name'] and s['City'] == sp['City']:
			raise Exception(i)

def drop_nonunique_name_city(df):
	"""
	Removes all runners that cannot be uniquely represented by their name and city
	"""
	number_of_removals = 0 

	while 1:
		try:
			check_unique_name_city(df=df)
			break
		except Exception as e:
			r = int(str(e))  

			print('Dropping rows {} and {}\nCommon name: {}, city: {}...'.format(r, r + 1, df.iloc[r]['Name'], df.iloc[r]['City']))
			df.drop(index=df.iloc[r : r + 2].index, inplace=True) # index keyword relies on no row number in .csv file

			number_of_removals += 2
			continue

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

if __name__ == '__main__':
	pass
