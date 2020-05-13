
import pandas as pd
import geopandas as gpd
# import seaborn as sb
import numpy as np
# import matplotlib.pyplot as plt

from sklearn import preprocessing

# FUNCTIE VOOR HET REORDENEN VAN KOLOMMEN
# --------------------------------------


def movecol(df, cols_to_move=[], ref_col='', place='After'):

    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]

    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]

    return(df[seg1 + seg2 + seg3])


print("Prepping veiligheid")

# Dataset inlezen

file = "raw-data/Veiligheid.csv"
data_veiligheid = pd.read_csv(file, sep=";")

df = pd.DataFrame(data_veiligheid)

info_kolommen_veiligheid = data_veiligheid.info()


beschrijvende_stats_veiligheid = data_veiligheid.describe()

soorten_misdrijven = data_veiligheid["Soort misdrijf"].drop_duplicates()

data_veiligheid_nieuw = data_veiligheid

data_veiligheid_nieuw.rename(columns={'Soort misdrijf': 'Soort_misdrijf', 'Geregistreerde misdrijven/Totaal geregistreerde misdrijven (aantal)': 'Aantal_misdrijven',
                                      'Geregistreerde misdrijven/Geregistreerde misdrijven, relatief (% van totaal geregistreerde misdrijven)': 'Misdrijven_relatief(%)', 'Geregistreerde misdrijven/Geregistreerde misdrijven per 1000 inw.  (per 1 000 inwoners)': 'Aantal_misdrijven(per_1000_inw)'}, inplace=True)


data_veiligheid_nieuw.loc[data_veiligheid_nieuw['Aantal_misdrijven'] == 0]

file = "raw-data/gemeenten-provincie.xlsx"
postcode = pd.read_excel(file)

df2 = pd.DataFrame(postcode)

postcode.rename(columns={"Gemeente": "Regio's"}, inplace=True)

df2 = pd.DataFrame(postcode)

data_veiligheid_incl_provincie = data_veiligheid_nieuw.merge(df2, on="Regio's")


data_veiligheid_incl_provincie = movecol(data_veiligheid_incl_provincie, cols_to_move=[
                                         'Provincie'], ref_col="Regio's", place='After')


provincies = sorted(
    data_veiligheid_incl_provincie["Provincie"].drop_duplicates())


data_voorspelling_totaal = data_veiligheid_incl_provincie.loc[(
    (data_veiligheid_incl_provincie.Soort_misdrijf == 'Misdrijven, totaal'))]

totaal_provincie_perjaar = data_voorspelling_totaal.groupby(
    ['Provincie', 'Perioden']).sum()

totaal_misdrijven_pv_jaar = totaal_provincie_perjaar.drop(
    columns=['Misdrijven_relatief(%)'])

data_voorspelling_groupby = data_voorspelling_totaal.groupby(
    ['Perioden', "Regio's"]).sum()
np.set_printoptions(threshold=np.inf)

min_max_scaler = preprocessing.MinMaxScaler()

aantal_misdrijven_minmax = min_max_scaler.fit_transform(
    data_voorspelling_totaal[["Aantal_misdrijven"]])
data_voorspelling_groupby["Aantal_misdrijven_genormaliseerd"] = aantal_misdrijven_minmax

m1 = data_voorspelling_groupby['Aantal_misdrijven_genormaliseerd'] < 0.005357
m2 = data_voorspelling_groupby['Aantal_misdrijven_genormaliseerd'] > 0.017679

data_voorspelling_groupby['Aantal_misdrijven_geklasseerd'] = np.select(
    [m1, m2], ['Laag', 'Hoog'], default='Middel')

# gemeente = input('Voer hier een gemeente in')

# soortmisdrijf_regio_perjaar = data_veiligheid_incl_provincie.loc[(
#     (data_veiligheid_incl_provincie["Regio's"] == gemeente))]

# sb.pairplot(soortmisdrijf_regio_perjaar.groupby(
#     ["Perioden", "Soort_misdrijf"]).sum(), kind="reg")

# sb.pairplot(totaal_provincie_perjaar, kind="reg")


print("Functions ready")


def veiligheidAPI(text):
    # voor elke client/ bezoeker
    return data_voorspelling_groupby.to_dict(orient="index")
