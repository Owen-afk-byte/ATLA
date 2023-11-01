# for science
import pandas as pd
# for command line
import sys
# for string manipulation
import re
# for stopwords (ziph's law)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

script = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-08-11/avatar.csv')


# ******************************************************************************

def bestDirectors():

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

    # print(director_df)

    director_df['count'] = count.values

    print(director_df.sort_values(by='imdb_rating', ascending=False))

# ******************************************************************************

def chapPerChar():

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

def linesPerChar():

    # filter database to have each character in each chapter
    script_dialogue = script[['chapter', 'character']]

    # filter to remove 'Scene Description' from characters
    just_characters_no_scene_desc = script_dialogue.loc[script_dialogue["character"] != 'Scene Description' ]

    # should remove instances where 2 characters speak
    # for example "Katara and Sokka" is a value in the character column

    # count the number of chapters each character shows up in
    count_dialogue = just_characters_no_scene_desc.groupby('character').count()

    # rename the count column to something more appropriate
    count_no_line = count_dialogue.rename({'chapter': 'no. of lines'}, axis='columns')

    # sort the count
    sorted_dialogue = count_no_line.sort_values(by='no. of lines', ascending=False)

    print(sorted_dialogue)

# ******************************************************************************

def mostUsedWordsForChar():

    name = input('Enter character name: ')

    just_character = script[['character', 'full_text']].loc[script["character"] == name ]

    # print(just_character)

    all_dialogue = ' '.join(just_character['full_text'].tolist())

    # preprocess text

    # take away scene directions/descriptions
    all_dialogue = re.sub(r'\[.*?\]', '', all_dialogue)

    # replace all line breaks with a space
    all_dialogue = re.sub('\n', ' ', all_dialogue)

    # replace all special characters with a space
    all_dialogue = re.sub('[^A-Za-z0-9]+', ' ', all_dialogue)

    # replace all single characters with a space
    all_dialogue = re.sub(r'\b[a-zA-Z]\b', ' ', all_dialogue)

    # replace all double spaces with one space
    all_dialogue = re.sub(' +', ' ', all_dialogue)

    # remove leading and trailing spaces
    all_dialogue = all_dialogue.strip()

    # make all text lower case
    all_dialogue = all_dialogue.lower()

    # remove stop words from text
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(all_dialogue)
    filtered_dialogue = [w for w in word_tokens if not w in stop_words]

    # print(all_dialogue)

    # get word counts

    # words = list(all_dialogue.split(" "))

    word_count = {}

    for word in filtered_dialogue:
        if word not in word_count:
            word_count[word] = 1
        elif word in word_count:
            word_count[word] += 1

    # print(word_count)

    # turn counts into dataframe

    freq_words = pd.DataFrame([word_count])
    freq_words = freq_words.T
    freq_words = freq_words.rename(columns={0: 'Frequency'})

    # sort the counts

    sorted_freq = freq_words.sort_values(by='Frequency', ascending=False)

    # tidy up table

    # et the row index as a regular column
    sorted_freq.reset_index(level=0, inplace=True)

    # rename the column containing the row names to the desired name
    sorted_freq.rename(columns={'index': 'Words'}, inplace=True)

    print(sorted_freq)

# ******************************************************************************

if __name__ == '__main__':
    globals()[sys.argv[1]]()
