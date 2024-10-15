import json
import os
import sys

sys.path.append(os.getcwd())
from utils.dictionary import COCADictionary, LongmanDictionary


coca = LongmanDictionary('assets/Dictionaries/Longman')

queryWord = 'sophisticated'
extracted_data = coca.search(queryWord)



print(json.dumps(extracted_data, indent=4, ensure_ascii=False))