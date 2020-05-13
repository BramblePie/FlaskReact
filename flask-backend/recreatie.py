# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from Helper_functions import *


# %%
test1 = wfs_data("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",0)
test2 = wfs_data("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",1000)
test3 = wfs_data("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",2000)
test4 = wfs_data("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",3000)
test5 = wfs_data("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",4000)


# %%
df_recreatie = pd.concat([test1, test2, test3, test4, test5], ignore_index=True)


# %%
df_recreatie = df_recreatie[['aantal_woningen','aantal_woningen_bouwjaar_voor_1945','aantal_woningen_bouwjaar_45_tot_65','aantal_woningen_bouwjaar_65_tot_75','aantal_woningen_bouwjaar_75_tot_85','aantal_woningen_bouwjaar_85_tot_95','aantal_woningen_bouwjaar_95_tot_05','aantal_woningen_bouwjaar_05_tot_15','aantal_woningen_bouwjaar_15_en_later','gemiddelde_woz_waarde_woning','percentage_koopwoningen', 'percentage_huurwoningen','kinderdagverblijf_gemiddelde_afstand_in_km','kinderdagverblijf_aantal_binnen_1_km','kinderdagverblijf_aantal_binnen_3_km','kinderdagverblijf_aantal_binnen_5_km','buitenschoolse_opvang_gem_afstand_in_km','buitenschoolse_opvang_aantal_binnen_1_km','buitenschoolse_opvang_aantal_binnen_3_km','buitenschoolse_opvang_aantal_binnen_5_km','grote_supermarkt_gemiddelde_afstand_in_km','grote_supermarkt_aantal_binnen_1_km','grote_supermarkt_aantal_binnen_3_km','grote_supermarkt_aantal_binnen_5_km','winkels_ov_dagelijkse_levensm_gem_afst_in_km','winkels_ov_dagel_levensm_aantal_binnen_1_km','winkels_ov_dagel_levensm_aantal_binnen_3_km','winkels_ov_dagel_levensm_aantal_binnen_5_km','warenhuis_gemiddelde_afstand_in_km', 'warenhuis_aantal_binnen_5_km',
'warenhuis_aantal_binnen_10_km', 'warenhuis_aantal_binnen_20_km','cafe_gemiddelde_afstand_in_km', 'cafe_aantal_binnen_1_km','cafe_aantal_binnen_3_km', 'cafe_aantal_binnen_5_km','cafetaria_gemiddelde_afstand_in_km', 'cafetaria_aantal_binnen_1_km','cafetaria_aantal_binnen_3_km', 'cafetaria_aantal_binnen_5_km','restaurant_gemiddelde_afstand_in_km','restaurant_aantal_binnen_1_km','restaurant_aantal_binnen_3_km', 'restaurant_aantal_binnen_5_km','hotel_gemiddelde_afstand_in_km', 'hotel_aantal_binnen_5_km','hotel_aantal_binnen_10_km', 'hotel_aantal_binnen_20_km','treinstation_gemiddelde_afstand_in_km','overstapstation_gemiddelde_afstand_in_km','brandweerkazerne_gemiddelde_afstand_in_km','geometry']]


# %%
zipfile = "zip://flask-backend/Postcode4.zip"
df = gpd.read_file(zipfile)



# %%
df_recreatie = pd.concat([df_recreatie, df['PC4']], axis=1)
df_recreatie = df_recreatie[['PC4','aantal_woningen', 'aantal_woningen_bouwjaar_voor_1945',
       'aantal_woningen_bouwjaar_45_tot_65',
       'aantal_woningen_bouwjaar_65_tot_75',
       'aantal_woningen_bouwjaar_75_tot_85',
       'aantal_woningen_bouwjaar_85_tot_95',
       'aantal_woningen_bouwjaar_95_tot_05',
       'aantal_woningen_bouwjaar_05_tot_15',
       'aantal_woningen_bouwjaar_15_en_later', 'gemiddelde_woz_waarde_woning',
       'percentage_koopwoningen', 'percentage_huurwoningen',
       'kinderdagverblijf_gemiddelde_afstand_in_km',
       'kinderdagverblijf_aantal_binnen_1_km',
       'kinderdagverblijf_aantal_binnen_5_km',
       'buitenschoolse_opvang_gem_afstand_in_km',
       'buitenschoolse_opvang_aantal_binnen_1_km',
       'buitenschoolse_opvang_aantal_binnen_5_km',
       'grote_supermarkt_gemiddelde_afstand_in_km',
       'grote_supermarkt_aantal_binnen_1_km',
       'grote_supermarkt_aantal_binnen_5_km',
       'winkels_ov_dagelijkse_levensm_gem_afst_in_km',
       'winkels_ov_dagel_levensm_aantal_binnen_1_km',
       'winkels_ov_dagel_levensm_aantal_binnen_5_km',
       'warenhuis_gemiddelde_afstand_in_km', 'warenhuis_aantal_binnen_5_km',
       'warenhuis_aantal_binnen_10_km', 'warenhuis_aantal_binnen_20_km',
       'cafe_gemiddelde_afstand_in_km', 'cafe_aantal_binnen_1_km', 'cafe_aantal_binnen_5_km',
       'cafetaria_gemiddelde_afstand_in_km', 'cafetaria_aantal_binnen_1_km', 'cafetaria_aantal_binnen_5_km',
       'restaurant_gemiddelde_afstand_in_km', 'restaurant_aantal_binnen_1_km', 'restaurant_aantal_binnen_5_km',
       'hotel_gemiddelde_afstand_in_km', 'hotel_aantal_binnen_5_km',
       'hotel_aantal_binnen_10_km', 'hotel_aantal_binnen_20_km',
       'treinstation_gemiddelde_afstand_in_km',
       'overstapstation_gemiddelde_afstand_in_km',
       'brandweerkazerne_gemiddelde_afstand_in_km', 'geometry']]


