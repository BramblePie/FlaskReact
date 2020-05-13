import pandas as pd
import geopandas as gpd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from prep import movecol

# Dataset inlezen
file = "raw-data/Veiligheid2.csv"
data_veiligheid = pd.read_csv(file, sep=";")

# ## Data exploratie
# Alle soorten misdrijven die er minimaal 1 keer in voorkomen.
soorten_misdrijven = data_veiligheid["Soort misdrijf"].drop_duplicates()

# ## Data Preperation
# Kolomnamen van de dataset wijzigen.

data_veiligheid_nieuw = data_veiligheid
data_veiligheid_nieuw.rename(columns={'Soort misdrijf':'Soort_misdrijf','Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)':'Aantal_misdrijven', 'Geregistreerde misdrijven/Geregistreerde misdrijven, relatief (% van totaal geregistreerde misdrijven)':'Misdrijven_relatief(%)', 'Geregistreerde misdrijven/Geregistreerde misdrijven per 1000 inw.  (per 1 000 inwoners)':'Aantal_misdrijven(per_1000_inw)'}, inplace=True)

#nieuwe dataset inladen voor mergen dataset, zodat regio's ook provincie er achter heeft staan.
file = "raw-data/gemeenten-provincie.xlsx"
postcode = pd.read_excel(file) 

#dataframe maken van de dataset
df2 = pd.DataFrame(postcode)

#colom hernoemen
postcode.rename(columns={"Gemeente":"Regio's"}, inplace=True)

#dataframe opnieuw defineren
df2 = pd.DataFrame(postcode)

#mergen van 2 dataset op basis van regio's kolom
data_veiligheid_incl_provincie = data_veiligheid_nieuw.merge(df2, on="Regio's")

data_veiligheid_incl_provincie = movecol(data_veiligheid_incl_provincie, cols_to_move=['Provincie'], ref_col="Regio's", place='After')

# Alle Gemeentelijke records groeperen in de bijbehorende Provincie
provincies = sorted(data_veiligheid_incl_provincie["Provincie"].drop_duplicates())

# TOTAAL AANTAL MISDRIJVEN PER JAAR PER PROVINCIE. RELATIEVE KOLOM IS NIET VAN TOEPASSING AANGEZIEN TOTALEN GEBASEERD IS OP 100%.
data_voorspelling_totaal = data_veiligheid_incl_provincie.loc[((data_veiligheid_incl_provincie.Soort_misdrijf == 'Misdrijven, totaal'))]
totaal_provincie_perjaar = data_voorspelling_totaal.groupby(['Provincie', 'Perioden']).sum()
totaal_misdrijven_pv_jaar = totaal_provincie_perjaar.drop(columns=['Misdrijven_relatief(%)'])

data_voorspelling_groupby = data_voorspelling_totaal.groupby(['Perioden', "Regio's"]).sum()

min_max_scaler = preprocessing.MinMaxScaler()

aantal_misdrijven_minmax = min_max_scaler.fit_transform(data_voorspelling_totaal[["Aantal_misdrijven"]])
data_voorspelling_groupby["Aantal_misdrijven_genormaliseerd"] = aantal_misdrijven_minmax

m1 = data_voorspelling_groupby['Aantal_misdrijven_genormaliseerd'] < 0.005357
m2 = data_voorspelling_groupby['Aantal_misdrijven_genormaliseerd'] > 0.017679

data_voorspelling_groupby['Aantal_misdrijven_geklasseerd'] = np.select([m1,m2], ['Laag','Hoog'], default='Middel')

#nieuwe index maken voor Flask
misdrijven_df = data_voorspelling_groupby.reset_index()
misdrijven_df

soort_misdrijf = data_veiligheid_incl_provincie.drop(columns=['Perioden', 'Provincie',
       'Aantal_misdrijven', 'Misdrijven_relatief(%)',
       'Aantal_misdrijven(per_1000_inw)'])

misdrijven_df = misdrijven_df.merge(soort_misdrijf, on="Regio's")
misdrijven_df = movecol(misdrijven_df, cols_to_move=['Soort_misdrijf'], ref_col="Regio's", place='After')

#PER PERIODE/JAAR EEN OVERZICHT VAN ALLE SOORTEN MISDRIJVEN EN WAT HET RELATIEF IS VAN HET TOTAAL. REGIO IS GEKOZEN DOOR INPUT
# pd.set_option('display.max_rows', 50)

misdrijven_df = misdrijven_df.drop(columns=["Misdrijven_relatief(%)"])

# gemeente = input('Voer hier een gemeente in')

# soortmisdrijf_regio_perjaar = misdrijven_df.loc[((misdrijven_df["Regio's"] == gemeente) | (misdrijven_df["Perioden"] == gemeente))]

# soortmisdrijf_regio_perjaar

print("Functions ready")


def veiligheidAPI(plaats):
    # voor elke client/ bezoeker
    resultaat = misdrijven_df.loc[(misdrijven_df["Regio's"] == plaats)]
    return resultaat.to_dict(orient="records")
