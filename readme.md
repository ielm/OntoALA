# OntoALA - Automatic Language Acquisition
A trial by fire experiment to learn troponyms for lexical senses (verbs) that have a listed instrument. 

### Basic Algorithm
* Select a verb from the Lexicon that has a "basic" diathesis - instransitive, transitive, ditransitive (not a phrasal): e.g., hit-v1 
*  Create a MatchAgainstList list that contains: 
    * this head word (hit), 
    * the synonyms (if any) listed in its sense in our lexicon, 
    * the hyponyms (if any) listed in its sense, 
    * any synonyms listed elsewhere in the lexicon - i.e., senses that have the exact same syn-struc/sem-struc combination. 
* Look up the word in WordNet and create a list of the troponyms from all of its syn-sets in this part of speech; these can be single words or multiword expressions. Call this the "CandidatesForLearningList". Include in the definition and examples. A subset for 'kill' is:
    * S: (v) eliminate, annihilate, extinguish, eradicate, wipe out, decimate, carry off (kill in large numbers) "the plague wiped out an entire population."
    * S: (v) decimate (kill one in every ten, as of mutineers in Roman armies)
    * S: (v) down (kill by submerging in water), etc. 

* Using WordNet and Worknik, for each entity in CandidatesForLearningList
    * If any of the definitions includes "[word from MatchAgainstList] + (usually/typically) by/with/using _NP_"
        * E.g., 'stone' is a troponym of 'kill' and is described in WordNet as "kill by throwing stones at", and in Wordnik (among many other definitions) as "transitive verb to hurl or throw stones at, especially to kill with stones"; similarly, saber, overlie, brain, tomahawk. [ignore any difficult formulations like 'kill with or as if with...']
    * Place that candidate word/expression + the definition(s) that gave you this evidence + the associated example(s) into a list called InterestingCandidates
        * the candidate structure for 'stone' is something like 
            ```
            DEFINITIONS
                [wordnik] transitive verb To hurl or throw stones at, especially to kill with stones. 
                [wordnet] (kill by throwing stones at)
            EXAMPLES
                [wordnet] "People wanted to stone the woman who had a child out of wedlock."
            ```
    * For each InterestingCandidate, search COCA for examples that reflect the correct syntactic structure. If there are any (there are none for stone) then add them to the EXAMPLES zone of the candidate structure. 
    * For each InterestingCandidate that has at least one example (from WordNet, Wordnik or COCA), semantically analyze the example(s) and create 3 batches:
        * If the case-role fillers of the example work (e.g., "People stone woman" matches our "human kill animal" expectations, then append the example with the feature "works-semantically: True".
        * Else, if we don't know the necessary words, then append the feature "works-semantically: Unknown" [e.g., if the example had been 'People stone warlock']
        * Else (if the example doesn't work semantically) then append the feature "works-semantically: False".
    * For each entry in the batch "InterestingCandidates (works-semantically yes)", semantically analyze the 'with/by/using NP" phrase.  Again make three batches

        * Instrument-status unambiguous

        * Instrument-status ambiguous

        * Instrument-status unknown

    * All of the above are interesting, at least for this initial phase of exploration.

### Research Methodology

We need to explore this algorithm in some lightweight, even semi-automatic, way before going all-in because it might end up not working as I hope it will. We won't worry too much about output formats and things like that for a start. The question is whether our output will end up being nice a laser-focused like I hope, or whether we'll end up with WordNet-like chaos for reasons I'm not anticipating.

### A Note on Step-by-Step Outputs

Each main step detailed in the algorithm (with a specific named output) should be designed as a standalone process that writes its results out to a file or files in some reasonable format (probably JSON).

Each subsequent step should be expected to read in the output of the previous step.

This is being emphasized so that it's clear that we need to "save our state" between each step, so we can readily inspect any interim results, mock or manipulate inputs for future steps, etc.  By making some reasonable text based output, we can also store different runs of results in git or a similar versioning system.

A diagram of each step with interim data objects, and a brief description of illustration of their shape / contents would be appropriate here.