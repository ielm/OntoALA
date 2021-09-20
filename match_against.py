from knowledge.lexicon import Lexicon, Sense

from typing import Union


class MatchAgainstList:
    def __init__(self, head: Union[str, Sense]):
        if isinstance(head, str):
            head = Lexicon().sense(head)
        self.head = head

        self.synonyms = self._get_synonyms()
        self.hyponyms = self._get_hyponyms()

    def _get_synonyms(self):
        if self.head.synonyms:
            return [self.head.duplicate(s) for s in self.head.synonyms]

    def _get_hyponyms(self):
        if self.head.hyponyms:
            return [self.head.duplicate(h) for h in self.head.hyponyms]

    def to_str(self):
        s =  f"    Head:\t{self.head.id}\n"
        s += f"Synonyms:\t{self.synonyms}\n"
        s += f"Hyponyms:\t{self.hyponyms}"
            
        s += f"\n\nWARNING - SYN-STRUC/SEM-STRUC SYNONYM SEARCH NOT IMPLEMENTED"

        return s
