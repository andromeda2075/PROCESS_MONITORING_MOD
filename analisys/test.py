import datetime
import matplotlib.pyplot as plt
import pandas as pd

d2 = {'name': ['Alice', 'Bob','Guiomar'],

      'score': [9.5, 8,10],

      'employed': [False, True,True],

      'kids': [0, 0,1]}
df2 = pd.DataFrame(data=d2)
print(df2)
df = pd.DataFrame()
df['name'] = d2['name']
print(df)