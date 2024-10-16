import json
import os
import sys

sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *
from utils.word import *


coca = COCADictionary('assets/Dictionaries/COCA')
sentences = read_paragraphs('assets/Materials/sentences.txt')

longman = LongmanDictionary('assets/Dictionaries/Longman')
vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')
dict_list = [longman, vocabulary]

for sentence in sentences[:1]:
    print(sentence)
    words = list(set(read_sentence(sentence)))
    words = [i for i in words if word_filter(i, coca)]

    for i in words:
        print(i)
        result_dict = {'word': i}
        result_dict['result'] = [dict.search(i) for dict in dict_list]
        format_dictionary(result_dict, dict_list)
