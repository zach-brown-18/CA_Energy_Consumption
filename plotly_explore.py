from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
import plotly.express as px

# Get fips codes
df_fips = pd.read_csv("ca_fips.csv", dtype={"fips": str})
df_fips = df_fips.drop(columns="county")

# County
df_electricity_by_county = pd.read_csv("ElectricityByCounty.csv")
df_electricity_by_county = df_electricity_by_county.drop(columns="Sector")
df_electricity_by_county = pd.concat([df_fips,df_electricity_by_county], axis=1)
print(df_electricity_by_county)

title = "Electicity Consumption by County 2018"
fig = px.choropleth(
    df_electricity_by_county,
    geojson=counties,
    locations='fips',
    color='2018',
    hover_name="County",
    title=title
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(
        bgcolor='#00bfff', 
        font_size=16, 
        font_family="Rockwell",
    ),
    title={'y':.9}
)
fig.update_geos(fitbounds="locations")
fig.show()

# Per person
df_population_by_county = pd.read_csv("ca_population_2016-2018.csv")
df_population_by_county = pd.concat([df_fips,df_population_by_county], axis=1)
df_population_by_county['electricity_per_person_2018'] = df_electricity_by_county['2018'] / df_population_by_county['Pop_2018']
df_population_by_county['electricity_per_person_2017'] = df_electricity_by_county['2017'] / df_population_by_county['Pop_2017']
df_population_by_county['electricity_per_person_2016'] = df_electricity_by_county['2016'] / df_population_by_county['Pop_2016']
print(df_population_by_county)

title = "Electricity Consumption per Person by County 2018"
fig_per_person = px.choropleth(
    df_population_by_county,
    geojson=counties,
    locations='fips',
    color='electricity_per_person_2018',
    hover_name="County",
    title=title
)
fig_per_person.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(
        bgcolor='#00bfff', 
        font_size=16, 
        font_family="Rockwell",
    ),
    title={'y':.9}
)
fig_per_person.update_geos(fitbounds="locations")
fig_per_person.show()

df_electricity_by_county.sort_values(by="2018", ascending=False)
df_electricity_by_county_2018 = df_electricity_by_county[['fips','County','2018']]
top_10 = df_electricity_by_county_2018.sort_values(by="2018", ascending=False).iloc[:10,:]
remainder = df_electricity_by_county_2018.sort_values(by="2018", ascending=False).iloc[10:,:]
print(top_10)
print(remainder)

remainder_sum = remainder['2018'].sum()
remainder_sum

import numpy as np
data={'fips':[np.nan],'County':['Remainder'],'2018':[remainder_sum]}
df_remainder_sum = pd.DataFrame(data=data)
top_10_and_remainder = top_10.append(df_remainder_sum)

fig_pie = px.pie(top_10_and_remainder, values='2018', names='County', title='Electricity Consumption of CA Counties')
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.show()

title = "Electricity Consumption 2018 - Top 10 Counties"
labels={"2018": "Electricity Consumption"}
fig_bar = px.bar(top_10, x='County', y='2018', title=title, labels=labels)
fig_bar.show()

title = "Electricity consumption by county 2018"
labels={"2018": "Electricity Consumption"}
fig_bar_all = px.bar(df_electricity_by_county.sort_values(by="2018", ascending=False), x='County', y='2018', title=title, labels=labels)
fig_bar_all.show()

