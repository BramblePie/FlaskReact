# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from Helper_functions import *
import numpy as np 
from sklearn import preprocessing
gpdf_wijken = wfs_data("https://geodata.nationaalgeoregister.nl/wijkenbuurten2019/wfs", "wijkenbuurten2019:cbs_wijken_2019")
#gpdf_gemeenten = wfs_data("https://geodata.nationaalgeoregister.nl/wijkenbuurten2019/wfs", "wijkenbuurten2019:gemeenten2019")


# %%
gpdf_wijken = gpdf_wijken.replace(-99999999, np.nan)
#gpdf_gemeenten = gpdf_gemeenten.replace(-99999999, np.nan)



# %% [markdown]
# # Construct data
# 
# Hieronder wordt er aan de hand van boolean values een selectie gemaakt in de data. Deze boolean values zijn representatief met user input van de front end. Voor nu wordt er nog geen rekening gehouden met classificatie. Er wordt echter wel een selecte gemaakt met daarin dat bijvoorbeeld kolom 'omgevingsadressendichtheid' en 'stedelijkheid_adressen_per_km2' betrekking hebben tot stedelijkheid. Met deze data wordt er één extra kolom gemaakt met daarbin de normalisatie waarde. 
# Deze normalisatie waarde wordt later dan weer gebruikt om een weging te kunnen maken voor de user input. 
# Hieronder een overzicht met welke kolommen worden meegenomen bij de user input en dus de normalisatie:
# 
# - `Stedelijkheid` worden de kolommen omgevingsadressendichtheid, stedelijkheid_adressen_per_km2 meegenomen
# - `water` wordt de kolom oppervlakte_water_in_ha meegenomen
# - `mensen` worden de kolommen aantal_inwoners, bevolkingsdichtheid_inwoners_per_km2 meegenomen 
# - `kinderen` worden de kolommen aantal_inwoners, percentage_personen_0_tot_15_jaar meegenomen
# - `senioren` worden de kolommen aantal_inwoners, percentage_personen_65_jaar_en_ouder meegenomen 
# %%
gpdf_wijken_backup = gpdf_wijken

# stedelijkheid = True
# water = True
# mensen = True 
# kinderen = True 
# senioren = True

# if stedelijkheid == True:
#     # Normalisatie waarde aanmaken voor 'omgevingsadressendichtheid'
#     x = gpdf_wijken[['omgevingsadressendichtheid']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['omgevingsadressendichtheid_genormaliseerd'] = pd.DataFrame(x_scaled)

#     # Normalisatie waarde aanmaken voor stedelijkheid_adressen_per_km2
#     x = gpdf_wijken[['stedelijkheid_adressen_per_km2']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['stedelijkheid_adressen_per_km2_genormaliseerd'] = pd.DataFrame(x_scaled)

#     # Maken van vertaling naar één normalisatie waarde in een kolom 'stedelijkheid_normalisatie_waarde'
#     gpdf_wijken['stedelijkheid_normalisatie_waarde'] = gpdf_wijken['omgevingsadressendichtheid_genormaliseerd'] + gpdf_wijken['stedelijkheid_adressen_per_km2_genormaliseerd']

#     # Verwijderen van overbodige kolommen
#     gpdf_wijken.drop(columns=['omgevingsadressendichtheid_genormaliseerd','stedelijkheid_adressen_per_km2_genormaliseerd'], axis=1, inplace=True)

#     #KLASSE KOLOM MAKEN OP BASIS VAN KWARTIELEN VAN NORMALISATIE WAARDE
#     dataframe_kolom = gpdf_wijken["stedelijkheid_normalisatie_waarde"]
#     q25 = dataframe_kolom.quantile(q=.25)
#     q50 = dataframe_kolom.quantile(q=.5)
#     q75 = dataframe_kolom.quantile(q=.75)

#     # Gebruik de aantallen die bij vg_data.describe() staan
#     m1 = dataframe_kolom < q25
#     m2 = np.logical_and(dataframe_kolom >  q25, dataframe_kolom < q50)
#     m3 = np.logical_and(dataframe_kolom >  q50, dataframe_kolom < q75)
#     m4 = dataframe_kolom > q75

