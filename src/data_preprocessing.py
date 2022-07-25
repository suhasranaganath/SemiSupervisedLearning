"""
Summary:
    Read and process text of input file.

@authors: ivbarrie (this version); yabrumer (acm version)

"""

import os
import string
import re
import nltk
from pathlib import Path
import pandas as pd
pd.set_option('display.max_rows', None)
from atlm import analyzers
from fasttext_english_detector import LanguageIdentification
from config import Config







def clean_text(x, pii_kw_list=[r'alphanumericpii',
                              r'namepii',
                              r'xuidpii',
                              r'guidpii',
                              r'pii',
                              r'guid',
                              r'name',
                              r'alphanumeric',
                              r'phonenumber',  '[', ']', '|', '-', '(', ')']):

    for e in pii_kw_list:
        x = x.replace(e, '')
    x = x.replace('{}', '')
    x = x.replace('\n', ' ')
    x = ' '.join(x.split())


    return x

def union_text(row):
    r, c, s = row[Config.RESOLUTION_COLUMN_NAME], row[Config.CAUSE_COLUMN_NAME], row[Config.SYMPTOMS_COLUMN_NAME]
    X = set([r, c, s])
    union_str = '. '.join(str(x) for x in X)
    return union_str




def read_input_file(file_name):
    """Read input file and perform basic pre-processing (no analyzers).

    Params:
        file_name (str): file keyword used to form fully-qualified path

    Returns:
        df (DataFrame)

    """
    dtypes = {Config.INCIDENT_ID_COLUMN_NAME: 'str'}
    parse_dates = [Config.INCIDENTS_CLOSED_TIME_COLUMN_NAME]
    df = pd.read_csv(file_name,
                     dtype=dtypes,
                     parse_dates=parse_dates,
                     sep='\t',
                     lineterminator='\r',
                     warn_bad_lines=True,  # return idx of bad line that is skipped
                     error_bad_lines=False)  # do not read bad line
    print('input data columns:\n', list(df))
    print('input data shape:\n', df.shape)
    print('Removing nan val rows')
    df.fillna('', inplace=True)  # e.g. take care of float nan vals for str ops
    print('Removing trailing new-line spaces')
    for key in list(df):
        print(f"formatting key {key} to string")
        df[key] = df[key].astype(str)
        df[key] = df[key].apply(lambda x: x[1:] if x and x[0] == '\n' else x)
        df[key] = df[key].apply(lambda x: x[:-1] if x and x[-1] == '\n' else x)
    print('input data columns:\n', list(df))
    print('input data shape:\n', df.shape)
    print('Example of input data dates')
    print(df[Config.INCIDENTS_CLOSED_TIME_COLUMN_NAME].head(5))
    print('Quick check on Azure Firewall L2')
    df_az = df[df[Config.L2_RC_COLUMN_NAME].str.contains('Azure Firewall')]
    print(df_az[Config.L2_RC_COLUMN_NAME].head(5))
    print('Getting union of Resolution, Causetxt, Symptoms as one field')
    print(df.shape)
    print('Grouping by %s' % Config.INCIDENT_ID_COLUMN_NAME )
    df = df.groupby(Config.INCIDENT_ID_COLUMN_NAME).head(1)
    print('Summary of some root cause counts top 10')
    print('L2:')
    dv2 = df[Config.L2_RC_COLUMN_NAME].value_counts()
    print(dv2.head(10))
    print('L3:')
    dv3 = df[Config.L3_RC_COLUMN_NAME].value_counts()
    print(dv3.head(10))
    print('Input data shape after grouping')
    print(df.shape)
    print('dtypes of input data')
    print(df.dtypes)
    print('End of input data summary')
    df.fillna('', inplace=True)
    df[Config.CONCAT_TEXT_COLUMN_NAME] = ''
    df[Config.RES_CAUS_SYM_UNION] = df.apply(union_text, axis=1)
    print('Setting concat text prior to atlm-processing it')
    for t in [Config.TITLE_COLUMN_NAME, Config.RES_CAUS_SYM_UNION, Config.ISSUEDESCR_COLUMN_NAME]:
        df[t] = df[t].apply(lambda x: clean_text(x))
        df[t] = df[t].str.lower()
        df[Config.CONCAT_TEXT_COLUMN_NAME] += ' ' + df[t]
    df.fillna('', inplace=True)
    print('Clearing rows with empty %s' % Config.CONCAT_TEXT_COLUMN_NAME)
    print('Shape Before removing empty concat txt:', df.shape)
    df = df[df[Config.CONCAT_TEXT_COLUMN_NAME] != '']
    print('Shape after removing empty concat txt:', df.shape)
    print('Shape after read and first preprocessing', df.shape)
    return df






def english_text_filter(df, fasttext_lang_model_path):
    """Use FastText to predict whether input text is English"""
    lang_detector = LanguageIdentification(pretrained_lang_model_dir=fasttext_lang_model_path)
    df[Config.IS_ENGLISH_COLUMN_NAME] = df[Config.CONCAT_TEXT_COLUMN_NAME].\
                                        apply(lambda x: lang_detector.predict_is_english(x))

    return df

