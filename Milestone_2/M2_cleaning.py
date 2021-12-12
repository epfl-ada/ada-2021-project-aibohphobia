import numpy as np
import pandas as pd
import datetime as dt
import bz2
import json
from tld import get_tld
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import string
import math
from collections import Counter
from operator import itemgetter
import re
from tqdm.auto import trange, tqdm

nltk.download('stopwords')
nltk.download('punkt')


def get_sitename(url):
    """
        Function to extract sitename from a URL
    :param url:  string with url to parse
    :return: String with name of site
    """
    res = get_tld(url, as_object=True)
    return res.domain


def extract_name(df):
    """
    Function to extract sitename from a list of URLs (a row in the original dataset)
    :rtype: dataframe with new column `sitename`
    """
    df['sitenames'] = np.nan
    for row in range(df.shape[0]):
        df['sitenames'][row] = [get_sitename(site) for site in df['urls'][row]]


def get_domain(url):
    """
        Function to extract domain from a URL
    :param url: string with url
    :return: string with domain main
    """
    res = get_tld(url, as_object=True)
    return res.tld


def tokenize(text):
    """
        Function to transform a string into a list of words in their generalised form
    :param text: strings
    :return: list of strings (tokenized words)
    """
    stemmer = PorterStemmer()
    text = "".join([ch for ch in text if ch not in string.punctuation])  # get the text without punctuation
    tokens = nltk.word_tokenize(text)  # Tokenizers divide strings into lists of substrings
    return " ".join(
        [stemmer.stem(word.lower()) for word in tokens if word not in stopwords.words('english')])  # stem all words


def generalizeDictionary(matchers):
    """
        Function to put transform a dictionary (key-value is category-word) into its generalised form
    :param matchers: dictionary with each category associated with different words. for eg: {"art": ["art", "paint", "draw", "museum"]}
    """
    stemmer = PorterStemmer()
    for category in matchers:
        for i in range(len(matchers[category])):
            matchers[category][i] = tokenize(matchers[category][i])


def getWordsFromURL(url):
    """
        Function to split a url into separate words
    :param url: string of url
    :return: string of url split in words
    """
    return re.compile(r'\W+', re.UNICODE).split(url)


def classify(matchers, url):
    """
        Given a (generalised) dictionary, add tags to a URL if certain words/topics detected.
    :param matchers: dictionary with each category associated with different words. for eg: {"art": ["art", "paint", "draw", "museum"]}
    :param url: string of url
    :return: dictionary with added tags if categories are found in URLS
    """
    stemmer = PorterStemmer()
    tag_found = []
    general_url = [tokenize(x) for x in getWordsFromURL(url)]
    for category in matchers:
        for i in range(len(matchers[category])):
            match = matchers[category][i]
            if match in general_url:
                tag_found.append(category)
    return tag_found


# Cleaning data functions #

def Remove_none_speakers(chunk):
    """
        Remove where speaker is None type
    :param chunk: dataframe
    :return: dataframe with dropped None speakers
    """
    chunk = chunk.drop(chunk[chunk['speaker'] == 'None'].index)
    chunk = chunk.reset_index(drop=True)
    return chunk


def Remove_none_unique_ids(chunk):
    '''
        Remove duplicate quoteIDs
    :param chunk: dataframe
    :return: dataframe with removed duplicate quoteIDs
    '''
    if not (chunk.quoteID.is_unique):
        chunk = chunk.drop_duplicates(subset=['quoteID'], keep='first')
    return chunk


def Remove_empty_quotes(chunk):
    '''
        Remove empty quotes
    :param chunk: dataframe
    :return: dataframe with deleted empty quotes
    '''
    chunk = chunk.drop(chunk[chunk["quotation"].isna() | chunk["quotation"].isnull()].index)
    chunk = chunk.reset_index(drop=True)
    return chunk


def extract_element_from_series(array):
    """
        From a series of arrays, we keep only the first element of the arrays
    :param array: series of array
    :return:series with first elements of each arrays
    """
    single = array.apply(lambda x: 'NaN' if x is None else x[0])
    return single


