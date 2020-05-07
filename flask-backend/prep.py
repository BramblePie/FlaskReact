import pandas as pd
import geopandas as gpd
import seaborn as sb
import numpy as np
# import matplotlib.pyplot as plt
 
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