import sys
from utils import GetData, GetEps, GetModel, GetScriptDataByLines
from utils import GetScriptSet, GetEpisodeSet, QueryPreprocess

def main(query="you know nothing", cmd="script", top_n=5):
    if len(sys.argv) > 2:
        query = sys.argv[1]
        cmd = sys.argv[2]
        top_n = int(sys.argv[3])
    buffer = ""

    data = GetData()
    if cmd == "scene": # search for scene
        query = QueryPreprocess(query)
        eps = GetEps()
        vec, tfidf = GetModel(data, eps)
        sceneSet = GetEpisodeSet(data, eps, vec, tfidf, query, top_n)
        for i, (x, y, z) in enumerate(sceneSet):
            buffer += "{}. {}-<{}>:\r{}\r\r".format(i+1, x, y, z)
    elif cmd == "script": # search for script
        docs = GetScriptDataByLines()
        scriptSet = GetScriptSet(docs, data, query, top_n)
        for i, (x, y, z) in enumerate(scriptSet):
            buffer += "{}. {}-<{}>:\r{}\r\r".format(i+1, x, y, z)
    print(buffer)
    # sys.stdout.flush()
    # return docs

if __name__ == '__main__':
    main()
    


