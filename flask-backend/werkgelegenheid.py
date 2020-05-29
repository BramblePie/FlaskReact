from Helper_functions import *

# Dataset inlezen
file = "raw-data/Vestigingen__gemeente.csv"
postcode_file = "raw-data/gemeenten-provincie.xlsx"
data_pc = pd.read_excel(postcode_file)
data_vg = pd.read_csv(file, sep=";")

# Invullen van de Na/NaN waarden in kolom Vestigingen (aantal) door 0
data_vg2 = data_vg["Vestigingen (aantal)"].fillna(0)
data_vg_incl_provincie = pd.merge(data_vg, data_pc, left_on="Regio's", right_on="Regio's")
data_vg_incl_provincie = movecol(data_vg_incl_provincie, cols_to_move=['Provincie'], ref_col="Regio's", place='After')
werkgelegenheid_groupby = data_vg_incl_provincie.groupby(['Provincie',"Regio's", 'Perioden', 'Bedrijfstakken/branches SBI 2008']).sum()
min_max_scaler = preprocessing.MinMaxScaler()
aantal_vestigingen_minmax = min_max_scaler.fit_transform(data_vg_incl_provincie[["Vestigingen (aantal)"]])
werkgelegenheid_groupby["Aantal_vestigingen_genormaliseerd"] = aantal_vestigingen_minmax

# De data van werkgelegenheid_groupby wordt gecategoriseerd op een `Laag`, `Middel` of `Hoog` aantal vestigingen in een bepaalde branche.
vestigingen = werkgelegenheid_groupby["Vestigingen (aantal)"]

# Gebruik de kwantielen van werkgelegenheid_groupby staan
werk_25 = vestigingen.quantile(q=.25)
werk_50 = vestigingen.quantile(q=.5)
werk_75 = vestigingen.quantile(q=.75)
m1 = np.logical_and(vestigingen < werk_25, vestigingen != 0)
m2 = np.logical_and(vestigingen >  werk_25, vestigingen < werk_50)
m3 = np.logical_and(vestigingen >  werk_50, vestigingen < werk_75)
m4 = vestigingen > werk_75

werkgelegenheid_groupby["Vestigingen Klasse"] = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')
werkgelegenheid_groupby_index = werkgelegenheid_groupby.reset_index()
splitten_bedrijfstak = werkgelegenheid_groupby_index["Bedrijfstakken/branches SBI 2008"].str.split(" ", n=1, expand=True)
samenvoegen_df = pd.merge(werkgelegenheid_groupby_index, splitten_bedrijfstak, left_index=True, right_index=True)
samenvoegen_df.rename(columns={0:'Bedrijfstak_code', 1:'Bedrijfstak'}, inplace=True)
werkgelegenheid_geprept = movecol(samenvoegen_df, cols_to_move=['Bedrijfstak_code', 'Bedrijfstak'], ref_col="Perioden", place='After')
werkgelegenheid_df= werkgelegenheid_geprept.drop(columns='Bedrijfstakken/branches SBI 2008')

def werkgelegenheidAPI(branche_code, klasse):
    resultaat = werkgelegenheid_df.loc[((werkgelegenheid_df["Bedrijfstak_code"] == branche_code) & (werkgelegenheid_df["Vestigingen Klasse"] == klasse))]
    return resultaat.to_dict(orient="records")
print("Gefixed")