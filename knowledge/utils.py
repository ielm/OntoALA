from lex.api import LexiconAPI
from lex.management import LEXICON_ACTIVE
from ontomem.frame import Space, Frame
from ontomem.memory import MemoryManager
from ont.api import OntologyAPI
from ont.management import ONTOLOGY_ACTIVE

import json
import sys
import os
import re


def load_ontology_from_db(collection: str):

    os.environ[ONTOLOGY_ACTIVE] = collection
    ontology = Frame("ONTOLOGY")
    ontology["VERSION"] = collection

    api = OntologyAPI()

    relations = list(map(lambda r: r.upper(), api.relations(inverses=True)))
    relations.remove("INVERSE")

    for concept in api.collection.find({}):
        name = concept["name"]
        if "." in name:
            print("Skipping %s" % name)
            continue

        f = Frame(name.upper())
        for property in concept["localProperties"]:
            slot = property["slot"].upper()
            facet = property["facet"].upper()
            filler = property["filler"]
            if slot in relations:
                if "." in filler:
                    print("Skipping %s[%s][%s] = %s" % (name, slot, facet, filler))
                    continue
                filler = Frame(filler.upper())
            if slot == "INVERSE":
                filler = filler.upper()

            f[slot][facet] += filler

            if slot == "INVERSE":
                f[slot].set_inherit_local()

        for parent in concept["parents"]:
            f.add_parent(Frame(parent.upper()))

def load_lexicon_from_db(collection: str):

    lexword = Frame("LEX-WORD")

    os.environ[LEXICON_ACTIVE] = collection
    lexicon = Frame("LEXICON")
    lexicon["VERSION"] = collection

    api = LexiconAPI()

    senses = api.all_senses()
    for s in senses:
        sense_id = s["SENSE"]
        word = s["WORD"]
        cat = s["CAT"]
        index = int(re.findall("([^0-9]*)([0-9]+)", sense_id)[0][1])

        sense = Frame(f"{word}.{cat}.{index}")
        sense.add_parent(lexword)
        sense.add_to_space("LEX")
        sense["WORD"] = word
        sense["CAT"] = cat
        sense["SENSE"] = sense_id
        sense["SYN-STRUC"] = s["SYN-STRUC"]
        sense["SEM-STRUC"] = s["SEM-STRUC"]
        sense["SYNONYMS"] = s["SYNONYMS"] if "SYNONYMS" in s else None
        sense["HYPONYMS"] = s["HYPONYMS"] if "HYPONYMS" in s else None
        sense["DEF"] = s["DEF"] if "DEF" in s else None
        sense["EX"] = s["EX"] if "EX" in s else None


        meaning_procedures = []
        if "MEANING-PROCEDURES" in s and s["MEANING-PROCEDURES"] != "NIL":
            meaning_procedures = s["MEANING-PROCEDURES"]

        sense["MEANING-PROCEDURES"] = meaning_procedures

def load_local_lexicon(file: str):
    from ontogen.knowledge.local.lexicon import Lexicon as L 

    lexword = Frame("LEX-WORD")
    senses = []

    for k1, lemma in L.items():
        for k2, sense in L[k1].items():
            print(k2)
            sense["SENSE"] = k2
            sense["WORD"] = k2.split('-')[0]
            senses.append(sense)

    for s in senses:
        sense_id = s["SENSE"]
        word = s["WORD"]
        cat = s["CAT"]
        index = int(re.findall("([^0-9]*)([0-9]+)", sense_id)[0][1])

        sense = Frame(f"{word}.{cat}.{index}")
        if sense not in Space("LEX"):
            sense.add_parent(lexword)
            sense.add_to_space("LEX")
            sense["WORD"] = word
            sense["CAT"] = cat
            sense["SENSE"] = sense_id
            sense["SYN-STRUC"] = s["SYN-STRUC"]
            sense["SEM-STRUC"] = s["SEM-STRUC"]
            sense["SYNONYMS"] = s["SYNONYMS"] if "SYNONYMS" in s else None
            sense["HYPONYMS"] = s["HYPONYMS"] if "HYPONYMS" in s else None
            sense["DEF"] = s["DEF"] if "DEF" in s else None
            sense["EX"] = s["EX"] if "EX" in s else None

            meaning_procedures = []
            if "MEANING-PROCEDURES" in s and s["MEANING-PROCEDURES"] != "NIL":
                meaning_procedures = s["MEANING-PROCEDURES"]

            sense["MEANING-PROCEDURES"] = meaning_procedures

def load_knowledge_from_db(ont_collection: str, lex_collection: str, save_to: str=None):
    # Read in the ontology and lexicon into OntoMem
    load_ontology_from_db(ont_collection)
    load_lexicon_from_db(lex_collection)

    # Optionally, save to a mem file
    if save_to is not None:
        MemoryManager.save_memory(save_to)

def load_knowledge_from_db_and_file(ont_collection: str, lex_collection: str, lex_file: str, save_to: str=None):
    # Read in the ontology and lexicon into OntoMem
    load_ontology_from_db(ont_collection)
    load_lexicon_from_db(lex_collection)
    load_local_lexicon(lex_file) 

    # Optionally, save to a mem file
    if save_to is not None:
        MemoryManager.save_memory(save_to)
    


if __name__ == "__main__":
    arguments = sys.argv

    ont = None
    lex = None
    lfx = None
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

    load_knowledge_from_db_and_file(ont, lex, lfx, save_to=out)

    print("")
    print("Output to %s" % out)

