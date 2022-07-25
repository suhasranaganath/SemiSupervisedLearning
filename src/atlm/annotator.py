
"""
Created on 2/26/2020
@author: ahmos
@editor: ivbarrie

Last updated: 2020-08-03
"""

import atlm.tokenizer as tokenizer
import atlm.entity_lookup as lookup

def get_regex_annotations(char_sequence):
    return [token_info for token_info in tokenizer.tokenize(char_sequence) if token_info[2] in tokenizer.named_entity_types]

def get_annotations(char_sequence, lexicons_dir):
    # NOTE: lookup.get_dictionary invokes lexicons/*txt
    annotations = get_regex_annotations(char_sequence) + \
                  lookup.get_dictionary_lookup_annotations(text=char_sequence, lexicons_dir=lexicons_dir) + \
                  tokenizer.find_non_ascii_segments(char_sequence)
    return  annotations

def remove_conflicting_annotations(annotation_list):
    sorted_annotations = sorted(annotation_list, key=lambda x: x[1]) # sorting by 2nd element
    new_list = []
    n = len(sorted_annotations)
    if n <= 1:
        return list(sorted_annotations)
    
    for i in range(1,n):
        s1,e1, t1, v1 = sorted_annotations[i-1]
        s2,e2, t2, v2 = sorted_annotations[i]
        if e1 <= s2:
            new_list.append(sorted_annotations[i-1])
    new_list.append(sorted_annotations[n-1])
    return new_list

def process_text_with_annotations(text, annotations, keep_tag_annotations):
    annotations = remove_conflicting_annotations(annotations)
    text_segments = []
    sorted_annotations = sorted(annotations, key=lambda x: x[1]) # sorting by 2nd element
    index = 0

    for i in range(len(annotations)):
        (start, end, ne_type, ne_val) = sorted_annotations[i]
        if index < start:
            text_segments.append(text[index:start])
        if ne_type in keep_tag_annotations:
            text_segments.append('<' + ne_type + '> ' + ne_val + ' </' + ne_type + '>' )
        index = end
    text_segments.append(text[index:len(text)])
    return ' '.join(text_segments)

def tag_text_with_annotations(char_sequence, text_annotations ):
    output_text = char_sequence.lower()
    n_annotations = len(text_annotations)
    for i in range(n_annotations):
        annotation = text_annotations[i]
        (start, end, ne_type, ne_val) = annotation
        if ne_type in tokenizer.named_entity_types or \
                ne_type in lookup.entity_type_source.keys() or \
                ne_type == 'NONASCII':
            if ne_type in tokenizer.filter_token_type_list:
                output_text = output_text.replace(ne_val,'<' + ne_type + '_Removed>' )
            else:
                output_text = output_text.replace(ne_val.lower(), " <" + str(ne_type) + \
                                                  "> " + ne_val.lower() + " </" + str(ne_type) + "> ")

    return output_text