#     gpdf_wijken['klasse_stedelijkheid_normalisatie'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')

# # -----------------------------------------------------------------------------------------------------

# if mensen == True:
#     # Normalisatie waarde aanmaken voor 'omgevingsadressendichtheid'
#     x = gpdf_wijken[['aantal_inwoners']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['aantal_inwoners_genormaliseerd'] = pd.DataFrame(x_scaled)
    
#     # Normalisatie waarde aanmaken voor stedelijkheid_adressen_per_km2
#     x = gpdf_wijken[['bevolkingsdichtheid_inwoners_per_km2']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['bevolkingsdichtheid_inwoners_per_km2_genormaliseerd'] = pd.DataFrame(x_scaled)

#     # Maken van vertaling naar één normalisatie waarde in een kolom 'stedelijkheid_normalisatie_waarde'
#     gpdf_wijken['mensen_normalisatie_waarde'] = gpdf_wijken['aantal_inwoners_genormaliseerd'] + gpdf_wijken['bevolkingsdichtheid_inwoners_per_km2_genormaliseerd']

#     # Verwijderen van overbodige kolommen
#     gpdf_wijken.drop(columns=['aantal_inwoners_genormaliseerd','bevolkingsdichtheid_inwoners_per_km2_genormaliseerd'], axis=1, inplace=True)

#     #KLASSE KOLOM MAKEN OP BASIS VAN KWARTIELEN VAN NORMALISATIE WAARDE
#     dataframe_kolom = gpdf_wijken["mensen_normalisatie_waarde"]
#     q25 = dataframe_kolom.quantile(q=.25)
#     q50 = dataframe_kolom.quantile(q=.5)
#     q75 = dataframe_kolom.quantile(q=.75)

#     # Gebruik de aantallen die bij vg_data.describe() staan
#     m1 = dataframe_kolom < q25
#     m2 = np.logical_and(dataframe_kolom > q25, dataframe_kolom < q50)
#     m3 = np.logical_and(dataframe_kolom > q50, dataframe_kolom < q75)
#     m4 = dataframe_kolom > q75

#     gpdf_wijken['klasse_mensen_normalisatie'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')

# # -----------------------------------------------------------------------------------------------------

# if kinderen == True:
#     # Normalisatie waarde aanmaken voor 'omgevingsadressendichtheid'
#     gpdf_wijken['kinderen_berekening'] = gpdf_wijken['percentage_personen_0_tot_15_jaar'] / 100
#     gpdf_wijken['aantal_kinderen_in_wijk'] = gpdf_wijken['aantal_inwoners'] * gpdf_wijken['kinderen_berekening']
#     gpdf_wijken['aantal_kinderen_in_wijk'] = gpdf_wijken['aantal_kinderen_in_wijk'].apply(np.floor)

#     x = gpdf_wijken[['aantal_kinderen_in_wijk']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['kinderen_normalisatie_waarde'] = pd.DataFrame(x_scaled)

#     gpdf_wijken.drop(columns=['kinderen_berekening', 'aantal_kinderen_in_wijk'], axis=1, inplace=True)

#     #KLASSE KOLOM MAKEN OP BASIS VAN KWARTIELEN VAN NORMALISATIE WAARDE
#     dataframe_kolom = gpdf_wijken["kinderen_normalisatie_waarde"]
#     q25 = dataframe_kolom.quantile(q=.25)
#     q50 = dataframe_kolom.quantile(q=.5)
#     q75 = dataframe_kolom.quantile(q=.75)

#     # Gebruik de aantallen die bij vg_data.describe() staan
#     m1 = dataframe_kolom < q25
#     m2 = np.logical_and(dataframe_kolom >  q25, dataframe_kolom < q50)
#     m3 = np.logical_and(dataframe_kolom >  q50, dataframe_kolom < q75)
#     m4 = dataframe_kolom > q75

#     gpdf_wijken['klasse_kinderen_normalisatie'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')

# # -----------------------------------------------------------------------------------------------------

