# runs the flesch reading ease test in 1-year blocks and finds the average

# complexity of riddles over time, plots it using matplotlib

from textstat.textstat import textstatistics, legacy_round
from os import listdir
from math import inf
from statistics import stdev
from collections import Counter
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 0 to display graphs of the average number of male/female pronouns per riddle per year
# 1 to display graphs of the average Flesch reading ease score per riddle per year
test = 0

riddles = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/gale/cleaned_metadata.csv")

# clean up the dataframe
riddles = riddles[pd.notnull(riddles.CONTENT)]
riddles = riddles[pd.notnull(riddles.DATE)]
riddles['DATE'] = pd.to_datetime(riddles['DATE'])
riddles = riddles.reset_index()

years = [item.year for item in riddles['DATE']]
riddles['YEAR'] = years

riddles = riddles.loc[riddles['PUBLICATION']!="Our Young Folk's Weekly Budget"]
riddles = riddles.reset_index()

print("There are " + str(len(riddles)) + " riddles in the current set.")

def create_collection(document):
    c = Counter(
        # set to lower case
        word.lower()
        # remove punctuation
        for word in re.findall(r'\b[^\W\d_]+\b', document))
    return c

def flesch_reading_ease(text):
    syllables_ct = textstatistics().syllable_count(text)
    word_ct = len(text.split())
    sentences_ct = len(text.split("."))-1

    avg_syllables = syllables_ct/word_ct
    avg_words = word_ct/sentences_ct

    FRE = 206.835 - (1.015 * avg_words) - (84.6 * avg_syllables)

    return legacy_round(FRE, 2)

def pronoun_usage(text):
    c = create_collection(text)
    female = ['she', 'her', 'hers', 'herself']
    male = ['he', 'his', 'him', 'himself']

    words = {'male':0, 'female':0, 'total':0}

    for key in c:
        words['total']+=c[key]
        if key in male:
            words['male']+=c[key]
        elif key in female:
            words['female']+=c[key]

    return words['total'], words['female']/words['total']



print("Analysis done.")

def graph_flesch():
    fr = [flesch_reading_ease(item) for item in riddles['CONTENT']]
    riddles['FLESCH'] = fr
    g = riddles.groupby(['YEAR'], as_index=False)
    yearly_averages = g.agg({"FLESCH":np.mean})
    print(yearly_averages)
    yearly_averages.plot(x='YEAR', y='FLESCH', title="Average Flesch reading ease score for riddles released each year")
    plt.show()

def graph_pron():
    pron = [pronoun_usage(item) for item in riddles['CONTENT']]
    male,female = zip(*pron)
    riddles['TOKENS'] = male
    riddles['FEMALE_PRONOUNS'] = female
    g = riddles.groupby(['YEAR'], as_index=False)
    yearly_averages = g.agg({"TOKENS":np.mean})
    print(yearly_averages)
    yearly_averages.plot(x='YEAR', y='TOKENS', title="Average tokens per riddle per year (not including riddles published in \"Our Young Folk's Weekly Budget\")")
    plt.show()

    yearly_averages = g.agg({"FEMALE_PRONOUNS":np.mean})
    print(yearly_averages)
    yearly_averages.plot(x='YEAR', y='FEMALE_PRONOUNS', title="Average female pronouns as a percentage of all tokens per riddle per year")
    plt.show()

if test == 0:
    graph_pron()
else:
    graph_flesch()
