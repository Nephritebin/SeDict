import json
import os
import sys

sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *


longman = LongmanDictionary('assets/Dictionaries/Longman')
# vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')
# coca = COCADictionary('assets/Dictionaries/COCA')

# queryWord = 'sophisticated'
# extracted_data = longman.search(queryWord)
# print(json.dumps(extracted_data, indent=4, ensure_ascii=False))

sentences = read_paragraphs('assets/Materials/sentences.txt')
se = sentences[2]
words = read_sentences(se)

# for i in words:
#     print(i)
#     extracted_data = longman.search(i)
#     if extracted_data != -1:
#         print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
extracted_data = longman.search("starting")
#TODO: Fix this problem

