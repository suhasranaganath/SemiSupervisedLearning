"""
Created on 2/26/2020
@author: ahmos
@editor: ivbarrie

Last updated: 2020-08-03
"""

import ply.lex as lex


# List of token names.   This is always required
tokens = (
    'EMAIL',
    'URI',
    'URI2',
    'GUID',
    'MONETARY',
    'TEMP_SET',
    'TEMP_DURATION',
    'DATE',
    'TIME',
    'HYPTHNATION',
    'VERSION_NUM',
    'STORAGE_QUANTITY',
    'CLITIC',
    'SR',
    'NUMBER',
    'IDENTIFIER',
    'ALPHANUM',
    'SEPARATOR'
)

named_entity_types =[
    'EMAIL',
    'URI',
    'URI2',
    'GUID',
    'MONETARY',
    'TEMP_SET',
    'TEMP_DURATION',
    'DATE',
    'TIME',
    'HYPTHNATION',
    'VERSION_NUM',
    'STORAGE_QUANTITY',
    'CLITIC',
    'IDENTIFIER',
    'SR',
    'NUMBER'
]

filter_token_type_list = ['DATE', 'TIME', 'GUID', 'URI', 'URI2', 'NONASCII']


#1
def t_GUID(t):
    r'\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12}'
    return t

#2
def t_EMAIL(t):
    #credit: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    #URI = scheme:[//authority]path[?query][#fragment]    
    r'[A-z][A-z0-9_\.\-]+@\S+(\.\S+)*(/\S+)*?\S*'
    return t

#2
def t_URI(t):
    #credit: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    #URI = scheme:[//authority]path[?query][#fragment]    
    r'\w{3,}://\S+(\.\S+)*(/\S+)*?\S*'
    return t


#3
def t_URI2(t):
    #credit: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    #URI = scheme:[//authority]path[?query][#fragment]    
    r'(www)(\.\S+)+(/\S+)*?\S*'
    #r'(www)'
    return t

#4
def t_VERSION_NUM(t):
    r'\d+(\.\d+)+'   
    return t

#5 
def t_MONETARY(t):
    r'''\$\d+(\.\d+)*(\/\S+)?
    |\d+(\.\d+)*(\s*)(dollars|dollar|euros|euro|pesos|dlrs|dlr)(\/\S+)?
    '''   
    return t

#6
def t_DATE(t):
    r'''([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0|1])?(st|nd|rd|th)?\s*(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s*(\,)?\s*(19\d{2}|20\d{2})
    |(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0|1])[\s|\,]?\s*[\,]?(19\d{2}|20\d{2})
    |(0[1-9]|1[0-2]|[1-9]|[1-9])([\.|\-|\/])((0[1-9]|1[0-9]|2[0-9]|3[0|1]|[1-9])([\.|\-|\/]))?(19\d{2}|20\d{2})
    |(19\d{2}|20\d{2})([\.|\-|\/])(0[1-9]|1[0-2]|[1-9]|[1-9])([\.|\-|\/])(0[1-9]|1[0-9]|2[0-9]|3[0|1][1-9])
    '''
    # this one below (using capture group \2) does not work!
    #r'''(0[1-9]|1[0-2]|[1-9])([\.|\-|\/])(0[1-9]|1[0-9]|2[0-9]|3[0|1])\2(19\d{2}|20\d{2})
    #'''
    return t

#7
def t_TIME(t):
    r'(t)?(0[1-9]|1[0-9]|2[0-3]|[1-9]):(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[1-9])(:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[1-9])(\.\d+)?)?(\s*(am|pm))?\s*(gmt|utc|pst|est)?'
    return t

#8
# temporal expression: duration
def t_TEMP_SET(t):
    r'''(current|next|last|previous|past|coming)\s*(month|year|week|quarter|semester|term|january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*(19\d{2}|20\d{2})?
    |(today|yesterday|tomorrow)
    '''
    return t

#9
# temporal expression: duration
def t_TEMP_DURATION(t):
    r'''(\d+)\s*(years|months|weeks|days|hours|minutes|seconds|milliseconds|microseconds|yrs|year|yr|month|day|hour|hrs|hr|minute|mins|min|second|secs|sec)
    '''
    return t

#10
def t_HYPTHNATION(t):
    r'\w+(\-\w+)+'   
    return t

#11
def t_CLITIC(t):
    r'\'(re|ve|m|s)'   
    return t

#12 
def t_STORAGE_QUANTITY(t):
    r'\d+(\.\d+)*\s*(mb|gb|tb|pb|kb|megabyte|gigabyte|terabyte)'   
    return t

def t_SR(t):
    r'(support request|sr\#|sr \#|sr no\.|sr no|sr number|case number|case|sr)\s*\d+|\d{15,}'
    return t

#13
# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    #t.value = int(t.value)    
    return t

#14
# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[A-z]+\d+[A-z0-9]+'
    return t

#15
def t_ALPHANUM(t):
    r'\w[\w|\d]*'
    return t

#16
# A regular expression rule with some action code
def t_SEPARATOR(t):
    r'\s|\,|\;|\-|\:|\.|\?|\!|\#|\%|\*|\(|\)|\\|/|\[|\]|\{|\}'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def tokenize(char_sequence):
    lexer.input(char_sequence)
    lex_token_list = []
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        lex_token_list.append((int(tok.lexpos), int(tok.lexpos) + len(str(tok.value)), str(tok.type),str(tok.value)) )
    return lex_token_list

#credit:https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def find_non_ascii_segments(char_sequence):
    annotations = []
    start = 0
    index = char_sequence.find(' ',start)
    if index == -1: # no white spaces
        annotations.append( (0, len(char_sequence) , 'NONASCII', char_sequence) )
        return annotations
    
    while index > -1:
        segment = char_sequence[start:index+1]
        if not is_ascii(segment):
            annotations.append( (start, index+1, 'NONASCII', segment) )
        start = index + 1
        index = char_sequence.find(' ',start)

    if start < len(char_sequence):
        segment = char_sequence[start:]
        if not is_ascii(segment):
            annotations.append( (start, len(char_sequence), 'NONASCII', segment) )
    return annotations

def heuristic_tag_non_English(char_sequence):
    annotations = []
    return annotations