def Remove_empty_qids(chunk):
    """
        Remove rows with empty qids
    :param chunk: dataframe
    :return: dataframe with deleted empty qids for speakers rows
    """
    chunk = chunk.drop(chunk[chunk['qids'].apply(lambda x: False if x else True)].index)
    chunk['qids'] = extract_element_from_series(chunk['qids'])
    chunk = chunk.reset_index(drop=True)
    return chunk


def Remove_low_proba(chunk, threshold):
    """
        Remove speakers when the probability of being the speaker is below the threshold
    :param chunk: dataframe
    :param threshold: threshold of below which we remove speakers due to uncertainty
    :return: dataframe with only fairly certain speakers kept
    """
    # Gather the first probability for each row
    string_probas, nber_probas = [], []
    chunk['probas'] = extract_element_from_series(chunk['probas'])
    string_probas = chunk['probas']
    string_probas = [string_probas[i][1] for i in chunk.index]
    nber_probas = list(map(float, string_probas))
    series_probas = pd.Series(nber_probas, dtype='float64', index=chunk.index)

    # Check if the probability is larger than the threshold, if not remove corresponding index
    chunk = chunk.drop(series_probas[series_probas < threshold].index)
    chunk = chunk.reset_index(drop=True)
    return chunk


def Chunk_url_extract(chunk, matchers):
    """
        Function that takes a dataframe and will extract sitename, domain and topics (tags) from URL
    :param chunk: dataframe
    :param matchers: dictionary with each category associated with different words. for eg: {"art": ["art", "paint", "draw", "museum"]}
    :return: dataframe with addtional columns for sitename, domain and tags
    """

    tags_column = []  # List of lists. Each list inside corresponds to a row. Will become the 'tag' column
    site_column = []
    domain_column = []
    len_chunk = len(chunk)
    print('Total length: ', len_chunk)
    for index, row in tqdm(chunk.iterrows()):
        tags = []  # tags for all the urls in that row
        domains = []
        sitenames = []
        for url in row['urls']:
            # Extract data
            tld = get_domain(url)
            name = get_sitename(url)
            categories = classify(matchers, url)
            # Append data
            domains.append(tld)
            sitenames.append(name)
            tags.append(categories)
        tags_column.append(tags)
        site_column.append(sitenames)
        domain_column.append(domains)
    # Create new columns with new data
    chunk['sitenames'] = site_column
    chunk['domain'] = domain_column
    chunk['tags'] = tags_column
    return chunk


### Wikidata processing: this is done once only###
# -------------------------------------------------------
def qid_to_gender(Wikidata_speakers):
    """
        Given a qid, extract gender and date of birth from Wikidata_speakers file
    :param Wikidata_speakers: dataframe with information about speakers
    :return: dataframe with gender renamed from QID to male/female
    """
    df_speakers = Wikidata_speakers[['id', 'label', 'gender', 'nationality', 'date_of_birth']].copy()
    df_speakers['gender'] = extract_element_from_series(df_speakers['gender'])
    df_gender = pd.DataFrame({'qid': ['Q6581097', 'Q6581072'], 'sex': ['Male', 'Female']})
    Wikidata_gender = pd.merge(df_speakers, df_gender, left_on='gender', right_on='qid',
                               how='inner')  # row removed if no gender specified in the wikidata
    return Wikidata_gender


def qid_to_citizenship(df_speakers, Wikidata_countries):
    """
        Given a qid, extract citizenship of speaker from Wikidata_coruntries file
    :param df_speakers: dataframe we wish to add information of citizenship to
    :param Wikidata_countries: dataframe with info about nationality of spkeakers
    :return:
    """
    df_speakers['nationality'] = extract_element_from_series(df_speakers['nationality'])
    df_citizenship = pd.merge(df_speakers, Wikidata_countries, left_on='nationality', right_on='QID', how='left')

    Wikidata_citizenship = df_citizenship[['id', 'sex', 'Label', 'Description']]
    Wikidata_citizenship = Wikidata_citizenship.rename(
        columns={'label': 'name', 'Label': 'citizenship', 'sex': 'gender'})
    return Wikidata_citizenship


