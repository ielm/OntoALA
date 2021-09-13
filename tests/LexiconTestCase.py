from collections import OrderedDict
from knowledge.lexicon import Lexicon, MeaningProcedure, SemStruc, Sense, SynStruc
from ontomem.frame import Frame
from unittest import TestCase


class LexiconTestCase(TestCase):
    def test_sense(self):
        lexword = Frame("LEX-WORD")

        sense = Frame("TEST.V.1")
        sense.add_parent(lexword)
        sense.add_to_space("LEX")
        sense["WORD"] = "TEST"
        sense["CAT"] = "V"
        sense["SENSE"] = "TEST-V1"
        sense["SYN-STRUC"] = OrderedDict([("test", "a")])
        sense["SEM-STRUC"] = {"test": "b"}
        sense["MEANING-PROCEDURES"] = [
            ["TEST-MP1", "PARAM1", ["VALUE", "PARAM2"]],
            ["TEST-MP2"],
        ]

        lexicon = Lexicon()
        self.assertNotIn("TEST-V1", lexicon.sense_cache)

        sense = lexicon.sense("TEST-V1")
        self.assertEqual("TEST-V1", sense.id)
        self.assertEqual(SynStruc(OrderedDict([("test", "a")])), sense.synstruc)
        self.assertEqual(SemStruc({"test": "b"}), sense.semstruc)
        self.assertEqual(
            [
                MeaningProcedure(["TEST-MP1", "PARAM1", ["VALUE", "PARAM2"]]),
                MeaningProcedure(["TEST-MP2"]),
            ],
            sense.meaning_procedures,
        )

        self.assertIn("TEST-V1", lexicon.sense_cache)
        self.assertEqual(sense, lexicon.sense("TEST-V1"))

        lexicon = Lexicon()
        self.assertNotIn("TEST-V1", lexicon.sense_cache)

    def test_null_sense(self):
        lexicon = Lexicon()
        self.assertEqual(Lexicon.null_sense(), lexicon.sense("ERROR"))
        self.assertEqual(Lexicon.null_sense(), lexicon.sense("PERSON-NAME"))


