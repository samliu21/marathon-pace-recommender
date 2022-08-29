import getopt
import pandas as pandas
import sys

# Save df as csv with name "name"
def save(df, name):
	df.to_csv(name, index=False)

# Sort rows of df by athlete name and city in place, then drop unnecessary columns
def sort_name_city(df):
	df.sort_values(by=['Name', 'City'], inplace=True)

# Drop unnecessary columns
def drop_unnecessary_cols(df):
	df.drop(columns=['Bib', 'Country', 'Projected Time', 'Gender', 'Division'], inplace=True)	

# Removes all runners that cannot be uniquely represented by their name and city
def drop_nonunique_name_city(df):
	# Checks whether athletes in a sorted df can be uniquely represented by name and city
	# If check fails, the function throws exception with iloc of the first of the two runners, then returns
	def check_unique_name_city(df):
		for i in range(df.shape[0] - 1):
			s = df.iloc[i]
			sp = df.iloc[i + 1]

			if s['Name'] == sp['Name'] and s['City'] == sp['City']:
				raise Exception(i)

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

# Drop any rows that contain "-" null keyword
def drop_null(df):
	null_rows = df.isin(['-',]).any(axis=1)
	null_rows = null_rows[null_rows == True]

	print('{} rows dropped...'.format(df.shape[0] - null_rows.shape[0]))
	df.drop(null_rows.index, inplace=True)

if __name__ == '__main__':
	argv = sys.argv[1:]

	valid_args = ['-dropcol', 'dropnull', '-sort', '-unique', '-save', '-all']
	mp = {
		'-dropcol': drop_unnecessary_cols,
		'-dropnull': drop_null,
		'-sort': sort_name_city,
		'-unique': drop_nonunique_name_city,
		'-save': save,
	}

	# Check args are valid
	for arg in argv: 
		if arg not in valid_args:
			raise Exception('Invalid argument {}.\nValid arguments are {}'.format(arg, valid_args))

	# Check for -all arg
	if '-all' in argv:
		if len(argv) > 1:
			raise Exception('No other argument can be passed alongside -all.')

		for fcn in valid_args[: -1]:
			mp[fcn]()
		sys.exit()

	# Run functions in specified order
	for fcn in valid_args:
		if fcn in argv:
			mp[fcn]()
