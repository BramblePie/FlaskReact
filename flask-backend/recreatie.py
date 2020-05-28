from Helper_functions import *

test1 = wfs_data_rec("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",0)
test2 = wfs_data_rec("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",1000)
test3 = wfs_data_rec("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",2000)
test4 = wfs_data_rec("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",3000)
test5 = wfs_data_rec("https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?language=eng&", "cbspostcode4:postcode42017",4000)
df_recreatie = pd.concat([test1, test2, test3, test4, test5], ignore_index=True)
# Info over de kolommen in perceelprijzen
info_kolommen_recreatie = df_recreatie.info()
# Beschrijvende statistieken van de data
beschrijvende_stats_recreatie = df_recreatie.describe(exclude='geometry')

#Dataframe maken van alleen recreatie onderdelen binnen 5km
df_recreatie = df_recreatie[['aantal_inwoners','winkels_ov_dagel_levensm_aantal_binnen_5_km', 'warenhuis_aantal_binnen_5_km', 'cafe_aantal_binnen_5_km', 'cafetaria_aantal_binnen_5_km', 'restaurant_aantal_binnen_5_km', 'hotel_aantal_binnen_5_km']]

#postcode zip inladen
zipfile = "zip://raw-data/Postcode4.zip"
df = gpd.read_file(zipfile)

#Postcodezip en df samenvoegen en hernoemen
df_recreatie = pd.concat([df_recreatie, df['PC4']], axis=1)
df_recreatie = df_recreatie.rename(columns={"PC4": "postcode"})
df_recreatie = movecol(df_recreatie, cols_to_move=['postcode'], ref_col='winkels_ov_dagel_levensm_aantal_binnen_5_km', place='After')
df_recreatie = movecol(df_recreatie, cols_to_move=['winkels_ov_dagel_levensm_aantal_binnen_5_km'], ref_col='postcode', place='After')
df_recreatie = movecol(df_recreatie, cols_to_move=['aantal_inwoners'], ref_col='postcode', place='After')

df = pd.read_csv('raw-data/postcode_gemeente.csv', index_col=0)
df = df.rename(columns={"Gemeentenaam2019":"gemeente"})
df_recreatie = df_recreatie.merge(df, on='postcode')
df_recreatie = movecol(df_recreatie, cols_to_move=['gemeente'], ref_col='postcode', place='After')

#nulwaardes als string omzetten naar 0
df_recreatie = df_recreatie.replace('-99997', 0)

#normaliseren
lijst = df_recreatie[['winkels_ov_dagel_levensm_aantal_binnen_5_km',
       'warenhuis_aantal_binnen_5_km', 'cafe_aantal_binnen_5_km',
       'cafetaria_aantal_binnen_5_km', 'restaurant_aantal_binnen_5_km',
       'hotel_aantal_binnen_5_km']]

for x in lijst:
    kolom = df_recreatie[[x]]
    
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(kolom)
    df_recreatie[x + "_genormaliseerd"] = pd.DataFrame(x_scaled)
    df_recreatie = movecol(df_recreatie, cols_to_move=[x + "_genormaliseerd"], ref_col=x, place='After')

#klasses aanmaken op basis van quantiles
for x in lijst:
    kolom = df_recreatie[x + "_genormaliseerd"]

    q_25 = kolom.quantile(q=.25)
    q_50 = kolom.quantile(q=.5)
    q_75 = kolom.quantile(q=.75)
    
    m1 = np.logical_and(kolom <= q_25, kolom != 0)
    m2 = np.logical_and(kolom >= q_25, kolom < q_50)
    m3 = np.logical_and(kolom >= q_50, kolom < q_75)
    m4 = kolom > q_75
    
    df_recreatie[x + "_klasse"] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')
    df_recreatie = movecol(df_recreatie, cols_to_move=[x + "_klasse"], ref_col=x + '_genormaliseerd', place='After')

def recreatieAPI(recreatie, klasse):
    resultaat = df_recreatie.loc[((df_recreatie[recreatie + "_aantal_binnen_5_km_klasse"] == klasse))]
    resultaat = resultaat[['postcode', 'gemeente', 'winkels_ov_dagel_levensm_aantal_binnen_5_km',
       'winkels_ov_dagel_levensm_aantal_binnen_5_km_klasse',
       'warenhuis_aantal_binnen_5_km',
       'warenhuis_aantal_binnen_5_km_klasse', 'cafe_aantal_binnen_5_km',
       'cafe_aantal_binnen_5_km_klasse', 'cafetaria_aantal_binnen_5_km',
       'cafetaria_aantal_binnen_5_km_klasse', 'restaurant_aantal_binnen_5_km',
       'restaurant_aantal_binnen_5_km_klasse', 'hotel_aantal_binnen_5_km',
       'hotel_aantal_binnen_5_km_klasse']]
    return resultaat.to_dict(orient="records")