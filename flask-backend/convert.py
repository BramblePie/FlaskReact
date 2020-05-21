import pandas as pd
datamisdaad = pd.read_csv('data/misdrijven.csv')
data = pd.read_csv('form.csv')
data = data.merge(datamisdaad, on='gemeente')
data = data.drop_duplicates()
data.to_csv('form2.csv')