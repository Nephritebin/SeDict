import os, sys

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag

from utils.helper import *

# Here are some functions you can defined by yourself.

def check_whether_paragraph_is_valid(paragraph):
    words = word_tokenize(paragraph)
    pos_tags = pos_tag(words)
    words = [(word.lower(), pos) for word, pos in pos_tags if word.isalpha()]
    if len(words) > 0:
        return True
    return False

def are_all_letters_uppercase(s):
    # Filter out non-alphabetic characters, then check if remaining are all uppercase
    return all(char.isupper() for char in s if char.isalpha())

def check_whether_paragraph_is_section_title(paragraph):
    return are_all_letters_uppercase(paragraph)

def read_paragraph(sentence):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    words = [(word.lower(), pos) for word, pos in pos_tags if pos not in ('NNP', 'NNPS') and word.isalpha()]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in words]
    return lemmatized_words


# Define a function to filter the words
# You can load your own learned words list from assets
print(os.getcwd())
learned_words = load_learned_words('assets/Materials/learned_words.txt')
wired_words = load_learned_words('assets/Materials/wired_words.txt')

# Define the threshold for the words
# Noun, Verb, Adjective, Adverb, Conjunction
threshold = {'n': 5000, 'v': 3000, 'j': 3000, 'r': 3000, 'c': 1000} 


def word_filter(word, coca, current_words):
    # Define the words to be filtered manually
    if word in learned_words:
        return False
    if word in current_words:
        return False
    if word in wired_words:
        return False
    
    # Not be able to find the word in the COCA dataset
    extracted_data = coca.search(word)
    if extracted_data == -1:
        return True
    
    # Infinitive marker, determiner, preposition, article
    if extracted_data['part_of_speech'] in ('i', 'd', 'p', 'a', 't', 'x', 'm', 'e', 'u'):
        return False
    
    # If the rank of the words is greater than threshold, return True
    # The threshold is set based on the part of speech of the word
    elif extracted_data['part_of_speech'] in ('n', 'v', 'j', 'r', 'c'):
        if extracted_data['rank'] > threshold[extracted_data['part_of_speech']]:
            return True
    else:
        raise ValueError(f"Invalid part of speech: {extracted_data['part_of_speech']}")
    return False
