# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Data understanding
# 
# De gebruikte dataset is “Geregistreerde criminaliteit" (https://opendata.cbs.nl/statline/#/CBS/nl/dataset/83648NED/table?fromstatweb). 
# 
# De CBS data is een csv bestand, dit staat voor comma seperated values of door comma gescheide waarden in het nederlands.
# De data bevat de volgende kolomen:
#  - `ID` is de unieke waarde voor elke row.
#  - `Soort misdrijf` geeft aan welke om wat voor misdrijf het gaat.
#  - `Perioden` geeft de periode aan waarin de misdrijven en aantal misdrijven zijn uitgevoerd.
#  - `Regio's` is de regio waarin de genoemde aantal misdrijven in zijn gebeurd.
#  - `Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)` is de aantal misdrijven die binnen een provincie/gemeente geregistreerd zijn.
#  - `Geregistreerde misdrijven/Geregistreerde misdrijven, relatief (% van totaal geregistreerde misdrijven)` is de procentuele aantal van de totaal geregistreerde misdrijven.
#  - `Geregistreerde misdrijven/Geregistreerde misdrijven per 1000 inw. (per 1.000 inwoners)` is de aantal misdrijven die binnen een provincie/gemeente geregistreerd zijn per 1.000 inwoners.
# %% [markdown]
# ## Beschrijven van de data
# 
# Hieronder staat een beschrijving van de data vanuit de Centraal Bureau Statistieken. Dit wordt telkens door middel van een stukje code weergegeven. 

# %%
import pandas as pd
import geopandas as gpd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from prep import movecol

# Dataset inlezen
file = "../../../raw-data/Veiligheid2.csv"
data_veiligheid = pd.read_csv(file, sep=";")

df = pd.DataFrame(data_veiligheid)

# Dataverkennen door dataframe te openen
data_veiligheid


# %%
# Info over de kolommen
info_kolommen_veiligheid = data_veiligheid.info()
info_kolommen_veiligheid


# %%
# Beschrijvende statistieken van de data
beschrijvende_stats_veiligheid = data_veiligheid.describe()
beschrijvende_stats_veiligheid


# %%
# Informatie over de kolomnamen in de Dataframe
data_veiligheid.columns


# %%
# Controleren op nulwaarden in de dataframe
data_veiligheid.isna().sum()

# %% [markdown]
# ## Data exploratie

# %%
# Pairplot weergave van de data.
#sb.pairplot(data_veiligheid, kind="reg")


# %%
# Catplot weergave van de data.
# sb.barplot(x="Perioden", y="Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)", data=data_veiligheid, color="steelblue", errwidth=0)


# %%
# Alle soorten misdrijven die er minimaal 1 keer in voorkomen.
soorten_misdrijven = data_veiligheid["Soort misdrijf"].drop_duplicates()
soorten_misdrijven

# %% [markdown]
# ## Data Preperation

# %%
# Kolomnamen van de dataset wijzigen.

data_veiligheid_nieuw = data_veiligheid

data_veiligheid_nieuw.rename(columns={'Soort misdrijf':'Soort_misdrijf','Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)':'Aantal_misdrijven', 'Geregistreerde misdrijven/Geregistreerde misdrijven, relatief (% van totaal geregistreerde misdrijven)':'Misdrijven_relatief(%)', 'Geregistreerde misdrijven/Geregistreerde misdrijven per 1000 inw.  (per 1 000 inwoners)':'Aantal_misdrijven(per_1000_inw)'}, inplace=True)

data_veiligheid_nieuw = data_veiligheid_nieuw.drop(columns=["Aantal_misdrijven(per_1000_inw)"])

data_veiligheid_nieuw


# %%
# Controleren op nulwaarden in de dataframe
data_veiligheid_nieuw.isna().sum()


# %%
data_veiligheid_nieuw.loc[data_veiligheid_nieuw['Aantal_misdrijven'] == 0]


# %%
#nieuwe dataset inladen voor mergen dataset, zodat regio's ook provincie er achter heeft staan.

file = "../../../raw-data/gemeenten-provincie.xlsx"
postcode = pd.read_excel(file) 

#dataframe maken van de dataset
df2 = pd.DataFrame(postcode)

#colom hernoemen
postcode.rename(columns={"Gemeente":"Regio's"}, inplace=True)

#dataframe opnieuw defineren
df2 = pd.DataFrame(postcode)

#mergen van 2 dataset op basis van regio's colomn
data_veiligheid_incl_provincie = data_veiligheid_nieuw.merge(df2, on="Regio's")

data_veiligheid_incl_provincie


# %%
data_veiligheid_incl_provincie = movecol(data_veiligheid_incl_provincie, cols_to_move=['Provincie'], ref_col="Regio's", place='After')

data_veiligheid_incl_provincie.loc[((data_veiligheid_incl_provincie["Regio's"] == "Zwolle"))]


# %%
# Alle Gemeentelijke records groeperen in de bijbehorende Provincie

provincies = sorted(data_veiligheid_incl_provincie["Provincie"].drop_duplicates())

provincies


# %%
np.set_printoptions(threshold=np.inf)

min_max_scaler = preprocessing.MinMaxScaler()

aantal_misdrijven_minmax = min_max_scaler.fit_transform(data_veiligheid_incl_provincie[["Aantal_misdrijven"]])
data_veiligheid_incl_provincie["Aantal_misdrijven_genormaliseerd"] = aantal_misdrijven_minmax

data_veiligheid_incl_provincie


# %%
data_veiligheid_incl_provincie.describe()


# %%
m1 = data_veiligheid_incl_provincie['Aantal_misdrijven_genormaliseerd'] < 0.000105
m2 = data_veiligheid_incl_provincie['Aantal_misdrijven_genormaliseerd'] > 0.003222

data_veiligheid_incl_provincie['Aantal_misdrijven_geklasseerd'] = np.select([m1,m2], ['Laag','Hoog'], default='Middel')

data_veiligheid_incl_provincie


# %%
misdrijven_df = data_veiligheid_incl_provincie
misdrijven_df


# %%
#PER PERIODE/JAAR EEN OVERZICHT VAN ALLE SOORTEN MISDRIJVEN EN WAT HET RELATIEF IS VAN HET TOTAAL. REGIO IS GEKOZEN DOOR INPUT
pd.set_option('display.max_rows', 50)

gemeente = input('Voer hier een gemeente in')

soortmisdrijf_regio_perjaar = misdrijven_df.loc[((misdrijven_df["Regio's"] == gemeente) | (misdrijven_df["Perioden"] == gemeente))]

soortmisdrijf_regio_perjaar


# %%
sb.pairplot(soortmisdrijf_regio_perjaar.groupby(["Perioden", "Soort_misdrijf"]).sum(), kind="reg")


# %%
sb.pairplot(data_veiligheid_incl_provincie, kind="reg")


# %%
misdrijven_df


# %%
misdrijven_df["Soort_misdrijf"].unique()

