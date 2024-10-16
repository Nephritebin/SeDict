import os
import fnmatch

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag

# Make sure to download the necessary resources for NLTK
# If you haven't downloaded them yet, uncomment the following lines
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('wordnet')

def get_absolute_path(path):
    # Check if the path is absolute
    if os.path.isabs(path):
        # print(f"The path is already an absolute path: {path}")
        return path
    else:
        # Convert to absolute path
        absolute_path = os.path.abspath(path)
        # print(f"The path '{path}' is a relative path. The absolute path is: {absolute_path}")
        return absolute_path

def find_files(directory, pattern='*.mdx'):
    mdx_files = []
    # Traverse the directory tree
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            # Construct the absolute path and append it to the list
            mdx_files.append(os.path.abspath(os.path.join(root, filename)))
    if len(mdx_files) == 0:
        raise FileNotFoundError(f"No MDX files found in the directory: {directory}")
    if len(mdx_files) > 1:
        raise ValueError(f"Multiple MDX files found in the directory: {directory}")
    return mdx_files[0]

def read_paragraphs(filename):
    filename = get_absolute_path(filename)
    # Open the file in read mode with UTF-8 encoding
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Tokenize the read text into sentences
    sentences = sent_tokenize(text)
    return sentences

def get_wordnet_pos(pos_tag):
    """Convert POS tag to a format recognized by WordNetLemmatizer."""
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default

def read_sentence(sentence):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    words = [(word.lower(), pos) for word, pos in pos_tags if pos not in ('NNP', 'NNPS') and word.isalpha()]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in words]
    return lemmatized_words

def word_filter(word, coca=None):
    # Define the words to be filtered
    extracted_data = coca.search(word)
    if extracted_data == -1:
        return True
    
    # If the rank of the words is greater than 4000, return True
    if extracted_data['rank'] > 2000:
        return True
    return False

def format_dictionary(result_dict, dict_list):
    print(f"Word: {result_dict['word']}")
    if len(dict_list) != len(result_dict['result']):
        raise ValueError("The length of the dictionary list and the result list do not match.")
    for i in range(len(result_dict['result'])):
        if result_dict['result'][i] == -1:
            continue
        dict_list[i].format_output(result_dict['result'][i])
        