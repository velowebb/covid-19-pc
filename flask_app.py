
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import pandas as pd

app = Flask(__name__)

popData = {}

import csv
with open('/home/zonyl/covid/population.csv', "r") as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		popData[row['Country Name']] = row['2018']


def perCapita(series):

	series['cpc'] = "{}*".format(series['Confirmed'])
	series['dpc'] = "{}*".format(series['Deaths'])
	series['rpc'] = "{}*".format(series['Recovered'])
	series['apc'] = "{}*".format(series['Active'])

	if series['Country_Region'] in popData and popData[series['Country_Region']]:
		pop = round(float(popData[series['Country_Region']]) / 1000)
		series['pop'] = pop
		series['cpc'] = round(series['Confirmed'] / pop, 6)
		series['dpc'] = round(series['Deaths'] / pop, 6)
		series['rpc'] = round(series['Recovered'] / pop, 6)
		series['apc'] = round(series['Active'] / pop, 6)
	return series

def stupidCountries():
    return {
        "US": "United States",
        "Russia": "Russian Federation",
        "Korea, South": "Korea, Rep.",
        "Iran":"Iran, Islamic Rep.",
        "Egypt":"Egypt, Arab Rep.",
        "Congo (Kinshasa)":"Congo, Dem. Rep.",
        "Congo (Brazzaville)": "Congo, Rep.",
        "Czechia" : "Czech Republic",
        "Gambia" : "Gambia, The"
    }

@app.route('/')
def hello_world():
	from datetime import date, timedelta
	yesterday = (date.today() - timedelta(days = 1)).strftime('%m-%d-%Y')
	url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(yesterday)
	df = pd.read_csv(url).drop(columns=["FIPS","Admin2","Province_State","Last_Update","Lat","Long_","Combined_Key"])
	df = df.groupby("Country_Region", as_index=False).sum()
	df = df.replace(stupidCountries())
	df = df.apply(perCapita, axis=1)
	df = df.drop(columns=["Confirmed", "Deaths", "Recovered", "Active"])
	df = df[["Country_Region", "pop", "cpc", "dpc", "rpc", "apc"]]
	table = df.to_json(orient='split')
	return table
	#return url

