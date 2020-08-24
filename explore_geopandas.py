import pandas as pd
import matplotlib.pyplot as plt
import geopandas

df = pd.read_csv("~/Desktop/zach/Programming/data/ElectricityByCounty.csv")
df = df.drop(columns="Sector")
df

plt.plot(df['County'], df['Total Usage'])

df_geo = geopandas.GeoDataFrame.from_file("~/Desktop/zach/Programming/data/California_County_Boundaries-shp/cnty19_1.shp")