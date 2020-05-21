
import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn import preprocessing
<<<<<<< Updated upstream
pd.options.display.max_columns = None
pd.options.display.max_rows = None
=======
>>>>>>> Stashed changes
data = pd.read_csv('data/link/dataset.csv')
data = data[['gemeente','postcode','gemiddelde_woz_waarde_woning','geometry']]
gemiddeldewoz = data[['gemeente','gemiddelde_woz_waarde_woning']].groupby('gemeente').mean()
gemiddeldewoz['gemiddelde_woz_waarde_gemeente'] = gemiddeldewoz['gemiddelde_woz_waarde_woning']
gemiddeldewoz = gemiddeldewoz.drop(columns='gemiddelde_woz_waarde_woning')
data = data.merge(gemiddeldewoz, on='gemeente')
np.set_printoptions(threshold=np.inf)
min_max_scaler = preprocessing.MinMaxScaler()
data_minmax = min_max_scaler.fit_transform(data[["gemiddelde_woz_waarde_gemeente"]])
data["woz_normalisatie"] = data_minmax
p25 = data['woz_normalisatie'].quantile(q=0.25)
p50 = data['woz_normalisatie'].quantile(q=0.50)
p75 = data['woz_normalisatie'].quantile(q=0.75)
p100 = data['woz_normalisatie'].quantile(q=1)
m1 = data["woz_normalisatie"] < p25
m2 = np.logical_and(data["woz_normalisatie"] > p25,data["woz_normalisatie"] < p50)
m3 = np.logical_and(data["woz_normalisatie"] > p50,data["woz_normalisatie"] < p75)
m4 = data["woz_normalisatie"] > p75
data['klasse_woz'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='none')
data.to_csv('data/link/datasetwoznormaliseerd.csv')
data = data[['gemeente','postcode','gemiddelde_woz_waarde_woning','gemiddelde_woz_waarde_gemeente','klasse_woz']]
data.to_csv('data/link/datasetwozfunctie.csv')
wozwaarde = data
def wozwaardeAPI(gemeente):
    wozdata = wozwaarde.loc[wozwaarde['gemeente'] == gemeente]
    return wozdata.to_dict(orient='records')