# %%
df_recreatie = df_recreatie.replace('-99997', np.nan)

# %%
df_recreatie_formulier = df_recreatie
lijst = df_recreatie_formulier[['aantal_woningen_bouwjaar_voor_1945',
       'aantal_woningen_bouwjaar_45_tot_65',
       'aantal_woningen_bouwjaar_65_tot_75',
       'aantal_woningen_bouwjaar_75_tot_85',
       'aantal_woningen_bouwjaar_85_tot_95',
       'aantal_woningen_bouwjaar_95_tot_05',
       'aantal_woningen_bouwjaar_05_tot_15',
       'aantal_woningen_bouwjaar_15_en_later','gemiddelde_woz_waarde_woning',
       'percentage_koopwoningen', 'percentage_huurwoningen',
       'kinderdagverblijf_gemiddelde_afstand_in_km',
       'kinderdagverblijf_aantal_binnen_1_km',
       'kinderdagverblijf_aantal_binnen_5_km',
       'buitenschoolse_opvang_gem_afstand_in_km',
       'buitenschoolse_opvang_aantal_binnen_1_km',
       'buitenschoolse_opvang_aantal_binnen_5_km',
       'grote_supermarkt_gemiddelde_afstand_in_km',
       'grote_supermarkt_aantal_binnen_1_km',
       'grote_supermarkt_aantal_binnen_5_km',
       'winkels_ov_dagelijkse_levensm_gem_afst_in_km',
       'winkels_ov_dagel_levensm_aantal_binnen_1_km',
       'winkels_ov_dagel_levensm_aantal_binnen_5_km',
       'warenhuis_gemiddelde_afstand_in_km', 'warenhuis_aantal_binnen_5_km',
       'warenhuis_aantal_binnen_10_km', 'warenhuis_aantal_binnen_20_km',
       'cafe_gemiddelde_afstand_in_km', 'cafe_aantal_binnen_1_km', 'cafe_aantal_binnen_5_km',
       'cafetaria_gemiddelde_afstand_in_km', 'cafetaria_aantal_binnen_1_km', 'cafetaria_aantal_binnen_5_km',
       'restaurant_gemiddelde_afstand_in_km', 'restaurant_aantal_binnen_1_km', 'restaurant_aantal_binnen_5_km',
       'hotel_gemiddelde_afstand_in_km', 'hotel_aantal_binnen_5_km',
       'hotel_aantal_binnen_10_km', 'hotel_aantal_binnen_20_km',
       'treinstation_gemiddelde_afstand_in_km',
       'overstapstation_gemiddelde_afstand_in_km',
       'brandweerkazerne_gemiddelde_afstand_in_km']]

for x in lijst:
    kolom = df_recreatie_formulier[[x]]
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(kolom)
    df_recreatie_formulier[x + "_genormaliseerd"] = pd.DataFrame(x_scaled)
    df_recreatie_formulier = movecol(df_recreatie_formulier, cols_to_move=[x + "_genormaliseerd"], ref_col=x, place='After')
# %%
df_recreatie_formulier = df_recreatie_formulier.rename(columns={"PC4": "postcode"})
df_recreatie = df_recreatie.rename(columns={"PC4": "postcode"})
# %%
df_toevoeging = pd.read_csv('flask-backend/dataset.csv')
df_toevoeging = df_toevoeging[['postcode','gemeente']]

# %%
df_recreatie = pd.merge(df_recreatie, df_toevoeging, on='postcode', how='left')
df_recreatie_formulier = pd.merge(df_recreatie_formulier, df_toevoeging, on='postcode', how='left')
df_recreatie = movecol(df_recreatie, cols_to_move=['gemeente'], ref_col='postcode', place='After')
df_recreatie_formulier = movecol(df_recreatie_formulier, cols_to_move=['gemeente'], ref_col='postcode', place='After')
df_recreatie.drop(columns=['aantal_woningen_bouwjaar_voor_1945_genormaliseerd'])
df_recreatie.drop(columns=['geometry'])
# %%
def RecreatieAPI_Postcode(postcode):
    df = df_recreatie.loc[df_recreatie['postcode'] == postcode]
    return df.to_dict()

def RecreatieAPI_Gemeente(gemeente):
    df = df_recreatie.loc[df_recreatie['gemeente'] == gemeente]
    return df.to_dict()
    

