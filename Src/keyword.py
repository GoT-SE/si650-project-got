import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
import gensim.models.word2vec as w2v

def list2dict(keys, values):
    dictionary = {}
    for idx, key in enumerate(keys):
        if not key in dictionary.keys():
            dictionary[key] = []
        dictionary[key].append(values[idx])
    return dictionary

def 

if __name__ == "__main__":
    review_episode = pd.read_table("../Data/review-by-line.dat", sep='\t', header=None)
    reviews = list2dict(review_episode[0], review_episode[1])

    summary_episode = pd.read_table("../Data/summary-by-line.dat", sep='\t', header=None)
    summaries = list2dict(summary_episode[0], summary_episode[1])

    episodes = pd.read_table("../Data/got.dat", sep='\t', header=None)
    episode_names = list2dict(episodes[1], episodes[0])

    f_syn = open('../Data/synonyms.json', 'r')
    syn_dict = json.loads(f_syn.read())

    tokenizer = 
