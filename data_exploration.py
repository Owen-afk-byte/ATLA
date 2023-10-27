import pandas as pd

script = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-08-11/avatar.csv')

# filter database for character_words entries that are not null
character_scripts = script[script['character_words'].notnull()]

# filter database to have unique chapter entries
script_unique_chapters = script.drop_duplicates(subset=['chapter'])

#create a new dataframe with only the director and imdb_rating columns
director_df = script_unique_chapters[['director', 'imdb_rating']]

#print mean of imdb_rating column for each director, sorted by highest to lowest
print(director_df.groupby('director').mean())

# add column to director_df that counts the number of chapter entries per director
# director_df['count'] = script_unique_chapters.groupby('director')['chapter'].count()

# print(director_df.sort_values(by='imdb_rating', ascending=False))