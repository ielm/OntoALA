"""
You must use python 3.10 for this to work! COCA.reader() uses the new match/case syntax
"""

import pandas as pd
from pandas import DataFrame
from enum import Enum

import time, sys

import re
import os
import csv

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

class CMODE(Enum):
    LINEAR = "LINEAR"
    WLPOS = "WLPOS"
    DB = "DB"


# class COCAText:
#     def __init__(
#         self,
#         data_dir: str = "/Users/ivan/Dropbox/rpi/leia/code/OntoALA/corpus/",
#         mode: CMODE = CMODE.LINEAR,
#     ):
#         self.data_dir = data_dir
#         self.mode = mode
#         self.data = self.reader()

#     def reader(self):
#         def _process_line(line: str):
#             line_no = re.match(r"##[\d]+", line).group(0)
#             unprocessed_text = re.split(r"##[\d]+", line)[1]
#             return [line_no, unprocessed_text]

#         def _process_wlpos():
#             pass

#         match self.mode:
#             case CMODE.LINEAR:
#                 linear_df = pd.DataFrame()  # output dataframe
#                 file_no = 0  # index for updating progress bar
#                 for subdir, dirs, files in os.walk(f"{self.data_dir}/text/"):
#                     dir_len = len(files)
#                     for filename in [f for f in files if ".txt" in f]:
#                         update_progress(file_no / dir_len, "Linear Mode", filename)
#                         file_no += 1
#                         with open(f"{subdir}/{filename}", "rt") as fin:
#                             for line in fin:
#                                 if line != "\n":
#                                     newline = _process_line(line)
#                                     linear_df.append(newline)
#                 return linear_df

#             case CMODE.WLPOS:
#                 pass

#             case CMODE.DB:
#                 pass


class COCA:
    def __init__(
        self,
        data_dir: str = "/Users/ivan/Dropbox/rpi/leia/code/OntoALA/corpus/",
        pkl: bool = False,
        pkl_dir: str = "/Users/ivan/Dropbox/rpi/leia/code/OntoALA/pkl/",
    ):
        self.data_dir = data_dir  # corpus location
        self.pkl_dir = pkl_dir  # pickle location
        self.pkl = pkl  # load from pickled data
        self.mode = CMODE.DB  # the coca mode
        self.data = None  # the coca dataframe
        self.lexicon = None  # the lexicon dataframe
        self.sources = None  # the sources dataframe
        self.subgenre = None  # the subgenre codes dataframe

        self._reader()  # load the data from files or pickle

    def _reader(self):

        # if self.pkl: 
        #     for subdir, dirs, files in os.walk(f"{self.pkl_dir}"):
        #         # if len(dirs) == 0:
        #         #     print("There are no pickle files. Resorting to raw data loading...")
        #         #     continue

        #         # else:
        #         print(f"SubDir: {subdir}")
        #         print(f"Dirs: {dirs}")
        #         print(f"Files: {files}")

        def _manual_parse(filename: str, dstruct: dict):
            with open(filename, 'rt', encoding="ISO-8859-1") as fin:
                source_dict = dstruct
                    for line in fin.readlines():
                        values = str(line.strip()).split('\t')
                        entry = dict(zip(source_dict.keys(), values))
                        for k in source_dict.keys():
                            source_dict[k].append(entry[k])
                    return pd.DataFrame(source_dict)

        datafiles = []
        file_no = 0
        for subdir, dirs, files in os.walk(f"{self.data_dir}/db/csv/"):
            dir_len = len(files)
            flist = [f for f in files if ".csv" in f]
            for filename in flist:
                progress_bar(file_no / dir_len, "Build COCA DB", filename)
                if filename.startswith("db_"):
                    with open(f"{subdir}/{filename}", "rt") as fin:
                        datafiles.append(pd.read_csv(fin))
                elif filename == "coca-sources.csv":
                    f = f"{self.data_dir}/coca-sources.txt"
                    s_dict = {"textID": [], "year": [], "genre": [], "subGenre": [], "source": [], "title": []}
                    self.sources = _manual_parse(f, s_dict)
                elif filename == "subgenreCodes.csv":
                    with open(f"{subdir}/subgenreCodes.csv", "rt") as fin:
                        self.subgenre = pd.read_csv(fin)
                elif filename == "lexicon.csv":
                    with open(f"{self.data_dir}/lexicon.txt", "rt", encoding="ISO-8859-1") as fin:
                        # self.lexicon = pd.read_csv(fin)
                        lex_dict = {"wordID": [], "word": [], "lemma": [], "PoS": []}
                        for line in fin.readlines():
                            values = str(line.strip()).split('\t')
                            entry = dict(zip(lex_dict.keys(), values))
                            print(values)
                            for k in lex_dict.keys():
                                lex_dict[k].append(entry[k])
                        self.lexicon = pd.DataFrame(lex_dict)
                file_no += 1
        self.data = pd.concat(datafiles)

    def from_files(data_dir: str = ""):
        pass


# progress_bar() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def progress_bar(progress: float, name: str = "Percent", filename: str = ""):
    barLength = 50  # Modify this to change the length of the progress bar
    status = "In Progress"
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "Error: progress var must be float\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = f"\r{name}: [{'=' * block + ' ' * (barLength - block)}] {progress * 100}% {filename} {status}"
    sys.stdout.write(text)
    sys.stdout.flush()


if __name__ == "__main__":
    coca = COCA()