def formating_wikidata(Wikidata_speakers, Wikidata_countries):
    """
        Given a Wikidata_speakers, Wikidata_countries and a qid, extract nationality, gender, date of birth
    :param Wikidata_speakers: dataframe we wish to add information to
    :param Wikidata_countries: dataframe with info about nationality of spkeakers
    :return: dataframe with additional information such as gender and nationality
    """
    Wikidata_gender = qid_to_gender(Wikidata_speakers)

    Wikidata_citizenship = qid_to_citizenship(Wikidata_gender, Wikidata_countries)

    return Wikidata_citizenship


# -------------------------------------------------------


### This is called in the preprocessing
def merge_quotes_wikidata(Wikidata_utils, df):
    """
        Given the Wikidata_utils (pickle file to download on drive)
        and open the following way
        ----with open('Wikidata_utils.pkl', 'rb') as input_file:
                Wikidata_utils = pickle.load(input_file)---
                :param Wikidata_utils: dataframe with wikidata we use to merge
                :param df: dataframe
                :return: dataframe with additional information fomr  wikidata
    """
    Quotes_merged = pd.merge(df, Wikidata_utils, left_on='qids', right_on='id', how='left')
    Quotes_merged_id_drop = Quotes_merged.drop('id', axis=1)
    Quotes_merged_drop_gender = Quotes_merged_id_drop.dropna(subset=['gender'], axis=0)
    Quotes_final = Quotes_merged_drop_gender.reset_index(drop=True)
    return Quotes_final


### Preprocess whole chunk ###
#TODO: Remove this
"""

def process_chunk_complete(chunk, threshold_proba = 0.5, matchers, Wikidata_speakers, Wikidata_countries):
    '''
    Apply data cleaning and url informaiton extraction to a dataframe
    '''
    print(f'Processing chunk with {len(chunk)} rows')
    # DATA CLEANING
    # Remove None speakers
    chunk = Remove_none_speakers(chunk)

    # Remove none unique ids and keep the first one
    chunk = Remove_none_unique_ids(chunk)

    # Remove nan or empty quotes
    chunk = Remove_empty_quotes(chunk)

    # Remove empty qids and keep the first one
    chunk = Remove_empty_qids(chunk)

    # Remove speakers for which probability is lower than a threshold, and keep the first speaker if several
    chunk = Remove_low_proba(chunk, threshold_proba)

    # Add gender and citizenship
    chunk = merge_quotes_wikidata(Wikidata_speakers, Wikidata_countries, chunk)

    # URLS DATA EXTRACTION
    chunk = Chunk_url_extract(chunk, matchers)

    tot_length = len(chunk)
    return chunk, tot_length

"""
## Basic cleaning
def rapid_clean(df_base, threshold_proba=0.5):
    '''
        Apply basic data cleaning to a dataframe
    :param df_base: dataframe we wish to clean
    :param threshold_proba: threshold below which speakers are removed due to uncertainty (default = 50%)
    :return:
    '''

    df_base = Remove_none_speakers(df_base)

    # Remove none unique ids and keep the first one
    df_base = Remove_none_unique_ids(df_base)

    # Remove nan or empty quotes
    df_base = Remove_empty_quotes(df_base)

    # Remove empty qids and keep the first one
    df_base = Remove_empty_qids(df_base)

    # Remove speakers for which probability is lower than a threshold, and keep the first speaker if several
    df_base = Remove_low_proba(df_base, threshold_proba)
    return df_base

"""
Not used
def extract_and_merge(Wikidata_speakers, Wikidata_countries, df, matchers):
    '''
        Extract URL and Wikidata information from a dataframe
    :param Wikidata_speakers: 
    :param Wikidata_countries: 
    :param df: 
    :param matchers: 
    :return: 
    '''
    # Add gender and citizenship
    df = merge_quotes_wikidata(Wikidata_speakers, Wikidata_countries, df)

    # URLS DATA EXTRACTION
    df = Chunk_url_extract(df, matchers)
    tot_length = len(df)

    return df, tot_length
"""