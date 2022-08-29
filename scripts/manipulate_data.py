import argparse
import sys
from functools import partial

import pandas as pandas

# Save df as csv with name "name"
def save(df, name):
	df.to_csv('../data/{}'.format(name), index=False)
	print('Saved...')

# Sort rows of df by athlete name and city in place, then drop unnecessary columns
def sort_name_city(df):
	df.sort_values(by=['Name', 'City'], inplace=True)
	print('Sorted...')

# Drop unnecessary columns
def drop_unnecessary_cols(df):
	df.drop(columns=['Bib', 'Country', 'Projected Time', 'Gender', 'Division'], inplace=True)
	print('Unnecessary columns dropped...')

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

	print('Removed {} non-unique rows...'.format(number_of_removals))

# Drop any rows that contain "-" null keyword
def drop_null(df):
	null_rows = df.isin(['-',]).any(axis=1)
	null_rows = null_rows[null_rows == True]

	df.drop(null_rows.index, inplace=True)
	print('{} null rows dropped...'.format(null_rows.shape[0]))

if __name__ == '__main__':
	argv = sys.argv[1:]

	parser = argparse.ArgumentParser(
		prog='manipulate_data', 
		usage='python %(prog)s [name] [options]',
		description='Tools to manipulate data files',
	)

	parser.add_argument('name')
	parser.add_argument('-duc', '--dropcol', action='store_true')
	parser.add_argument('-dn', '--dropnull', action='store_true')
	parser.add_argument('-o', '--sort', action='store_true')
	parser.add_argument('-u', '--unique', action='store_true')
	parser.add_argument('-s', '--save', action='store_true')
	parser.add_argument('-a', '--all', action='store_true')

	args = parser.parse_args(argv)
	
	try:
		df = pandas.read_csv(args.name)
	except:
		raise Exception('No csv file with name {} was found.'.format(args.name))

	order_of_execution = [
		partial(drop_unnecessary_cols, df),
		partial(drop_null, df),
		partial(sort_name_city, df),
		partial(drop_nonunique_name_city, df),
		partial(save, df, '{}-cleaned.csv'.format(args.name.split('.csv')[0]))
	]

	if args.all:
		for fnc in order_of_execution:
			fnc()
		sys.exit()

	if args.dropcol:
		order_of_execution[0]()
	if args.dropnull:
		order_of_execution[1]()
	if args.sort:
		order_of_execution[2]()
	if args.unique:
		order_of_execution[3]()
	if args.save:
		order_of_execution[4]()

