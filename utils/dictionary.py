import json
import os

from readmdict import MDX, MDD
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

from utils.helper import *


class Dictionary:
    def __init__(self, filename, with_voice=False):
        self.filename = get_absolute_path(filename)
        self.mdx_filename = find_files(self.filename, '*.mdx')
        self.load()

    def load(self):
        headwords = [*MDX(self.mdx_filename)]     
        items = [*MDX(self.mdx_filename).items()]
        if len(headwords)==len(items):
            print(f'Successfully load the dictionary, we have {len(headwords)} items.')
            self.items_num = len(headwords)
            self.headwords = headwords
            self.items = items
        else:
            raise ValueError(f'[ERROR] Fail to open the dictionary: {len(headwords)}, {len(items)}')
    
    def search(self, word):
        wordIndex = self.headwords.index(word.encode())
        word, html = self.items[wordIndex]
        word, html = word.decode(), html.decode()
        return self._parse_html(str(pq(html)))
    
    # Waiting for inheriting classes to implement
    def _parse_html(self, html):
        pass

class COCADictionary(Dictionary):
    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        word = soup.find('div', class_='word').text
        entries = []
        
        # Find all positions, ranks, total frequencies and frequency tables
        pos_elements = soup.find_all('span', class_='pos')
        rank_elements = soup.find_all('span', class_='rank')
        total_elements = soup.find_all('div', class_='total')
        table_elements = soup.find_all('div', class_='table')
        
        for i in range(len(pos_elements)):
            pos = pos_elements[i].text
            rank = int(rank_elements[i].text)
            total_frequency = int(total_elements[i].text)

            frequencies = {}
            for category_div in table_elements[i].find_all('div', recursive=False):
                category_name = category_div.get('class')[0]  # take the first class name as the category
                frequency = int(category_div.find('div', class_='freq').text)
                frequencies[category_name] = frequency

            entries.append({
                'part_of_speech': pos,
                'rank': rank,
                'total_frequency': total_frequency,
                'frequencies': frequencies
            })

        data = {
            'word': word,
            'entries': entries
        }
        
        return data

class LongmanDictionary(Dictionary):
    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract the word name
        word = soup.find('h1', class_='pagetitle').text
        
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
        
        return {
            'word': word,
            'entries': entry_data
        }

