import json
import nltk
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz, process

def init():
    global stopwords
    # nltk.download('stopwords')
    stopwords = stopwords.words('english')

# extracr a name from a sentence
def extractNames(sentence):
    tagged_sentences = nltk.pos_tag(nltk.word_tokenize(sentence))
    
    names = []
    for chunk in nltk.ne_chunk(tagged_sentence):
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() in ['GPE', 'PERSON']:
                names.append(' '.join([c[0] for c in chunk]))
    return names

# take `text`
# remove punctuation and lower the letters
def cleanText(text):
    global stopwords
    import re
    text = text.lower()
    text = re.sub("[^A-Za-z0-9\n]", " ", text)
    text = re.sub("\n", " ", text)
    text = ' '.join([i for i in text.split() if i not in stopwords])
    return text

# take `query`
# replace the nicknames/first name with standard name
def synSubstitution(query):
    with open('../syn/wordcount-synonyms.json', 'r') as f:
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
def queryPreprocess(query):
    query = synSubstitution(query) # return standard person name
    query = cleanText(query) # remove punctuation and lower the letters
    return query

# take 'query' and return an episode set
# 'ratio' determines the weight of episode keywords extracted from summary
# sample return value: ['s01e01', 's01e02']
def getEpisodeSet(query, ratio = 0.5):
    return []

# take an episode set like ['s01e01']
# search the episode json file for best match
# sample return value:
# [{"s01e01": [scene1, scene2]}]
def getSceneSet(episodeSet, query):
    return []

# take 'query' to find best matches
# return `top_n` lines
# sample return value: [('s01e01', 'Winter is Coming', '...')]
def getScriptSet(query, top_n = 8):
    with open('../got/got.dat', 'r') as f:
        docs = f.read()
        docs = docs.split('\n')
    
    # case insensitive
    bests = process.extract(query, docs, scorer=fuzz.partial_ratio, limit = top_n)
    res = []
    for (line, score) in bests:
        x = line.split('\t')
        res.append((x[0].strip(), x[1].strip(), x[2].strip()))
    return res

def main():
    init()
    query = "who's dead will never die" # get the input
    cmd = "script"
    if cmd == "scene": # search for scene
        query = queryPreprocess(query)
        episodeSet = getEpisodeSet(query) # consider: 1. episode keywords 2. episode description 
        sceneSet = getSceneSet(episodeSet, query) # search the scenes in the given episodes for particular scenes
    elif cmd == "script": # search for script
        scriptSet = getScriptSet(query) # approximate match
        for i, (x, y, z) in enumerate(scriptSet):
            print("{}. {}-{}: {}".format(i+1, x, y, z))
    else:
        pass

if __name__ == '__main__':
    main()
