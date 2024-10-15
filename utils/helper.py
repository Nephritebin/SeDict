import os
import fnmatch

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


def get_absolute_path(path):
    # Check if the path is absolute
    if os.path.isabs(path):
        print(f"The path is already an absolute path: {path}")
        return path
    else:
        # Convert to absolute path
        absolute_path = os.path.abspath(path)
        print(f"The path '{path}' is a relative path. The absolute path is: {absolute_path}")
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

def read_sentences(sentence):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    transformed_words = [word.lower() if pos not in ('NNP', 'NNPS') else word
        for word, pos in pos_tags
    ]
    words = [word for word in transformed_words if word.isalpha()]
    
    print(words)
    
    lemmatizer = WordNetLemmatizer()
    stemmed_words = [lemmatizer.lemmatize(word) for word in words]
    return stemmed_words
    