import json
import os
import sys
from tqdm import tqdm


sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *
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
# vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')
oxford = OxfordDictionary('assets/Dictionaries/Oxford')
# dict_list = []
dict_list = [oxford]

current_words= []
paragraphs = read_essay(input_file)
for paragraph in tqdm(paragraphs[:4]):
    words = list(dict.fromkeys(read_paragraph(paragraph)))
    if len(words) == 0:
        continue
    words = [i for i in words if word_filter(i, coca, current_words)]
    current_words = list(dict.fromkeys(current_words + words))
    results = []
    for i in words:
        result_dict = {'word': i, 'result': [dict.search(i) for dict in dict_list]}
    #     results.append(result_dict)
    # write_paragraph_to_latex(paragraph, results, output_file, dict_list)

