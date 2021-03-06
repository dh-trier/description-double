"""
Python script to filter specific descriptions from the 
"La Description double" corpus of descriptions, 
based on the set of keywords present. 
"""


# =======================
# Imports
# =======================

import pandas as pd


# =======================
# Files and folders
# =======================

datafile = "Description-Double_Corpus-of-Descriptions_numbers.tsv"



# =======================
# Functions
# =======================

def open_file(datafile): 
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep="\t")
        #print(data.head())
        #columns = data.columns.tolist()
        #print(columns)
        return data


def select_data(data):
    #selected = data[(data.remPHYMORdis == 1)]
    #selected = data[(data.remPHYMORcon == 1)]
    #selected = data[(data.metaPORTRAIT == 1)]
    #selected = data[(data.metaPHYSIONOMIE == 1)]
    selected = data[(data.objPPHYS == 1) | (data.objPPHYSMOR == 1)]
    return selected


def save_data(selected): 
    selected = selected[["author", "title", "pages", "letter", "text"]]
    print(selected.head())
    print(selected.shape)
    with open("DD_selected_objPPHYS-OR-objPPHYSMOR.txt", "w", encoding="utf8") as outfile: 
        selected.to_csv(outfile, sep="\t")



# =======================
# Main
# =======================

def main(datafile):
    data = open_file(datafile)
    selected = select_data(data)
    save_data(selected)

main(datafile)
