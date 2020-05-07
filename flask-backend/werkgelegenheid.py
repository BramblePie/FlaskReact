import pandas as pd
import geopandas as gpd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from prep import movecol

pd.set_option('display.max_rows', 50)

# Dataset inlezen
file = "raw-data/Vestegingen_Gemeente.csv"
postcode_file = "raw-data/provincie.xlsx"
data_pc = pd.read_excel(postcode_file)
data_vg = pd.read_csv(file, sep=";")

# Info over de kolommen
groepeerde_data_vg = data_vg.groupby(["Regio's", "Perioden"]).sum()
info_kolommen_vg = data_vg.info()

# Beschrijvende statistieken van de data
beschrijvende_stats_vg = data_vg.describe()

# Er zijn nu 2 datasets:
# - `data_vg` is de 'standaard' dataframe met alle kolommen en waardes die compleet zijn.
# - `groepeerde_data_vg` is de **gegroepeerde** dataset, gegroepeerd op de kolommen `Regio's` en `Perioden`.
# # Data Preparation
# Tijdens de analyse van de benodigde data worden de datasets `data_vg` en `groepeerde_data_vg` gebruikt. Van deze dataset wordt de data vanaf het jaar 2013 t/m 2018 gebruikt. De jaren 2019 en 2020 zijn wel beschikbaar, maar nog niet volledig.
# 
# Om te bepalen welke data gebruikt dient te worden, wordt er gekeken naar hoe de data aan de data mining goals kan voldoen. De data mining goal is: **Het verhogen van succesvolle woningzoekers die op zoek zijn naar een woonplek**.
# 
# De `data_vg` focust zich op het zoeken van mogelijke werkplekken van een woningzoekende in de ideale regio. De user story die beantwoordt dient te worden met de `data_vg` is **Als bezoeker wil ik graag dat werkgelegenheid mee wordt geteld in de resultaten, zodat ik kan de hoeveelheid mogelijke werkplekken per regio als resultaat zie**.
# 
# De meest recente data van `data_vg` wordt gebruikt om deze user story te beantwoorden. Deze nieuwe dataframe zal `data_vg_2018` heten.
# 
# Voor de volledigheid wordt voor elke periode een eigen dataframe gemaakt, in de syntax van de dataframe wordt dit weergegeven door `data_vg_[jaartal]`.
# 
# Ook wordt er een dataframe `data_pc` toegevoegd aan `data_vg`, zodat per regio de plaats, gemeente en provincie wordt weergegeven.

# ## Select Data
# 
# Van `data_vg_2018` worden alle kolommen gebruikt voor het beantwoorden van de user story.
# 
# Van `data_pc` wordt een aantal kolommen gebruikt, namelijk:
# - `Plaats`.
# - `Gemeente`.
# - `Provincie`.
# 
# ## Clean Data
# 
# In dit onderdeel wordt gekeken welke acties moeten worden ondernomen om de data op te schonen. Er wordt bijvoorbeeld gekeken naar rare waardes, aanpassingen in de records of overige acties.
# Unieke waarden in de verschillende kolommen van data_vg
test = ["Bedrijfstakken/branches SBI 2008", "Perioden", "Regio's", "Vestigingen (aantal)"]
for i in test:
    print(i, data_vg[i].unique())

# Uit de vorige functie is te herlijden dat:
# - `Bedrijfstakken/branches SBI 2008` heeft geen opmerkelijke waarden. Alle records zijn volgens hetzelfde format ingevuld.
# - `Perioden` is gereed voor gebruik.
# - `Regio's` heeft een aantal dubbele waarden, maar die worden weer gescheiden door de afkorting van de province van de Regio.
# - `Vestigingen (aantal)` heeft een opmerkelijke notatie die op basis van vorige functie anders word weergegeven dan in de tabelweergave. De waarden zijn echter correct en hetzelfde, maar met een andere notatie. Het valt op dat er in deze kolom een NaN waarde zit, dat dient aangepast te worden.