# if senioren == True:
#     # Normalisatie waarde aanmaken voor 'omgevingsadressendichtheid'
#     gpdf_wijken['senioren_berekening'] = gpdf_wijken['percentage_personen_65_jaar_en_ouder'] / 100
#     gpdf_wijken['aantal_senioren_in_wijk'] = gpdf_wijken['aantal_inwoners'] * gpdf_wijken['senioren_berekening']
#     gpdf_wijken['aantal_senioren_in_wijk'] = gpdf_wijken['aantal_senioren_in_wijk'].apply(np.floor)

#     x = gpdf_wijken[['aantal_senioren_in_wijk']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['senioren_normalisatie_waarde'] = pd.DataFrame(x_scaled)

#     gpdf_wijken.drop(columns=['senioren_berekening', 'aantal_senioren_in_wijk'], axis=1, inplace=True)

#     #KLASSE KOLOM MAKEN OP BASIS VAN KWARTIELEN VAN NORMALISATIE WAARDE
#     dataframe_kolom = gpdf_wijken["senioren_normalisatie_waarde"]
#     q25 = dataframe_kolom.quantile(q=.25)
#     q50 = dataframe_kolom.quantile(q=.5)
#     q75 = dataframe_kolom.quantile(q=.75)

#     # Gebruik de aantallen die bij vg_data.describe() staan
#     m1 = dataframe_kolom < q25
#     m2 = np.logical_and(dataframe_kolom >  q25, dataframe_kolom < q50)
#     m3 = np.logical_and(dataframe_kolom >  q50, dataframe_kolom < q75)
#     m4 = dataframe_kolom > q75

#     gpdf_wijken['klasse_senioren_normalisatie'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')

# # -----------------------------------------------------------------------------------------------------

# if water == True:
#     # Normalisatie waarde aanmaken voor 'omgevingsadressendichtheid'
#     x = gpdf_wijken[['oppervlakte_water_in_ha']]
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     gpdf_wijken['water_normalisatie_waarde'] = pd.DataFrame(x_scaled)

#     #KLASSE KOLOM MAKEN OP BASIS VAN KWARTIELEN VAN NORMALISATIE WAARDE
#     dataframe_kolom = gpdf_wijken["water_normalisatie_waarde"]
#     q25 = dataframe_kolom.quantile(q=.25)
#     q50 = dataframe_kolom.quantile(q=.5)
#     q75 = dataframe_kolom.quantile(q=.75)

#     # Gebruik de aantallen die bij vg_data.describe() staan
#     m1 = dataframe_kolom < q25
#     m2 = np.logical_and(dataframe_kolom >  q25, dataframe_kolom < q50)
#     m3 = np.logical_and(dataframe_kolom >  q50, dataframe_kolom < q75)
#     m4 = dataframe_kolom > q75

#     gpdf_wijken['klasse_water_normalisatie'] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')

# gpdf_wijken

Dataframe_demografie = gpdf_wijken

Dataframe_demografie = gpdf_wijken[['wijkcode', 'wijknaam','gemeentenaam','water','omgevingsadressendichtheid','stedelijkheid_adressen_per_km2', 'bevolkingsdichtheid_inwoners_per_km2', 'aantal_inwoners', 'mannen',
       'vrouwen', 'percentage_personen_0_tot_15_jaar',
       'percentage_personen_15_tot_25_jaar',
       'percentage_personen_25_tot_45_jaar',
       'percentage_personen_65_jaar_en_ouder',
       'percentage_personen_45_tot_65_jaar', 'percentage_ongehuwd',
       'percentage_gehuwd', 'percentage_gescheid','aantal_huishoudens', 'percentage_eenpersoonshuishoudens',
       'percentage_huishoudens_zonder_kinderen',
       'percentage_huishoudens_met_kinderen', 'gemiddelde_huishoudsgrootte','oppervlakte_totaal_in_ha', 'oppervlakte_land_in_ha',
       'oppervlakte_water_in_ha']]

def demografieAPI(wijk_code):
    df = Dataframe_demografie.loc[Dataframe_demografie['wijkcode'] == wijk_code]
    return df.to_dict(orient='list')

