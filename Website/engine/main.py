import sys

def main(query="you know nothing", cmd="script"):
    query = sys.argv[1]
    cmd = sys.argv[2]
    scriptSet = [
        ("s03e21", "Valar Dohaeris", "Jon is tested by the wildling king; Tyrion asks for his reward; Daenerys sails into Slaver's Bay."), 
        ("s03e23", "Walk of Punishment", "Dany hears the price; Jaime strikes a deal with his captors.")
    ]
    sceneSet = ["s03e21", "s03e23", "s06e9"]
    buffer = ""
    if cmd == "scene": # search for scene
        for i, x in enumerate(sceneSet):
            # docs.append("{}. {}-{}: {}".format(i+1, x, y, z))
            # print("{}. {}".format(i+1, x))
            buffer += "{}. {}\r".format(i+1, x)
    elif cmd == "script": # search for script
        # docs = []
        for i, (x, y, z) in enumerate(scriptSet):
            # docs.append("{}. {}-{}: {}".format(i+1, x, y, z))
            # print("{}. {}-{}: {}".format(i+1, x, y, z))
            buffer += "{}. {}-{}: {}\r".format(i+1, x, y, z)
    print(buffer)
    sys.stdout.flush()
    # return docs

if __name__ == '__main__':
    main()
    


