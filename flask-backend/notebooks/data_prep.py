import geopandas as gpd
import pandas as pd

try:
    zipfile = "zip://raw-data/wijkenbuurten2019.zip"
    print(f"Loading {zipfile}...")
    gdf = gpd.read_file(zipfile)
    print(f"Loaded {zipfile}")

    print(gdf.head(1))
    print(gdf.info())

    inwgem = pd.DataFrame(gdf.drop(columns="geometry"))
    nums = inwgem._get_numeric_data()
    nums[nums < 0] = 0
    inwgem = inwgem.groupby(["GM_NAAM"]).sum()

    def get_gem_min_inw(aantal):
        return inwgem[inwgem["AANT_INW"] > aantal].to_dict(orient="index")
except:

    def get_gem_min_inw(aantal):
        return None
