from utils import load_knowledge_from_db

import sys


if __name__ == "__main__":
    arguments = sys.argv

    ont = None
    lex = None
    out = "build/knowledge.om"

    for arg in arguments:
        if arg.startswith("lex="):
            lex = arg.replace("lex=", "")
        if arg.startswith("ont="):
            ont = arg.replace("ont=", "")
        if arg.startswith("out="):
            out = arg.replace("out=", "")

    if ont is None or lex is None:
        print("Correct usage: builder.py lex=lexicon-version-here ont=ontology-version-here out=build/knowledge.om")
        print("out parameter is optional, defaults to build/knowledge.om")
        exit()

    print("Loading ontology from %s" % ont)
    print("Loading lexicon from %s" % lex)
    print("")

    load_knowledge_from_db(ont, lex, save_to=out)

    print("")
    print("Output to %s" % out)