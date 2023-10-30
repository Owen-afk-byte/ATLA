import pandas as pd

script = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-08-11/avatar.csv')


# ******************************************************************************

# filter database for character_words entries that are not null
character_scripts = script[script['character_words'].notnull()]

# filter database to have unique chapter entries
script_unique_chapters = script.drop_duplicates(subset=['chapter'])

#create a new dataframe with only the director and imdb_rating columns
director_df = script_unique_chapters[['director', 'imdb_rating']]

#print mean of imdb_rating column for each director, sorted by highest to lowest
director_df = director_df.groupby('director').mean()

# add column to director_df that counts the number of chapter entries per director
count = script_unique_chapters.groupby('director')['chapter'].count()

print(director_df)

director_df['count'] = count.values

print(director_df.sort_values(by='imdb_rating', ascending=False))

# ******************************************************************************

# filter database to have each character in each chapter
script_characters = script[['chapter', 'character']].drop_duplicates(subset=['chapter', 'character'])

# filter to remove 'Scene Description' from characters
just_characters = script_characters.loc[script_characters["character"] != 'Scene Description' ]

# should remove instances where 2 characters speak
# for example "Katara and Sokka" is a value in the character column

# count the number of chapters each character shows up in
count_characters = just_characters.groupby('character').count()

# rename the count column to something more appropriate
count_characters = count_characters.rename({'chapter': 'no. of chapters'}, axis='columns')

# sort the count
sorted_count = count_characters.sort_values(by='no. of chapters', ascending=False)

print(sorted_count)

# ******************************************************************************
