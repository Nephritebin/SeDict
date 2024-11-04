import json
import os
import sys
from tqdm import tqdm


sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *
from utils.personal import *

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
# oxford = OxfordDictionary('assets/Dictionaries/Oxford')
# dict_list = []
dict_list = [vocabulary, longman]

current_words= []
paragraphs = read_essay(input_file)
for paragraph in tqdm(paragraphs):
    if not check_whether_paragraph_is_valid(paragraph):
        continue
    words = list(dict.fromkeys(read_paragraph(paragraph)))
    words = [i for i in words if word_filter(i, coca, current_words)]
    results = []
    for i in words:
        result_dict = {'word': i, 'result': [dict.search(i) for dict in dict_list]}
        results.append(result_dict)
        for j in result_dict['result']:
            if j != -1:
                current_words.append(i)
                break
    write_paragraph_to_latex(paragraph, results, output_file, dict_list)
write_word_appendix(current_words, output_file)

