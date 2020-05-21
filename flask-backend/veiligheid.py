# Benodigde Libraries importeren

from Helper_functions import *

# Dataset inlezen
file = "flask-backend/raw-data/Veiligheid.csv"
data_veiligheid = pd.read_csv(file, sep=";")

# ## Data exploratie
# Alle soorten misdrijven die er minimaal 1 keer in voorkomen
soorten_misdrijven = data_veiligheid["Soort misdrijf"].drop_duplicates()

# ## Data Preperation
# Kolomnamen van de dataset wijzigen

data_veiligheid_nieuw = data_veiligheid
data_veiligheid_nieuw.rename(columns={'Soort misdrijf':'Soort_misdrijf','Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)':'Aantal_misdrijven', 'Geregistreerde misdrijven/Geregistreerde misdrijven, relatief (% van totaal geregistreerde misdrijven)':'Misdrijven_relatief(%)', 'Geregistreerde misdrijven/Geregistreerde misdrijven per 1000 inw.  (per 1 000 inwoners)':'Aantal_misdrijven(per_1000_inw)'}, inplace=True)
data_veiligheid_nieuw = data_veiligheid_nieuw.drop(columns=["Aantal_misdrijven(per_1000_inw)"])

# Nieuwe dataset inladen voor mergen dataset, zodat regio's ook provincie er achter heeft staan
file = "flask-backend/raw-data/gemeenten-provincie.xlsx"
postcode = pd.read_excel(file) 

# Dataframe maken van de dataset
df2 = pd.DataFrame(postcode)

# Kolom hernoemen
postcode.rename(columns={"Gemeente":"Regio's"}, inplace=True)

# Dataframe opnieuw defineren
df2 = pd.DataFrame(postcode)

# Mergen van 2 dataset op de Regio's kolom
data_veiligheid_incl_provincie = data_veiligheid_nieuw.merge(df2, on="Regio's")

data_veiligheid_incl_provincie = movecol(data_veiligheid_incl_provincie, cols_to_move=['Provincie'], ref_col="Regio's", place='After')

# Alle Gemeentelijke records groeperen in de bijbehorende Provincie
provincies = sorted(data_veiligheid_incl_provincie["Provincie"].drop_duplicates())

# Genormaliseerde waarde uitrekenen met MinMaxScaler en Classificatie toevoegen
min_max_scaler = preprocessing.MinMaxScaler()

aantal_misdrijven_minmax = min_max_scaler.fit_transform(data_veiligheid_incl_provincie[["Aantal_misdrijven"]])
data_veiligheid_incl_provincie["Aantal_misdrijven_genormaliseerd"] = aantal_misdrijven_minmax

m1 = data_veiligheid_incl_provincie['Aantal_misdrijven_genormaliseerd'] < 0.000105
m2 = data_veiligheid_incl_provincie['Aantal_misdrijven_genormaliseerd'] > 0.003222

data_veiligheid_incl_provincie['Aantal_misdrijven_geklasseerd'] = np.select([m1,m2], ['Laag','Hoog'], default='Middel')

#nieuwe index maken voor Flask
misdrijven_df = data_veiligheid_incl_provincie
misdrijven_df

# Functions zijn ready
print("Functions ready")

# Define functions
def veiligheidAPI(plaats):
    # voor elke client/ bezoeker
    resultaat = misdrijven_df.loc[(misdrijven_df["Regio's"] == plaats)]
    return resultaat.to_dict(orient="records")

#Klaar