# Controleren op de lege waardes
# data_vg_incl_provincie.isna().sum()

# Invullen van de Na/NaN waarden in kolom Vestigingen (aantal) door 0
data_vg2 = data_vg["Vestigingen (aantal)"].fillna(0)

# ## Construct data
# 
# Om de data bruikbaar te maken voor user input in het formulier, wordt een classificatie aangebracht aan het aantal vestigingen. De waarde van deze classificatie zal bepaald worden door de uitkomst van data_vg.describe() uit de data understanding. De klassen zijn:
# - `Laag`.
# - `Middel`.
# - `Hoog`.
# 
# Er wordt nog gewerkt aan een klasse `Geen` om de sectoren met 0 vestigingen te onderscheiden van de klasse `Laag`.

data_vg_incl_provincie = pd.merge(data_vg, data_pc, left_on="Regio's", right_on="Regio's")

data_vg_incl_provincie = movecol(data_vg_incl_provincie, cols_to_move=['Provincie'], ref_col="Regio's", place='After')

werkgelegenheid_groupby = data_vg_incl_provincie.groupby(['Provincie',"Regio's", 'Perioden', 'Bedrijfstakken/branches SBI 2008']).sum()

np.set_printoptions(threshold=np.inf)

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

werkgelegenheid_groupby

# # Uitkomst Analyse
# 
# Uit de analyse van deze notebook, wordt gekeken naar de requirements uit de User Input die de user story nodig heeft. Hieruit wordt geadviseerd welke opties de user moet kunnen invoeren in het formulier.
# 
# Vervolgens wordt er een advies gegeven wat voor beschrijvende statistieken en voorspellende aspecten uit de dataset toegepast kunnen worden, zodat ook die bijbehorende user stories uitgevoerd kunnen worden op de huidige dataset.

# ## User input in het formulier
# De huidige user story heeft als resultaat een aantal voorstellen voor verwerking in het formulier. De user story is:
# - **Als bezoeker wil ik graag dat werkgelegenheid mee wordt geteld in de resultaten, zodat ik kan de hoeveelheid mogelijke werkplekken per regio als resultaat zie**.
# 
# De dataset werkt met een classificatie van het aantal vestigingen per Regio per Bedrijfsbranche. Het aantal vestigingen zijn mogelijke werkplekken waar de user zou kunnen werken.
# 
# ### Advies Formulier
# In het formulier is het belangrijk dat de user een voorkeur voor bedrijfsbranche kan aanvinken. Dit zou bijvoorbeerld een lijstje met checkboxes kunnen zijn, zodat de user eventueel meerdere branches kan selecteren. Als extra optie kan de user aangeven welke klasse aan mogelijkheden het best bij de user past in bijvoorbeeld een drop down menu. Sommige gebruikers willen graag zo veel mogelijk opties zien, terwijl er ook gebruikers zijn die het fijner vinden om een geringe aantal opties te zien verschijnen.
# 
# ### Advies Beschrijvende statistieken en voorspellende aspecten
# De data in de analyse is gebaseerd op de periode 2018. Er is veel meer data beschikbaar van de perioden voor 2018 en een nog niet volledig overzicht van de jaren 2019 en 2020.
# 
# Voor het uitwerken van user stories over het beschrijvende gedeelte van deze dataset, kan gekeken worden naar de perioden voor 2018 en hier beschrijvende statistieken op uitvoeren. Er zou bijvoorbeeld een mooi overzicht van de ontwikkelingen van het aantal vestigingen van een bepaalde branche in een regio als overzicht gegeven kunnen worden.
# 
# Op basis van deze historische data kan ook een invulling gegeven worden aan het voorspellende aspect van de werkgelegenheid.

# def veiligheidAPI(text):
#     # voor elke client/ bezoeker
#     return data_voorspelling_groupby.reset_index().to_dict(orient="index")


def werkgelegenheidAPI(branche, vestigingsklasse, periode):
    
  pass
