import json
import os

from readmdict import MDX, MDD
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

from utils.helper import *

class Dictionary:
    def __init__(self, filename):
        self.dictionary_name = os.path.basename(filename)
        self.filename = get_absolute_path(filename)
        self.mdx_filename = find_files(self.filename, '*.mdx')
        self.load()
        self.attributes = {}

    def load(self):
        headwords = [*MDX(self.mdx_filename)]     
        items = [*MDX(self.mdx_filename).items()]
        if len(headwords)==len(items):
            print(f'Successfully load {self.dictionary_name} dictionary, we have {len(headwords)} items.')
            self.items_num = len(headwords)
            self.headwords = headwords
            self.items = items
        else:
            raise ValueError(f'[ERROR] Fail to open the dictionary: {len(headwords)}, {len(items)}')
    
    def search(self, word):
        try:
            wordIndex = self.headwords.index(word.encode())
        except ValueError:
            print(f"The word \'{word}\' is not found in the {self.dictionary_name} dictionary.")
            return -1  #
        word, html = self.items[wordIndex]
        word, html = word.decode(), html.decode()
        return self._parse_html(str(pq(html)))
    
    # Waiting for inheriting classes to implement
    def _parse_html(self, html):
        raise NotImplementedError
        pass
    
    def format_output(self, entry):
        raise NotImplementedError
        pass
    
    def result_to_latex(self, entry):
        raise NotImplementedError
        pass

class COCADictionary(Dictionary):
    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        word = soup.find('div', class_='word').text
        entry = None
        
        # Parse the html file and filter some not found cases specifically
        pos_elements = soup.find_all('span', class_='pos')
        rank_elements = soup.find_all('span', class_='rank')
        total_elements = soup.find_all('div', class_='total')
        table_elements = soup.find_all('div', class_='table')
        
        if pos_elements == [] or rank_elements == [] or total_elements == [] or table_elements == []:
            # print(f"The word \'{word}\' is not found in the {self.dictionary_name} dictionary.")
            return -1
        
        for i in range(len(pos_elements)):
            pos = pos_elements[i].text
            rank = int(rank_elements[i].text)
            total_frequency = int(total_elements[i].text)

            frequencies = {}
            for category_div in table_elements[i].find_all('div', recursive=False):
                category_name = category_div.get('class')[0]  # take the first class name as the category
                frequency = int(category_div.find('div', class_='freq').text)
                frequencies[category_name] = frequency

            # Should I only take the largest one?
            # TODO: Use the pos tag to filter the frequency
            if entry is None or entry['rank'] > rank:
                entry = {
                    'part_of_speech': pos,
                    'rank': rank,
                    'total_frequency': total_frequency,
                    'frequencies': frequencies}

        return entry

class LongmanDictionary(Dictionary):
    
    def __init__(self, filename):
        super().__init__(filename)
        self.attributes = ['pronunciation', ['part_of_speech', ['senses', ['definition', 'examples']]]]
        
    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
            
        # Extract the word name
        word = soup.find('h1', class_='pagetitle')
        if word is None:
            print(f"The word is not found in the {self.dictionary_name} dictionary.")
            return -1
        word = word.text
        
        # Extract pronunciation and frequency information
        entry_data = []
        for entry in soup.find_all('span', class_='ldoceEntry Entry'):
            entry_info = {}
            
            # Extract the pronunciation
            head = entry.find('span', class_='Head')
            if head:
                pronunciation = head.find('span', class_='PRON')
                if pronunciation:
                    entry_info['pronunciation'] = pronunciation.text.strip()
            
            # Extract part of speech
            pos = head.find('span', class_='lm5pp_POS') if head else None
            if pos:
                entry_info['part_of_speech'] = pos.text.strip()

            # Extract definitions and examples
            senses = entry.find_all('span', class_='Sense')
            sense_list = []
            for sense in senses:
                sense_data = {}
                
                definition = sense.find('span', class_='DEF')
                sense_data['definition'] = definition.text.strip() if definition else ""
                
                examples = []
                for example in sense.find_all('span', class_='EXAMPLE'):
                    example_text = example.find('span', class_='english LDOCE_switch_lang switch_children')
                    if example_text:
                        examples.append(example_text.text.strip().split('\n')[0])  # Extract only the English part
                sense_data['examples'] = examples
                
                sense_list.append(sense_data)
                
            entry_info['senses'] = sense_list
            
            entry_data.append(entry_info)
        
        return entry_data
    
    def format_output_printing(self, entries):
        for entry in entries:
            # Print pronunciation if available
            if 'pronunciation' in entry:
                print(f"Word: {entry.get('pronunciation').capitalize()}\n")
            
            part_of_speech = entry.get('part_of_speech', 'Unknown')
            print(f"Part of Speech: {part_of_speech.capitalize()}\n")

            for i, sense in enumerate(entry.get('senses', []), 1):
                definition = sense.get('definition', 'No definition provided')
                print(f"{i}. Definition: {definition}")
                
                examples = sense.get('examples', [])
                if examples:
                    print("   Examples:")
                    for example in examples:
                        print(f"   - {example}")
                print() 

class VocabularyDictionary(Dictionary):
    
    def __init__(self, filename):
        super().__init__(filename)
        self.attributes = ['meaning', 'explanation']
        
    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Parse the html file and filter some not found cases specifically
        its_elements = soup.find_all(class_='i t s')
        ai_elements = soup.find_all(class_='a i')
        
        if len(its_elements) == 0 or len(ai_elements) == 0:
            print(f"The word is not found in the {self.dictionary_name} dictionary.")
            return -1
        if len(its_elements) != 1 or len(ai_elements) != 1:
            # print(html)
            # raise NotImplementedError
            # TODO: Handle the case where there are multiple meanings and explanations
            pass
        
        # Make the return data structure   
        entries = {'Meaning': its_elements[0].text.replace("\'", "'"),
                   'Explanation': ai_elements[0].text.replace("\'", "'")}
        return entries
    
    def format_output_printing(self, entry):
        for key in entry:
            print(f"{key}: {entry[key]}")
        print()