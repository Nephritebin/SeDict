import json
import os
import sys

sys.path.append(os.getcwd())
from utils.dictionary import *
from utils.helper import *


# longman = LongmanDictionary('assets/Dictionaries/Longman')
# vocabulary = VocabularyDictionary('assets/Dictionaries/Vocabulary')

# queryWord = 'sophisticated'
# extracted_data = longman.search(queryWord)
# print(json.dumps(extracted_data, indent=4, ensure_ascii=False))

sentences = read_paragraphs('assets/Materials/sentences.txt')
se = sentences[0]
# se =  "The striped Bats are hanging on their feet for Best Performance."
print(read_sentences(se))
