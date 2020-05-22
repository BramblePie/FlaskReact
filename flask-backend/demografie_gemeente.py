# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from Helper_functions import *
import numpy as np 
from sklearn import preprocessing
gpdf_gemeenten = wfs_data("https://geodata.nationaalgeoregister.nl/wijkenbuurten2019/wfs", "wijkenbuurten2019:gemeenten2019")


# %%
gpdf_gemeenten = gpdf_gemeenten.drop(columns=['id','jrstatcode','percentage_westerse_migratieachtergrond','percentage_niet_westerse_migratieachtergrond',
       'percentage_uit_marokko',
       'percentage_uit_nederlandse_antillen_en_aruba',
       'percentage_uit_suriname', 'percentage_uit_turkije',
       'percentage_overige_nietwestersemigratieachtergrond'])

# %%
gpdf_gemeenten.columns
# %%
gpdf_gemeenten = gpdf_gemeenten.replace(-99999999, np.nan)


# %%
def DemografieAPI_gemeenten(gemeente):
    df = gpdf_gemeenten.loc[gpdf_gemeenten['gemeentenaam'] == gemeente]
    return df


# %%


