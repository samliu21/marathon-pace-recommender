from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

YEAR = 2015

url = 'http://registration.baa.org/{}/cf/Public/iframe_ResultsSearch.cfm'.format(YEAR)
headers = {
	'Accept': 'text/html',
	'Content-Type': 'application/x-www-form-urlencoded',
}
params = {
	'mode': 'results',
	'criteria': '',
	'StoredProcParamsOn': 'yes',
	'VarGenderID': 0,
	'VarBibNumber': '',
	'VarLastName': '',
	'VarFirstName': '',
	'VarStateID': 0,
	'VarCountryOfResID': 193, # America
	'VarCountryOfCtzID': 0,
	'VarReportingSegID': 1,
	'VarAwardsDivID': 0,
	'VarQualClassID': 0,
	'VarCity': '',
	'VarTargetCount': 50000,
	'records': 25,
}
def data(start):
	return {
		'start': start,
		'next': 'Next 25 Records',
	}

def get_25_athletes(start=1, session=None):
	"""
	Returns Pandas.DataFrame of athletes form index start -> start + 24
	"""

	if session:
		response = session.post(url=url, data=data(start=start))
	else:
		print('No session found...')

		response = requests.post(
			url=url,
			headers=headers,
			params=params,
			data=data(start=start),
		)

	if not response.ok:
		raise Exception('Request failed...')

	soup = BeautifulSoup(response.text, 'html.parser')

	"""
	<tr class="tf_header">
		<td>289</td>
		<td>Liu, Sam</td>
		...
	</tr>

	<table class="info_grid">
		<tr>
			<td>0:15:54</td>
			<td>0:31:47</td>
			...
		</tr>
		...
	</table>
	"""

	athlete_info = []
	athlete_times = []

	athletes_info_table = [athlete.find_all('td') for athlete in soup.find_all('tr', {'class': 'tr_header' })]
	for athlete in athletes_info_table:
		a = []
		for val in athlete[: -2]:
			try:
				a.append(val.string.strip())
			except:
				a.append(val.find('a').string.strip())
		athlete_info.append(a)

	athletes_times_table = [athlete.find_all('tr')[1::2] for athlete in soup.find_all('table', {'class': 'table_infogrid'})]
	for athlete in athletes_times_table:
		athlete_times.append([val.string.strip() for val in [*athlete[0].find_all('td'), *athlete[1].find_all('td')]])
	
	athletes = []
	for i in range(len(athlete_info)):
		athletes.append(athlete_info[i] + athlete_times[i])

	return pd.DataFrame(athletes, columns=[
		'Bib',
		'Name',
		'Age',
		'Sex',
		'City',
		'State',
		'Country',
		'5k',
		'10k',
		'15k',
		'20k',
		'Half',
		'25k',
		'30k',
		'35k',
		'40k',
		'Pace',
		'Projected Time',
		'Official Time',
		'Overall',
		'Gender', # Placement in gender group
		'Division', # Position in division
	])

with requests.Session() as s:
	s.headers = headers
	s.params = params

	for i in range(870):
		time.sleep(0.2) # Don't wreck the server 

		df = get_25_athletes(start=i * 25 + 1, session=s)
		df.to_csv('{}.csv'.format(YEAR), mode='a', index=False, header=(i == 0))

		if i % 25 == 0:
			print('Processed {} athletes'.format(i * 25))
