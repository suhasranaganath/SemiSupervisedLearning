"""
Created on 5/3/2020
@author: ahmos
@editor: ivbarrie

Last updated: 2020-08-03
"""

import pandas as pd
import json
import enum 
import re
import importlib
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer 

# custom libraries
import atlm.annotator as annotator
import atlm.tokenizer as tokenizer


def add_nltk_dir(nltk_dir):
    """Add storage paths for nltk wordnet, corpora, and taggers"""
    print('Adding nltk data dir from \n %s ' % nltk_dir)
    nltk.data.path.append(nltk_dir)  # append to list of paths nltk searches for data
    print('Check that nltk data dir added wordnet:\n %s', str(nltk.wordnet))
    return None

def load_analyzer_with_reflection(analyzer_type_path):
    module_name = analyzer_type_path[0:analyzer_type_path.rindex(".")]
    analyzer_type = analyzer_type_path[analyzer_type_path.rindex(".") + 1:]
    analyzer_module =  importlib.import_module(module_name)
    analyzer_ref = getattr(analyzer_module, analyzer_type)
    return analyzer_ref()

class TextProcessingPipeline(object):
    def __init__(self, analyzer_array):
        self.analyzer_pipeline = analyzer_array

    def analyze(self, items):
        for a in self.analyzer_pipeline:
            items = a.analyze(items)        
        return items


class StemmerFieldAnalyzer(object):

    def __init__(self):
        self.name = "StemmerFieldAnalyzer"
        self.ps = PorterStemmer()

    def analyze(self, items):
        """ applies preprocessing steps to each item in items and returns list of processed result per each item, in order. 
        If items are sentences of word surface forms, output will be sentences with stemmed word forms. """
        output = []
        for item in items:
            item = item.lower().strip()
            white_spaced_tokens = item.split()
            stemmed_item = []
            for tk in white_spaced_tokens:
                stemmed_item.append(self.ps.stem(tk))
            output.append(' '.join(stemmed_item))
        return output

class NamedEntityFieldAnalyzer(object):

    def __init__(self, tag_keeping_list, lexicons_dir, name="NamedEntityFieldAnalyzer"):

        self._tag_keeping_list = tag_keeping_list
        self.lexicons_dir = lexicons_dir
        self.name = name  # where is this attribute referenced?

    def analyze(self, items):
        output = []
        for item in items:
            output.append(self.process_text(item))
        return output

    def process_text(self, data):
        try:
            annotations = annotator.get_annotations(char_sequence=data.lower(), lexicons_dir=self.lexicons_dir)
            tagged_tokened_text = annotator.process_text_with_annotations(data.lower(), annotations, self._tag_keeping_list)
        except Exception as ex:
            print("Exception during text processing in {0}. Details:{1}".format(self.name,str(ex)))
            tagged_tokened_text = data
        return tagged_tokened_text

class LemmatizationFieldAnalyzer(object):

    def __init__(self, ):
        self.name = "LemmatizationFieldAnalyzer"
        self.lemmatizer = WordNetLemmatizer()      

    def analyze(self, items):
        output = []
        for item in items:
            item = item.lower().strip()
            white_spaced_tokens = item.split()
            postagged_tokens = nltk.pos_tag(white_spaced_tokens)
            lemmatized_tokens = []
            for (word, tag) in postagged_tokens:
                if tag.startswith('V'): # tags of verb POS class, e.g. vbz
                    tag = 'v'
                elif tag.startswith('A'): # tags of adjective POS class
                    tag = 'a'
                else:
                    tag = 'n' # tags of noun class, e.g. nns
                lemmatized_tokens.append(self.lemmatizer.lemmatize(word, pos=tag))
            output.append(' '.join(lemmatized_tokens))
        return output