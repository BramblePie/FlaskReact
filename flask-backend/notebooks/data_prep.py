import geopandas as gpd
import pandas as pd

zipfile = "zip://raw-data/wijkenbuurten2019.zip"
print(f"Loading {zipfile}...")
data = gpd.read_file(zipfile)
print(f"Loaded {zipfile}")

print(data.info())
