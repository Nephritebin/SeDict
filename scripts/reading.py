import json
import os
import sys
from tqdm import tqdm
from collections import OrderedDict


sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *
from utils.word import *
from utils.personal import word_filter, read_paragraph

input_file = 'assets/Materials/paper_reading.txt'
output_file = 'assets/Contents/reading.tex'
template_file = 'assets/Latex Templates/notes.tex'
try:
    os.remove(output_file)
except FileNotFoundError:
    pass

# Load coca dataset and dictionaries
coca = COCADictionary('assets/Dictionaries/COCA')
longman = LongmanDictionary('assets/Dictionaries/Longman')
vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')
dict_list = [vocabulary, longman]
# dict_list = [vocabulary]

paragraphs = read_essay(input_file)
for paragraph in tqdm(paragraphs):
    words = list(dict.fromkeys(read_paragraph(paragraph)))
    words = [i for i in words if word_filter(i, coca)]
    results = []
    for i in words:
        result_dict = {'word': i, 'result': [dict.search(i) for dict in dict_list]}
        results.append(result_dict)
    write_paragraph_to_latex(paragraph, results, output_file, dict_list)

# TODO: Use python to compile the Latex automatically