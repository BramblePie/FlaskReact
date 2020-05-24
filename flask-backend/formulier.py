import pandas as pd
datawoz = pd.read_csv('data/datasetwoznormaliseerd.csv')
datawoz = datawoz.drop(columns=['geometry', 'Unnamed: 0'])
datamisdaad = pd.read_csv('data/misdrijven.csv')
datamisdaad = datamisdaad.rename(columns={"Regio's": "gemeente",})
datamisdaad = datamisdaad.drop(columns=[ 'Unnamed: 0'])
datamisdaad = datamisdaad.loc[(datamisdaad['Soort_misdrijf'] == 'Misdrijven, totaal') & (datamisdaad['Perioden'] == '2019*')]
datademografie = pd.read_csv('data/Demografie_wijken_data.csv')
datademografie = datademografie.rename(columns={"gemeentenaam": "gemeente",})
datademografie = datademografie.drop(columns=['id','wijkcode','jrstatcode','gemeentecode','ind_wbi','Unnamed: 0','geometry','percentage_westerse_migratieachtergrond','percentage_niet_westerse_migratieachtergrond','percentage_uit_marokko','percentage_uit_nederlandse_antillen_en_aruba','percentage_uit_suriname', 'percentage_uit_turkije','percentage_overige_nietwestersemigratieachtergrond'])
datawerk = pd.read_csv('data/werkgelegenheid_df.csv')
datawerk = datawerk.rename(columns={"Regio's": "gemeente",})
datawerk = datawerk.drop(columns=['Unnamed: 0'])
data = datademografie.merge(datawoz, on='gemeente')
data = data.drop_duplicates()
data = data.merge(datawerk, on='gemeente')
data = data.drop_duplicates()
data = data.merge(datamisdaad, on='gemeente')
data = data.drop_duplicates()
def formulierAPI(stedelijkheidinput,wozinput,werkgelegenheidinput,Bedrijfstakinput,misdaadinput):
    resultaat = data.loc[(data['klasse_stedelijkheid_normalisatie'] == stedelijkheidinput) & (data['klasse_woz'] == wozinput)& (data['Vestigingen Klasse'] == werkgelegenheidinput) & (data['Bedrijfstak'] == Bedrijfstakinput)& (data['Aantal_misdrijven_klasse'] == misdaadinput)]
    output = resultaat[['gemeente']].drop_duplicates()
    return output.to_dict(orient='records')
#dit is de api voor het vinden van gemeenten waar je kunt wonen