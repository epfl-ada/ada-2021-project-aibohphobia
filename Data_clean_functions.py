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
nltk.download('stopwords')
nltk.download('punkt')

### Topics in URL ###

def get_sitename(url):
    res = get_tld(url, as_object=True)
    return res.domain

def extract_name(df): 
    df['sitenames'] = np.nan
    for row in range(df.shape[0]):
        df['sitenames'][row] = [get_sitename(site) for site in df['urls'][row]] 
        
def get_domain(url):
    res = get_tld(url, as_object=True)
    return res.tld

def get_sitename(url):
    res = get_tld(url, as_object=True)
    return res.domain

def tokenize(text):
    stemmer = PorterStemmer()
    text = "".join([ch for ch in text if ch not in string.punctuation]) # get the text without punctuation
    tokens = nltk.word_tokenize(text) #Tokenizers divide strings into lists of substrings
    return " ".join([stemmer.stem(word.lower()) for word in tokens if word not in stopwords.words('english')]) #stem all words

def generalizeDictionary(matchers):
    stemmer = PorterStemmer()
    for category in matchers:
        for i in range(len(matchers[category])):
            matchers[category][i] = tokenize(matchers[category][i])
            
def getWordsFromURL(url):
    return re.compile(r'\W+',re.UNICODE).split(url)

def classify(matchers, url): #Give it an already generalized dictionary
    stemmer = PorterStemmer()
    tag_found = []
    general_url = [tokenize(x) for x in getWordsFromURL(url)]
    for category in matchers:
        for i in range(len(matchers[category])):
            match = matchers[category][i]
            if match in general_url:
                tag_found.append(category)
    return tag_found # or you can "return None"


### Cleaning data functions ###

def Remove_none_speakers(chunk):
    chunk = chunk.drop(chunk[chunk['speaker']=='None'].index)
    chunk = chunk.reset_index(drop=True)
    return chunk 

def Remove_none_unique_ids(chunk):
    if not(chunk.quoteID.is_unique):
        chunk = chunk.drop_duplicates(subset=['quoteID'], keep='first')
    return chunk 

def Remove_empty_quotes(chunk):
    chunk = chunk.drop(chunk[chunk["quotation"].isna() | chunk["quotation"].isnull()].index)
    chunk = chunk.reset_index(drop=True)
    return chunk 

def Remove_low_proba(chunk, threshold):
    #Gather the first probability for each row
    string_probas, nber_probas = [], []
    string_probas = [chunk['probas'][i][0][1] for i in chunk.index]
    nber_probas = list(map(float, string_probas))
    series_probas = pd.Series(nber_probas, dtype='float64', index=chunk.index)
    
    #Check if the probability is larger than the threshold, if not remove corresponding index
    chunk = chunk.drop(series_probas[series_probas < threshold].index)
    chunk = chunk.reset_index(drop=True)    
    return chunk 

def Chunk_url_extract(chunk, matchers):
    tags_column = [] # List of lists. Each list inside corresponds to a row. Will become the 'tag' column
    site_column = []
    domain_column = []
    for index, row in chunk.iterrows():
            tags = [] #tags for all the urls in that row
            domains = []
            sitenames = []
            for url in row['urls']:
                #Extract data
                tld = get_domain(url)
                name = get_sitename(url)
                categories = classify(matchers, url)
                #Append data
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


### Preprocess whole chunk ###

def process_chunk_complete(chunk, threshold_proba, matchers):
    print(f'Processing chunk with {len(chunk)} rows')
    #DATA CLEANING
    #Remove None speakers
    chunk = Remove_none_speakers(chunk)
    
    #Remove none unique ids and keep the first one
    chunk = Remove_none_unique_ids(chunk)
        
    #Remove nan or empty quotes 
    chunk = Remove_empty_quotes(chunk)

    #Remove speakers for which probability is lower than a threshold
    chunk = Remove_low_proba(chunk, threshold_proba)
    
    #URLS DATA EXTRACTION
    chunk = Chunk_url_extract(chunk, matchers)
    
    tot_length = len(chunk)
    return chunk, tot_length