class SenseTestCase(TestCase):
    def test_parse_lisp(self):
        lisp = [
            "KICK--IMPERATIVE-V1",
            ["CAT", "V"],
            [
                "SYN-STRUC",
                [
                    ["ROOT", "$VAR0"],
                    ["CAT", "V"],
                    ["DIRECTOBJECT", [["ROOT", "$VAR2"], ["CAT", "N"]]],
                ],
            ],
            [
                "SEM-STRUC",
                ["KICK", ["THEME", ["VALUE", "^$VAR2"]], ["AGENT", "*HEARER*"]],
                [
                    "REQUEST-ACTION",
                    ["AGENT", "*SPEAKER*"],
                    ["THEME", ["VALUE", "^$VAR0"]],
                ],
            ],
            [
                "MEANING-PROCEDURES",
                ["FIX-CASE-ROLE", ["VALUE", "^$VAR1"], ["VALUE", "^$VAR2"]],
            ],
        ]

        sense = Sense.parse_lisp(lisp)
        self.assertEqual("KICK--IMPERATIVE-V1", sense.id)
        self.assertEqual("V", sense.pos)
        self.assertEqual(
            SynStruc(
                OrderedDict(
                    [
                        ("ROOT", "$VAR0"),
                        ("CAT", "V"),
                        (
                            "DIRECTOBJECT",
                            OrderedDict([("ROOT", "$VAR2"), ("CAT", "N")]),
                        ),
                    ]
                )
            ),
            sense.synstruc,
        )
        self.assertEqual(
            SemStruc(
                {
                    "KICK": {
                        "THEME": {
                            "VALUE": "^$VAR2",
                        },
                        "AGENT": "*HEARER*",
                    },
                    "REQUEST-ACTION": {
                        "AGENT": "*SPEAKER*",
                        "THEME": {"VALUE": "^$VAR0"},
                    },
                }
            ),
            sense.semstruc,
        )
        self.assertEqual(
            [
                MeaningProcedure(
                    ["FIX-CASE-ROLE", ["VALUE", "^$VAR1"], ["VALUE", "^$VAR2"]]
                )
            ],
            sense.meaning_procedures,
        )

    def test_parse_lisp_missing_fields(self):
        # Lex senses that come directly from the syntax output (generated) may not have a
        # synstruc or meaning procedures field attached.

        lisp = [
            "KICK--IMPERATIVE-V1",
            ["CAT", "V"],
            [
                "SEM-STRUC",
                ["KICK", ["THEME", ["VALUE", "^$VAR2"]], ["AGENT", "*HEARER*"]],
                [
                    "REQUEST-ACTION",
                    ["AGENT", "*SPEAKER*"],
                    ["THEME", ["VALUE", "^$VAR0"]],
                ],
            ],
        ]

        sense = Sense.parse_lisp(lisp)
        self.assertEqual("KICK--IMPERATIVE-V1", sense.id)
        self.assertEqual("V", sense.pos)
        self.assertEqual(SynStruc(OrderedDict()), sense.synstruc)
        self.assertEqual(
            SemStruc(
                {
                    "KICK": {
                        "THEME": {
                            "VALUE": "^$VAR2",
                        },
                        "AGENT": "*HEARER*",
                    },
                    "REQUEST-ACTION": {
                        "AGENT": "*SPEAKER*",
                        "THEME": {"VALUE": "^$VAR0"},
                    },
                }
            ),
            sense.semstruc,
        )
        self.assertEqual([], sense.meaning_procedures)

    def test_from_frame(self):
        lexword = Frame("LEX-WORD")

        sense = Frame("KICK.IMPERATIVE-V.1")
        sense.add_parent(lexword)
        sense.add_to_space("LEX")
        sense["WORD"] = "KICK"
        sense["CAT"] = "V"
        sense["SENSE"] = "KICK--IMPERATIVE-V1"
        sense["SYN-STRUC"] = OrderedDict(
            [
                ("ROOT", "$VAR0"),
                ("CAT", "V"),
                ("DIRECTOBJECT", OrderedDict([("ROOT", "$VAR2"), ("CAT", "N")])),
            ]
        )
        sense["SEM-STRUC"] = {
            "KICK": {
                "THEME": {
                    "VALUE": "^$VAR2",
                },
                "AGENT": "*HEARER*",
            },
            "REQUEST-ACTION": {"AGENT": "*SPEAKER*", "THEME": {"VALUE": "^$VAR0"}},
        }
        sense["MEANING-PROCEDURES"] = []

        sense = Sense.from_frame(sense)
        self.assertEqual("KICK--IMPERATIVE-V1", sense.id)
        self.assertEqual("V", sense.pos)
        self.assertEqual(
            SynStruc(
                OrderedDict(
                    [
                        ("ROOT", "$VAR0"),
                        ("CAT", "V"),
                        (
                            "DIRECTOBJECT",
                            OrderedDict([("ROOT", "$VAR2"), ("CAT", "N")]),
                        ),
                    ]
                )
            ),
            sense.synstruc,
        )
        self.assertEqual(
            SemStruc(
                {
                    "KICK": {
                        "THEME": {
                            "VALUE": "^$VAR2",
                        },
                        "AGENT": "*HEARER*",
                    },
                    "REQUEST-ACTION": {
                        "AGENT": "*SPEAKER*",
                        "THEME": {"VALUE": "^$VAR0"},
                    },
                }
            ),
            sense.semstruc,
        )

    def test_duplicate(self):
        lexword = Frame("LEX-WORD")

        sense = Frame("FIX-V.2")
        sense.add_parent(lexword)
        sense.add_to_space("LEX")
        sense["WORD"] = "FIX"
        sense["CAT"] = "V"
        sense["SENSE"] = "FIX-V2"
        sense["SYN-STRUC"] = OrderedDict(
            [
                ("SUBJECT", OrderedDict([("ROOT", "$VAR1"), ("CAT", "NP")])),
                ("ROOT", "$VAR0"),
                ("CAT", "V"),
                ("DIRECTOBJECT", OrderedDict([("ROOT", "$VAR2"), ("CAT", "P")])),
                ("PP", OrderedDict([("ROOT-WORD", "TO"),("ROOT", "$VAR4"), ("CAT", "PREP"), ("OBJ", OrderedDict([("ROOT", "$VAR3"), ("CAT", "N")]))]))
            ]
        )
        sense["SEM-STRUC"] = {
            "FASTEN": {
                "AGENT": {"VALUE": "^$VAR1"},
                "THEME": {"VALUE": "^$VAR2"},
                "DESTINATION": {"VALUE": "^$VAR3"}},
            "^$VAR4": {"NULL-SEM": "+"}
        }
        sense["MEANING-PROCEDURES"] = []

        sense["SYNONYMS"] = ["ATTACH",
                             "FASTEN",
                             "SECURE"],
        sense["HYPONYMS"] =  "NIL",

        sense = Sense.from_frame(sense)

        # print(sense.synonyms)
        duplicate_sense = sense.duplicate(sense.synonyms[0])




