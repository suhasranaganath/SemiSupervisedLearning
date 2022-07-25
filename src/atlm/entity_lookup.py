
"""
Created on 2/26/2020
@author: ahmos
@editor: ivbarrie

Last updated: 2020-08-03
"""

import os
print('Entering entity_lookup module...')

entity_type_source = {
    'VMSIZE': r'VMSizes.txt',
    'VM_SERIES': r'VMSeries.txt',
    'WEB_BROWSER': r'browsers.txt',
    'OFFER_TYPE': r'OfferType.txt',
    'ACM_INTENT': r'ACMFunctionality.txt',
    'COUNTRY': r'Countries.txt',
    'OPERATING_SYSTEM': r'OS.txt',
    'AZURE_PRODUCT': r'AzureProducts.txt',
    'AZURE_REGION' : r'AzureRegion.txt',
    'ORG_NAME': r'OrgName.txt',
    'MS_DIVISION': r'MSDivisionName.txt',
    'SERVICE_NAME': r'ServiceName.txt',    
}

named_entity_trie_map = {}

class DictionarySearch(object):
    def __init__(self, lex_entries):
        self.patterns = lex_entries
    
    def is_delimiter_char(self, ch):
        if ch in [' ', ',', '.','-',';']:
            return True
        return False

    def find_patterns(self, text):
        match_list = []
        for p in self.patterns:
            start_pos = text.find(p)
            end_pos = start_pos + len(p)
            if start_pos > -1:
                if (start_pos == 0 or \
                    self.is_delimiter_char(text[start_pos - 1]) ) and \
                    (end_pos == len(text) or self.is_delimiter_char(text[end_pos])):
                    match_list.append((p, start_pos, end_pos))
        return match_list

    def search_longest_patterns(self, text):
        pattern_match_annotations = self.find_patterns(text)
        # keep longest patterns
        n = len(pattern_match_annotations)
        filtered_patterns = []
        for i in range(n):
            (p1,s1,e1) = pattern_match_annotations[i]
            is_within_other_patterns = False
            for j in range(n):
                if j == i: continue
                (p2,s2,e2) = pattern_match_annotations[j]
                if s1>=s2 and e1 <= e2:
                    is_within_other_patterns = True
                    break
            if is_within_other_patterns == False:
                filtered_patterns.append(pattern_match_annotations[i])

        return filtered_patterns

def load_entity_types(lexicons_dir):
    for ne_type, filename in entity_type_source.items():
        with open(os.path.join(lexicons_dir, filename), encoding='utf-8') as file_handler:
            patterns = file_handler.readlines()
            patterns = [p.strip().lower() for p in patterns]
            named_entity_trie_map[ne_type] = DictionarySearch(patterns)

def get_dictionary_lookup_annotations(text, lexicons_dir):
    load_entity_types(lexicons_dir=lexicons_dir)
    text = text.lower()
    annotation_records = []
    for entity_type in named_entity_trie_map.keys():
        trie = named_entity_trie_map[entity_type]  # named_entity_trie defined in load_entity_types()
        for lexeme, start_idx, end_idx in trie.search_longest_patterns(text):
            annotation_records.append((start_idx, end_idx, entity_type, lexeme))
    return annotation_records