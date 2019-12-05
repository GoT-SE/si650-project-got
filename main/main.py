# take `query`
# remove punctuation and lower the letters
def clean_text(query):
    return query

# take `query`
# replace the nicknames/first name with standard name
def synSubstitution(query):
    return query

# take `query`
# first clean text
# replace the nicknames/first name with standard name
def queryPreprocess(query):
    query = clean_text(query) # remove punctuation and lower the letters
    query = synSubstitution(query) # return standard person name
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
    return []

def main():
    query = "" # get the input
    if cmd == "scene": # search for scene
        query = queryPreprocess(query)
        episodeSet = getEpisodeSet(query) # consider: 1. episode keywords 2. episode description 
        sceneSet = getSceneSet(episodeSet, query) # search the scenes in the given episodes for particular scenes
    elif cmd == "script": # search for script
        scriptSet = getScriptSet(query) # approximate match
    else:
        pass

if __name__ == '__main__':
    main()