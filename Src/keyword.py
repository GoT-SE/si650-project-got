import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim.models.word2vec as w2v
import os

def list2dict(keys, values):
    dictionary = {}
    for idx, key in enumerate(keys):
        if not key in dictionary.keys():
            dictionary[key] = []
        dictionary[key].append(values[idx])
    return dictionary

def build_dataset():
    review_episode = pd.read_table("../Data/review-by-line.dat", sep='\t', header=None)
    reviews = list2dict(review_episode[0], review_episode[1])

    summary_episode = pd.read_table("../Data/summary-by-line.dat", sep='\t', header=None)
    summaries = list2dict(summary_episode[0], summary_episode[1])

    episodes = pd.read_table("../Data/got.dat", sep='\t', header=None)
    episode_ids = episodes[0]
    episode_names = episodes[1]
    episode_scipts = episodes[2]
    
    got_data = {}
    for idx, episode_id in enumerate(episode_ids):
        got_data[idx] = {}
        got_data[idx]["id"] = episode_id
        got_data[idx]["name"] = episode_names[idx]
        got_data[idx]["script"] = episode_scipts[idx]
        try:
            got_data[idx]["summary"] = summaries.get(episode_names[idx])
            got_data[idx]["review"] = reviews.get(episode_id)
        except:
            print(episode_names[idx], episode_id)
    
    f = open("../Data/got.json","w")
    json.dump(got_data, f)
    f.close()

def set_stopwords():
    stop = set(stopwords.words("english"))
    for line in open("../Data/lemur-stopwords.txt"):
        stop.add(line.strip('\n'))
    return stop

def load_data(data_type):
    f_data = open('../Data/got.json', 'r')
    data = json.loads(f_data.read())
    stopwords = set_stopwords()
    words = []
    for idx, sentence in data.items():
        try:
            sent = word_tokenize(sentence.get(data_type))
            filtered = [w for w in sent if not w in stopwords]
            words.extend(filtered)
        except:
            print(idx)
    return words

def train_data(data, set_name):
    model = w2v.Word2Vec(
        sg=1,
        seed=1,
        size=300,
        min_count=3,
        window=7,
        sample=1e-3
    )
    model.build_vocab(data)
    model.train(data, total_examples=model.corpus_count, epochs=model.epochs)
    if not os.path.exists("trained"):
        os.makedirs("trained")
    model.save(os.path.join("trained", set_name+"_w2v.pkl"))

def synSubstitution(query):
    return 0

if __name__ == "__main__":
    # data_type choose from review, summary and script
    data = load_data("summary")
    train_data(data, "summary")
    
    # f_syn = open('../Data/synonyms.json', 'r')
    # syn_dict = json.loads(f_syn.read())
