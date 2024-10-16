import json
import os
import sys
from tqdm import tqdm

sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *
from utils.word import *


sentences = read_paragraphs('assets/Materials/sentences.txt')
output_file = 'assets/Contents/reading.tex'
try:
    os.remove(output_file)
except FileNotFoundError:
    pass

# Load coca dataset and dictionaries
coca = COCADictionary('assets/Dictionaries/COCA')
longman = LongmanDictionary('assets/Dictionaries/Longman')
vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')
dict_list = [longman, vocabulary]

for sentence in tqdm(sentences):
    words = list(set(read_sentence(sentence)))
    words = [i for i in words if word_filter(i, coca)]
    results = []
    for i in words:
        result_dict = {'word': i, 'result': [dict.search(i) for dict in dict_list]}
        results.append(result_dict)
    write_sentence_to_latex(sentence, results, output_file)
