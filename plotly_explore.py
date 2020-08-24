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
df_electricity_by_county = pd.read_csv("~/Desktop/zach/Programming/data/ElectricityByCounty.csv")
df_electricity_by_county = df_electricity_by_county.drop(columns="Sector")
df_electricity_by_county = pd.concat([df_fips,df_electricity_by_county], axis=1)
print(df_electricity_by_county)

fig = px.choropleth(
    df_electricity_by_county,
    geojson=counties,
    locations='fips',
    color='2018',
    hover_name="County"    
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(
        bgcolor='#00bfff', 
        font_size=16, 
        font_family="Rockwell",
    )
)
fig.update_geos(fitbounds="locations")
fig.show()

# Per person
df_population_by_county = pd.read_csv("~/Desktop/zach/Programming/data/ca_population_2016-2018.csv")
df_population_by_county = pd.concat([df_fips,df_population_by_county], axis=1)
df_population_by_county['electricity_per_person_2018'] = df_electricity_by_county['2018'] / df_population_by_county['Pop_2018']
print(df_population_by_county)

fig_per_person = px.choropleth(
    df_population_by_county,
    geojson=counties,
    locations='fips',
    color='electricity_per_person_2018',
    hover_name="County"    
)
fig_per_person.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(
        bgcolor='#00bfff', 
        font_size=16, 
        font_family="Rockwell",
    )
)
fig_per_person.update_geos(fitbounds="locations")
fig_per_person.show()