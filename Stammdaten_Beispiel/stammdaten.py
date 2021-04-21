import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Einlesen der Regionen Europas auf NUTS3 level
europe_map = gpd.read_file(r"NUTS_BN_01M_2021_3035\NUTS_BN_01M_2021_3035.shp")

#Shapefile anzeigen lassen
#europe_map.plot(Color='red') #plotten (berechnen) und attribute festlegen
#plt.show() #anzeigen als Bild
# Einlesen der Stammdaten als Pandas DF aus einer csv
wind = pd.read_csv("raw_wts_red.csv")

# Umwandlung des DF in ein GeoDataFrame (Einführung der geometry column)
wind_sd = gpd.GeoDataFrame(
    wind,
    geometry=gpd.points_from_xy(wind.ENH_Laengengrad, wind.ENH_Breitengrad),
)

# Definieren, welches EPSG Format die eingelesenen Daten haben
wind_sd.crs = {"init": "epsg:4326"}

# Umwandlung des EPSG Formats, damit einheitlich mit europe_map
wind_sd = wind_sd.to_crs({"init": "epsg:3035"})

# Aufteilen der Anlagen in On- und -Offshore
print(f"Anzahl WEA insgesamt: {len(wind_sd)}")
wind_on = wind_sd[wind_sd.loc[:, "ENH_Lage"] == "Windkraft an Land"]
print(f"Anzahl WEA an Land: {len(wind_on)}")
wind_off = wind_sd[wind_sd.loc[:, "ENH_Lage"] == "Windkraft auf See"]
print(f"Anzahl WEA auf See: {len(wind_off)}")


# Plotten der Anlagen, Punktgröße spiegelt Nettoleistung wider
fig, ax = plt.subplots(figsize=(10, 15))
europe_map.plot(facecolor="white", edgecolor="black", ax=ax)
wind_on.plot(facecolor="green", markersize=wind_on.ENH_Nettonennleistung / 100, ax=ax)
wind_off.plot(facecolor="blue", markersize=wind_off.ENH_Nettonennleistung / 100, ax=ax)
plt.show()

# Export des wind Geodataframes als Shapefile
wind_sd.to_file("export\Wind_Stammdaten_3035.shp")