def set_lang_model_path(nlp_dir, fasttext_dir='fasttext',
                                 lang_model_name="lid.176.ftz"):
    print('os(listdir) nlp_dir', os.listdir(nlp_dir))
    lang_model_dir = os.path.join(nlp_dir, fasttext_dir, lang_model_name)
    return lang_model_dir

def replace_tags(text, exclude_keywords=['<', '{', 'question:', 'answer:']):
    """Replace words in text based on excluding keyword tags.

    Params:
        text (str): input to parse
        exclude_keywords (list(str)): tags to remove from words of text

    Returns:
        new_text (str): tag-excluded text

    """
    assert type(text) == str
    new_text = ''
    for word in text.split(' '):
        if not any(e in word for e in exclude_keywords) and len(word) > 1:
            new_text += word + ' '
    new_text = new_text[:-1]  # remove the last space
    return new_text

def process_text(input_text):
    filtered = replace_tags(input_text)
    filtered.translate(str.maketrans('', '', string.punctuation))
    filtered = re.sub('[^a-zA-Z]', ' ', filtered)
    filtered = re.sub(r'\[[0-9]*\]', ' ', filtered)
    filtered = re.sub(r'\s+', ' ', filtered)
    filtered = re.sub(r'\s+', ' ', filtered)
    filtered = filtered.lower()
    TEXT_TO_REPLACE = {'acm': 'azure cost management',
                       'cx': 'customer',
                       'nan': ''}
    for k, v in TEXT_TO_REPLACE.items():
        filtered = filtered.replace(k, v)
    return filtered


def remove_stop_words(text, tokens_to_remove):
    new_text = ' '.join([x for x in text.split() if x not in tokens_to_remove])
    return new_text





def process_input_file(input_file_path, nltk_dir):
    """
    Read file and apply english text and empty rows filters.

    Params:
        input_file_path (str or DataReference): path to input data (prior to pre-processing)
        excluded_rows_output_path (str or DataReference): output path for rows excluded prior to model inference
        lexicons_dir (str or DataReference): blob path of dir with structure lexicon/*txt
        nltk_dir (str or DataReference): blob path of nltk data including wordnet (so we don't download it online)
        debug (bool): whether to print pre-processing steps

    Returns:
        df (DataFrame): data ready to be used for model inference

    Notes:
        Previous processed_column_name is now explicitly referenced by Config.INPUT_TEXT_COLUMN_NAME
    """
    print('Looking for the following input file:\n%s' % input_file_path)
    df = read_input_file(input_file_path)
    # English Text analysis:
    print('Setting lang model path for English text selection...')
    lang_model_path = set_lang_model_path(nlp_dir=nltk_dir)
    print('Lang model path for english detection:\n%s' % lang_model_path)
    print('Applying -is english- filter')
    df = english_text_filter(df=df, fasttext_lang_model_path=lang_model_path)
    print('Done applying english filter, summary:')
    print(df[Config.IS_ENGLISH_COLUMN_NAME].value_counts())
    print('Initial text pre-processing via basic regex filters...')
    print('First setting %s based on process_text of %s' % \
          (Config.INPUT_TEXT_COLUMN_NAME, Config.CONCAT_TEXT_COLUMN_NAME ))
    df[Config.INPUT_TEXT_COLUMN_NAME] = df[Config.CONCAT_TEXT_COLUMN_NAME].apply(lambda x: process_text(x))
    print('Appending adls nltk dir explicitly from analyers module...')
    analyzers.add_nltk_dir(nltk_dir=nltk_dir)
    print('Applying lemmatizer for further text pre-processing...')
    lemmatizer = analyzers.LemmatizationFieldAnalyzer()
    df[Config.INPUT_TEXT_COLUMN_NAME] = lemmatizer.analyze(df[Config.INPUT_TEXT_COLUMN_NAME])
    print('Removing stopwords...')
    tokens_to_remove = nltk.corpus.stopwords.words('english')
    tokens_to_remove.append(['hi', 'not', 'would', 'like', 'help', 'want', 'know', 'need', 'assistance'])
    df[Config.INPUT_TEXT_COLUMN_NAME] = df[Config.INPUT_TEXT_COLUMN_NAME].\
        apply(lambda x: remove_stop_words(x, tokens_to_remove=tokens_to_remove))
    # separate rows to exclude and keep
    print('Done pre-processing text')
    print('Gathering data to exclude based on English + non-empty processed text...')
    df_keep = df[(df[Config.IS_ENGLISH_COLUMN_NAME] == True) & (df[Config.INPUT_TEXT_COLUMN_NAME] != '')]
    print('Removing column from non-excluded data\n: %s ' % Config.IS_ENGLISH_COLUMN_NAME)
    del df_keep[Config.IS_ENGLISH_COLUMN_NAME]  # Config.IS_ENGLISH_COLUMN_NAME not currently expected in Kusto table schema
    print('Final columns of DataFrame before model inference\n ' , list(df_keep))
    return df_keep