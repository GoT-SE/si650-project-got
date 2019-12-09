import json
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
import numpy as np
import sys

def set_stopwords():
    stop = set(stopwords.words("english"))
    for line in open("../Data/lemur-stopwords.txt"):
        stop.add(line.strip('\n'))
    return stop

def clean_text(texts): # list of strings
    import re
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    
    stopwords = set_stopwords()
    stopwords.add('ext')
    stopwords.add('int')
    res = []
    for text in texts:
        text = text.lower()

        text = re.sub("\'ve", " have ", text)
        text = re.sub("\'re", " are ", text)
        text = re.sub("n't", " not ", text)
        text = re.sub("\'ll", " will ", text)
        text = re.sub("cut to", " ", text)
        text = re.sub("scene shifts", " ", text)
        text = re.sub("scene", " ", text)

        text = re.sub("[^A-Za-z\n]", " ", text)
        text = re.sub("\n", " ", text)

        text = ' '.join([ps.stem(w) for w in word_tokenize(text) if (w not in stopwords) and (len(w) > 1)])
        if text != '':
            res.append(text)

    return res

def load_episode_data(data):
    if data == None: return []
    sents = clean_text(sent_tokenize(data))
    return sents

def getModel(data):
    import os
    import pickle
    if os.path.exists('trained/vec.pkl') and os.path.exists('trained/tfidf.pkl'):
        tfidf = pickle.load(open("trained/tfidf.pkl", "rb"))
        vec = pickle.load(open("trained/vec.pkl", "rb"))
        return vec, tfidf
    
    with open('../Data/episodes.json', 'r') as f:
        eps = json.loads(f.read())['episodes']

    import re

    docs = []
    for idx in data.keys():
        script = load_episode_data(data[idx]['script'])
        summary = load_episode_data(data[idx]['summary'])
        review = load_episode_data(data[idx]['review'])
        doc = script + summary + review
        toapp = ' '.join(doc)
        # episodes
        toapp += ' ' + eps[int(idx)]['episodeDescription']
        chlist = [scene['characters'] for scene in eps[int(idx)]['scenes']]
        scenes = []
        for s in chlist:
            for ch in s:
                scenes.append(re.sub('name', '', str(ch)))
        cleaned = clean_text(scenes)
        toapp += ' '.join(cleaned)
        docs.append(toapp)


    text_vector = TfidfVectorizer(sublinear_tf=True, max_features=10000, max_df=0.85, ngram_range=(1,2), analyzer='word')
    tfidf = text_vector.fit_transform(docs)

    pickle.dump(tfidf, open("trained/tfidf.pkl", "wb"))
    pickle.dump(text_vector, open("trained/vec.pkl", "wb"))
    return text_vector, tfidf

def main(query, topn):
    with open('../Data/episodes.json', 'r') as f:
        eps = json.loads(f.read())['episodes']
    with open('../Data/got-new.json', 'r') as f_data:
        data = json.loads(f_data.read())
    
    vec, tfidf = getModel(data)

    from sklearn.metrics.pairwise import linear_kernel
    new_doc = [query]
    response = vec.transform(clean_text(new_doc))
    cosine_simi = linear_kernel(response, tfidf).flatten()
    related_docs_indices = cosine_simi.argsort()[:-73:-1]
    related_docs_indices = [idx for idx in related_docs_indices if cosine_simi[idx] >= 0.035]
    related_docs_indices = related_docs_indices[:topn]
    # related_docs_indices = [idx for idx in related_docs_indices if cosine_simi[idx] >= 0.035]
    for i, idx in enumerate(related_docs_indices):
        # print('{}. {}'.format(i+1, data[str(idx)]['id']))
        print('{}. {}-<{}>: {}\n{}\n'.format(i+1, data[str(idx)]['id'], eps[idx]['episodeTitle'], cosine_simi[idx], eps[idx]['episodeDescription']))

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
