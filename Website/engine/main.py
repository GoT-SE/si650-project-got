import sys
from utils import GetData, GetEps, GetModel, GetScriptDataByLines
from utils import GetScriptSet, GetEpisodeSet

def main(query="you know nothing", cmd="script"):
    query = sys.argv[1]
    cmd = sys.argv[2]
    buffer = ""

    data = GetData()
    if cmd == "scene": # search for scene
        eps = GetEps()
        vec, tfidf = GetModel(data, eps)
        sceneSet = GetEpisodeSet(data, eps, vec, tfidf, query)
        for i, (x, y, z) in enumerate(sceneSet):
            buffer += "{}. {}-<{}>:\r{}\r\r".format(i+1, x, y, z)
    elif cmd == "script": # search for script
        docs = GetScriptDataByLines()
        scriptSet = GetScriptSet(docs, data, query)
        for i, (x, y, z) in enumerate(scriptSet):
            buffer += "{}. {}-<{}>:\r{}\r\r".format(i+1, x, y, z)
    print(buffer)
    sys.stdout.flush()
    # return docs

if __name__ == '__main__':
    main()
    