class SemStrucTestCase(TestCase):
    def test_init_with_empty_string(self):
        # We test for this as there are entries in the lexicon like this
        semstruc = SemStruc("")
        self.assertEqual({}, semstruc.data)

    def test_init_with_basic_concept(self):
        semstruc = SemStruc("HUMAN")
        self.assertEqual({"HUMAN": {}}, semstruc.data)

    def test_init_with_listed_concept(self):
        # In the case of some REFSEMs, they represent a basic concept inside of a list (why??).
        # For example, THERE-ADV1 (REFSEM1).
        # TODO: can we rewrite these REFSEMs?  Or at least confirm that this is only a REFSEM thing and only exactly one option is present?
        semstruc = SemStruc(["HUMAN"])
        self.assertEqual({"HUMAN": {}}, semstruc.data)

    def test_elements(self):
        self.assertEqual([], SemStruc({}).elements())

        semstruc = SemStruc(
            {
                "HUMAN": {"head": "test"},
                "REFSEM1": {"TEST": {"rs1": "test"}},
                "DOG": {"sub": "test1"},
                "REFSEM2": {"TEST": {"rs2": "test"}},
                "CAT": {"sub": "test2"},
                "^$VAR1": {"var": "test1"},
                "^$VAR2": {"var": "test2"},
                "^$VAR4": {"var": "test4"},
                "REFSEM4": {"TEST": {"rs4": "test"}},
                "BIRD": {"sub": "test3"},
            }
        )

        self.assertEqual(
            [
                SemStruc.Head("HUMAN", {"head": "test"}),
                SemStruc.RefSem(1, SemStruc({"TEST": {"rs1": "test"}})),
                SemStruc.Sub(1, "DOG", {"sub": "test1"}),
                SemStruc.RefSem(2, SemStruc({"TEST": {"rs2": "test"}})),
                SemStruc.Sub(2, "CAT", {"sub": "test2"}),
                SemStruc.Variable(1, {"var": "test1"}),
                SemStruc.Variable(2, {"var": "test2"}),
                SemStruc.Variable(4, {"var": "test4"}),
                SemStruc.RefSem(4, SemStruc({"TEST": {"rs4": "test"}})),
                SemStruc.Sub(3, "BIRD", {"sub": "test3"}),
            ],
            semstruc.elements(),
        )

    def test_head(self):
        # Trivial example
        semstruc = SemStruc({"HUMAN": {}})

        self.assertEqual(SemStruc.Head("HUMAN", {}), semstruc.head())

        # Ignore refsems
        semstruc = SemStruc(
            {
                "REFSEM1": {},
                "REFSEM2": {},
                "HUMAN": {},
                "REFSEM3": {},
            }
        )

        self.assertEqual(SemStruc.Head("HUMAN", {}), semstruc.head())

        # Ignore variables
        semstruc = SemStruc(
            {
                "^$VAR0": {},
                "^$VAR1": {},
                "HUMAN": {},
                "^$VAR2": {},
            }
        )

        self.assertEqual(SemStruc.Head("HUMAN", {}), semstruc.head())

        # Return none if no head is found
        semstruc = SemStruc(
            {
                "^$VAR0": {},
                "REFSEM1": {},
            }
        )

        self.assertIsNone(semstruc.head())

        # Choose the first if more than one are found
        semstruc = SemStruc(
            {
                "HUMAN": {},
                "DOG": {},
            }
        )

        self.assertEqual(SemStruc.Head("HUMAN", {}), semstruc.head())

    def test_subs(self):
        # No results if none are declared
        semstruc = SemStruc({})

        self.assertEqual([], semstruc.subs())

        # No results if one is declared (it is the head)
        semstruc = SemStruc({"HUMAN": {}})

        self.assertEqual([], semstruc.subs())

        # Refsems and variables are ignored
        semstruc = SemStruc(
            {
                "HUMAN": {},
                "REFSEM1": {},
                "REFSEM2": {},
                "^$VAR0": {},
                "^$VAR1": {},
            }
        )

        self.assertEqual([], semstruc.subs())

        # All remaining non-refsem and non-variable entries are returned
        semstruc = SemStruc(
            {
                "HUMAN": {},
                "REFSEM1": {},
                "DOG": {},
                "^$VAR0": {},
                "CAT": {},
            }
        )

        self.assertEqual(
            [SemStruc.Sub(1, "DOG", {}), SemStruc.Sub(2, "CAT", {})], semstruc.subs()
        )

    def test_refsems(self):

        semstruc = SemStruc(
            {
                "REFSEM1": {"X": {"a": 1}},
                "REFSEM2": {"Y": {"a": 2}},
                "HUMAN": {},
                "REFSEM3": {"Z": {"a": 3}},
            }
        )

        refsems = semstruc.refsems()

        self.assertEqual(3, len(refsems))

        self.assertEqual(1, refsems[0].index)
        self.assertEqual(SemStruc({"X": {"a": 1}}), refsems[0].semstruc)

        self.assertEqual(2, refsems[1].index)
        self.assertEqual(SemStruc({"Y": {"a": 2}}), refsems[1].semstruc)

        self.assertEqual(3, refsems[2].index)
        self.assertEqual(SemStruc({"Z": {"a": 3}}), refsems[2].semstruc)

    def test_variables(self):

        semstruc = SemStruc(
            {
                "^$VAR1": {"X": 1},
                "^$VAR2": {"Y": 2},
                "HUMAN": {},
                "^$VAR4": {"Z": 3},
            }
        )

        variables = semstruc.variables()

        self.assertEqual(3, len(variables))

        self.assertEqual(1, variables[0].index)
        self.assertEqual({"X": 1}, variables[0].contents)

        self.assertEqual(2, variables[1].index)
        self.assertEqual({"Y": 2}, variables[1].contents)

        self.assertEqual(4, variables[2].index)
        self.assertEqual({"Z": 3}, variables[2].contents)


class MeaningProcedureTestCase(TestCase):
    def test_init(self):
        mp = MeaningProcedure(["MP-NAME", "PARAMETER1", ["VALUE", "PARAMETER2"]])

        self.assertEqual("MP-NAME", mp.name())
        self.assertEqual(["PARAMETER1", ["VALUE", "PARAMETER2"]], mp.parameters())

    def test_init_empty_mp(self):
        mp = MeaningProcedure([])

        self.assertEqual("UNKNOWN-MP", mp.name())
        self.assertEqual([], mp.parameters())
