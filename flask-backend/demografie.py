# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from Helper_functions import *

gpdf_wijken = wfs_data("https://geodata.nationaalgeoregister.nl/wijkenbuurten2019/wfs", "wijkenbuurten2019:cbs_wijken_2019")
#gpdf_gemeenten = wfs_data("https://geodata.nationaalgeoregister.nl/wijkenbuurten2019/wfs", "wijkenbuurten2019:gemeenten2019")


# %%
gpdf_wijken = gpdf_wijken.replace(-99999999, np.nan)
#gpdf_gemeenten = gpdf_gemeenten.replace(-99999999, np.nan)

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

def demografieAPI(text):
    df = Dataframe_demografie.loc[Dataframe_demografie['wijkcode'] == text]
    return df.to_dict(orient='list')

