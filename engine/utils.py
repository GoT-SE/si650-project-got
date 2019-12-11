import json
from fuzzywuzzy import fuzz, process
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
import numpy as np
import sys
import re
import os
import pickle

# return docs
def GetScriptDataByLines():
    # with open('../../Data/got-new-by-line.dat', 'r') as f:
    with open('Data/got-new-by-line.dat', 'r') as f:
        docs = f.read().split('\n')
    return docs

# return: [(s01e01, 'blablabla')]
def GetScriptSet(docs, data, query, top_n=8):
    # case insensitive
    bests = process.extract(query, docs, scorer=fuzz.partial_ratio, limit = top_n)
    res = []
    for (line, score) in bests:
        x = line.split('\t')
        res.append((data[x[0]]['id'], data[x[0]]['name'], x[1].strip()))
    return res

# return vec, tfidf
def GetModel(data, eps):
    # if os.path.exists('../../Src/trained/vec.pkl') and os.path.exists('../../Src/trained/tfidf.pkl'):
        # tfidf = pickle.load(open("../../Src/trained/tfidf.pkl", "rb"))
        # vec = pickle.load(open("../../Src/trained/vec.pkl", "rb"))
    if os.path.exists('Src/trained/vec.pkl') and os.path.exists('Src/trained/tfidf.pkl'):
        tfidf = pickle.load(open("Src/trained/tfidf.pkl", "rb"))
        vec = pickle.load(open("Src/trained/vec.pkl", "rb"))
        return vec, tfidf
    
    print('rebuild model...')
    def load_episode_data(data):
        if data == None: return []
        sents = clean_text(sent_tokenize(data))
        return sents
    
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
    
    vec = TfidfVectorizer(sublinear_tf=True, max_features=10000, max_df=0.85, ngram_range=(1,2), analyzer='word')
    tfidf = vec.fit_transform(docs)

    # pickle.dump(tfidf, open("../../Src/trained/tfidf.pkl", "wb"))
    # pickle.dump(vec, open("../../Src/trained/vec.pkl", "wb"))
    pickle.dump(tfidf, open("Src/trained/tfidf.pkl", "wb"))
    pickle.dump(vec, open("Src/trained/vec.pkl", "wb"))
    return vec, tfidf

# return: data
def GetData():
    # with open('../../Data/got-new.json', 'r') as f_data:
    with open('Data/got-new.json', 'r') as f_data:
        data = json.loads(f_data.read())
    return data

# return eps
def GetEps():
    # with open('../../Data/episodes.json', 'r') as f:
    with open('Data/episodes.json', 'r') as f:
        eps = json.loads(f.read())['episodes']
    return eps

# return: [('s01e01', 'Winter is Coming', 'description...')]
def GetEpisodeSet(data, eps, vec, tfidf, query, topn=10):
    from sklearn.metrics.pairwise import linear_kernel
    res = []
    new_doc = [query]
    response = vec.transform(clean_text(new_doc))
    cosine_simi = linear_kernel(response, tfidf).flatten()
    related_docs_indices = cosine_simi.argsort()[:-73:-1]
    related_docs_indices = [idx for idx in related_docs_indices if cosine_simi[idx] >= 0.035]
    related_docs_indices = related_docs_indices[:topn]
    for idx in related_docs_indices:
        res.append((data[str(idx)]['id'], eps[idx]['episodeTitle'], eps[idx]['episodeDescription']))
    
    return res

def set_stopwords():
    stop = set(stopwords.words("english"))
    # for line in open("../../Data/lemur-stopwords.txt"):
    for line in open("Data/lemur-stopwords.txt"):
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
        text = re.sub("scene shifts", " ", text)
        text = re.sub("scene", " ", text)
        text = re.sub("cut to", " ", text)

        text = re.sub("[^A-Za-z\n]", " ", text)
        text = re.sub("\n", " ", text)

        text = ' '.join([ps.stem(t) for t in word_tokenize(text) if (t not in stopwords) and (len(t) > 1)])
        if text != '':
            res.append(text)
    return res

# extracr a name from a sentence
def extractNames(sentence):
    tagged_sentences = nltk.pos_tag(nltk.word_tokenize(sentence))
    
    names = []
    for chunk in nltk.ne_chunk(tagged_sentences):
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() in ['GPE']:
                names.append(' '.join([c[0] for c in chunk]))
    return names

# take `query`
# replace the nicknames/first name with standard name
def synSubstitution(query):
    with open('Data/synonyms.json', 'r') as f:
        syns = json.load(f)['synonyms']
    
    syns = [json.dumps(syn) for syn in syns]
    names = extractNames(query)
    for name in names:
        best = process.extract(name, syns, scorer=fuzz.token_set_ratio, limit=1)[0]
        if best[1] > 80:
            query += ' ' + json.loads(best[0])['accepted']
    
    return query

# take `query`
# first clean text
# replace the nicknames/first name with standard name
def QueryPreprocess(query):
    query = synSubstitution(query) # return standard person name
    query = clean_text([query])[0] # remove punctuation and lower the letters
    return query
