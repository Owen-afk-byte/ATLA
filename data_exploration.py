import pandas as pd

script = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-08-11/avatar.csv')

# print first row
print(script.iloc[0])

# find best director
print(script[['director', 'imdb_rating']].groupby(['director']).mean())
