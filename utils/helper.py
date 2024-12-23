import os
import fnmatch
import subprocess
import re

from weasyprint import HTML
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
    
def load_learned_words(path):
    path = get_absolute_path(path)
    with open(path, 'r', encoding='utf-8') as file:
        # Read all lines in the file
        lines = file.readlines()
        # Create a set from the words, stripping whitespace and newline characters
        word_set = {line.strip() for line in lines}
        
    return word_set

def find_files(directory, pattern='*.mdx'):
    mdx_files = []
    # Traverse the directory tree
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            # Construct the absolute path and append it to the list
            mdx_files.append(os.path.abspath(os.path.join(root, filename)))
    return mdx_files

def read_essay(filename):
    filename = get_absolute_path(filename)
    # Open the file in read mode with UTF-8 encoding
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Tokenize the read text into paragraphs
    paragraphs = text.strip().split('\n\n')
    return [para.replace('\n', ' ').strip() for para in paragraphs if para.strip()]

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

def format_dictionary(result_dict, dict_list):
    print(f"Word: {result_dict['word']}")
    if len(dict_list) != len(result_dict['result']):
        raise ValueError("The length of the dictionary list and the result list do not match.")
    for i in range(len(result_dict['result'])):
        if result_dict['result'][i] == -1:
            continue
        dict_list[i].format_output(result_dict['result'][i])
        
# These two functions come from the latex template file.
# TODO: Find a better way to load the format from the template file.

def result_exist(result_dict):
    for result in result_dict['result']:
        if result != -1:
            return True
    return False

def add_around_substring(text, target, prefix, suffix):
    # Directly replace the target with prefix and suffix added
    modified_text = text.replace(target, f'{prefix}{target}{suffix}')
    return modified_text

from utils.personal import check_whether_paragraph_is_section_title

def write_paragraph_to_latex(sentence, results, output_file, dict_list):
    with open(output_file, 'a', encoding='utf-8') as file:
        
        if not check_whether_paragraph_is_section_title(sentence):
            word_list = [result['word'] for result in results if result_exist(result)]
            for i in word_list:
                sentence = add_around_substring(sentence, i, '\\textbf{', '}')
            word_string = ', '.join(word_list)
            
            # file.write("\\clearpage\n\\noindent\n")
            
            file.write("\\colorbox{bgcolor}{\\parbox{\\dimexpr\\linewidth-2\\fboxsep}{\n")        
            file.write(f"{sentence}\n")
            file.write("}}\\vspace{0.5cm}\\noindent\n\n")
            
            # Add the word list and explanations
            if len(word_list) > 0:
                file.write(f"\\textbf{{Word:}} {word_string}\\\\\n\n")
        else:
            file.write("\\clearpage\n\\noindent\n")
            file.write(f"\\chapter{{{sentence}}}\n\n")
    # for result in results:
    #     if result_exist(result):
    #         write_word_to_latex(result, output_file, dict_list)
    
def write_word_appendix(current_words, output_file):
    words = current_words
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write("\\clearpage\n\\noindent\n")
        file.write("\\fancyhead[LE,RO]{\\thepage}\n")
        file.write("\\fancyhead[RE,LO]{Appendix \\thechapter} \n")
        file.write("\\appendix")
        
        file.write("\\chapter{Word Lists}\n\n")
        file.write("\\begin{multicols}{4}\n")
        for i in words:
            file.write(f"{i}\n\n")
        file.write("\\end{multicols}\n")
            
def write_word_to_latex(result_dict, output_file, dict_list):
    with open(output_file, 'a', encoding='utf-8') as file:
        # file.write("\\clearpage\n\\noindent\n")
        for i in range(len(dict_list)):
            if result_dict['result'][i] == -1:
                continue
            latex_string = dict_list[i].result_to_latex(result_dict['word'], result_dict['result'][i])
            file.write(latex_string)

def symbols_to_latex(text):
    # Define a dictionary for mapping symbols to their LaTeX equivalents
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    
    # For each symbol in the map, replace it in the text
    for symbol, latex in replacements.items():
        text = text.replace(symbol, latex)
        
    pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+')
    # Replace matching patterns with an empty string
    cleaned_text = pattern.sub('', text)
        
    return cleaned_text

def generate_pdf_from_html_string(html_content, output_pdf, base_url=None):
    # Create an HTML object from a string
    html = HTML(string=html_content, base_url=base_url)
    html.write_pdf(target=output_pdf)


        