# tests gendered language, flesh reading ease, type-token ratio for riddles

from textstat.textstat import textstatistics, legacy_round
from os import listdir
from math import inf
from statistics import stdev
from collections import Counter
import re

def get_text(inputFn):
    with open(inputFn) as inputFileHandle:
        return inputFileHandle.read()


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


def average_flesch(file_list):
    complete = []
    for file in file_list:
        item = get_text(file)
        complete.append(flesch_reading_ease(item))
        
    print("Standard deviation: " + str(stdev(complete)))

    print("Average: " + str(sum(complete)/len(file_list)))
    print("Maximum: " + str(max(complete)))
    print("Minimum: " + str(min(complete)))


def type_token(text):
    c = create_collection(text)

    types = len(c)
    tokens = 0
    for value in c.values():
        tokens+=value
    tt = types/tokens

    if tt <.23:
        print("\nMIN")
        print(text)

    return tt


def average_tt(file_list):
    complete = []
    for file in file_list:
        text = get_text(file)
        complete.append(type_token(text))
    print(min(complete))
    print("Standard deviation: " + str(stdev(complete)))
    print("Average: " + str(sum(complete)/len(file_list)))


def pronoun_usage(text):
    c = create_collection(text)
    female = ['she', 'her', 'hers', 'herself']
    male = ['he', 'his', 'him', 'himself']
    neutral = ['it', 'one', 'they', 'its', 'itself', 'one\'s', 'theirs', 'them'\
               'themselves', 'themself']

    words = {'male':0, 'female':0, 'neutral':0, 'total':0}

    total_words = 0
    for key in c:
        words['total']+=c[key]

    for key in c:
        if key in male:
            words['male']+=c[key]
        elif key in female:
            words['female']+=c[key]
        elif key in neutral:
            words['neutral']+=c[key]

    
    if words['male']/words['total'] > .099:
        print('MALE')
        print(text)
        print()
        print()
        print()

    if words['female']/words['total'] > .069:
        print("FEMALE")
        print(text)
        print()
        print()
        print()

    if words['neutral']/words['total'] > .07:
        print("neutral")
        print(text)
        print()
        print()
        print()
    return words


def average_pronouns(file_list):
    pronouns = []
    for file in file_list:
        text = get_text(file)
        d = pronoun_usage(text)
        pronouns.append(d)

    males = [c['male']/c['total'] for c in pronouns]
    females = [c['female']/c['total'] for c in pronouns]
    neutral = [c['neutral']/c['total'] for c in pronouns]

    print(max(males))
    print(max(females))
    print(max(neutral))

    print("Standard deviation (male): " + str(stdev(males)))
    print("Standard deviation (female): " + str(stdev(females)))
    print("Standard deviation (neutral): " + str(stdev(neutral)))

    # print("Average (male): " + str(sum(males)/sum(pronouns)))
    # print("Average (female): " + str(sum(females)/sum(pronouns)))
    # print("Average (neutral): " + str(sum(neutral)/sum(pronouns)))


def main():
    directory = "/Users/ndrezn/OneDrive - McGill University/McGill/research/riddles/content/all/"
    file_list = [directory+f for f in listdir(directory) if not f.startswith('.')]

    average_tt(file_list)
    # average_tt(file_list)


if __name__ == '__main__':
    main()