
# Libraries to import
import pandas as pd
import numpy as np
import matplotlib as matplot
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pickle
from scipy.stats import ttest_ind
import math

# Supress warnings
import warnings
warnings.filterwarnings("ignore")


#interactive plots
import plotly.express as px
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
import bar_chart_race as bcr

# Networkx
import networkx as nx
from pyvis import network
from pyvis.network import Network
import matplotlib.image as mpimg

### Import colors of interest

palette_gender =['#529dc8', '#cc78bc'] #Male, Female
sns.set_palette(sns.color_palette(palette_gender))
sns.color_palette(palette_gender) #to visualize colors

palette_countries = ['#E5B25D', '#c13639', '#029e73'] #UK, USA, SA
sns.set_palette(sns.color_palette(palette_countries))
sns.color_palette(palette_countries) #to visualize colors

palette_media = ['#7D858D', '#dc6e57'] #Respected, Popular
sns.set_palette(sns.color_palette(palette_media))
sns.color_palette(palette_media) #to visualize colors

palette_cat = ['#7570b3', '#e7298a', '#90BE6D', '#ece133', '#F48C06', '#023E8A', '#442220'] #order whatever
sns.set_palette(sns.color_palette(palette_cat))


### Functions for part 1 of the data story

def add_female_percentage(df_origin_media):
    """
        Function to add the percentage of quotes depending on `gender` and `media_country`
    :param df: dataframe 
    """ 
    all_newspaper_countries = df_origin_media.groupby(['media_country'])['count'].sum().to_frame(name="Total").sort_values(['Total'],ascending=False).reset_index()
    df_origin_media_gender = df_origin_media.groupby(["media_country","gender"])['count'].sum().to_frame(name="count").sort_values(['count'],ascending=False).reset_index()
    df_female = df_origin_media_gender[df_origin_media_gender['gender'] == 'Female'].reset_index(drop=True)
    df_female_prop = df_female.merge(all_newspaper_countries, on='media_country')
    df_female_prop['Female %'] = df_female_prop['count']/df_female_prop['Total']*100
    df_female_prop = df_female_prop.sort_values('Female %', ascending = False)
    
    return df_origin_media_gender, df_female_prop

def plot_quotes_media_country(df_media_country):
    """
        Function to plot the number of quotes depending on `gender` and `media_country`
    :param df: dataframe 
    """    
    f = plt.figure(figsize=(12,6))
    ax = sns.barplot(data=df_media_country.sort_values(['count'],ascending=False), x='media_country',y='count', hue='gender')
    plt.xlabel("Media's country")
    plt.ylabel('Number of quotes')
    plt.yscale('log')
    plt.title("Number of quotes depending on gender and media's country for all years")
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45,  horizontalalignment='right')
    
    
def create_df_age_range(df):
    df_age_range = df.groupby(['media_country','gender', 'age_range']).quoteID.count().to_frame(name='count').reset_index()
    df_age_range.sort_values(['media_country','gender','age_range'], inplace=True)
    df_total_per_media_country = df_age_range.groupby(['media_country', 'gender'])["count"].sum().to_frame(name="Total").reset_index()
    df_age_range = df_age_range.merge(df_total_per_media_country, on=['media_country','gender'])
    df_age_range['Proportion']  = (df_age_range['count']/df_age_range['Total'])*100
    return df_age_range


def plot_quotes_age(df, age_threshold):
    """
        Function to plot the number of quotes depending on `age_range` and `gender`
    :param df: dataframe
    :param age_threshold: consider only speakers with an age smaller than `age_threshold`
    """
    list_countries = ['United Kingdom','United States of America','South Africa']
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,8), sharey=True)
    
    sns.barplot(data=df[df["gender"]=="Male"], x='age_range',y='Proportion', hue='media_country', hue_order=list_countries, ax=axes[1], palette=palette_countries)
    sns.barplot(data=df[df["gender"]=="Female"], x='age_range',y='Proportion', hue='media_country',  hue_order=list_countries, ax=axes[0], palette=palette_countries)
    
    
    axes[0].set_title('Percentage of female quotes per age range and country', size=25)
    axes[0].tick_params(axis='both', which='major', labelsize=15)
    axes[1].set_title('Percentage of male quotes per age range and country', size=25)
    axes[1].tick_params(axis='both', which='major', labelsize=15)
    
    axes[0].set_xlabel('Age intervals')
    axes[0].set_ylabel('Percentage of quotes ')
    axes[1].set_xlabel('Age intervals')
    axes[1].set_ylabel('')
    axes[0].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout(pad=5)

def create_df_prop_year(df_list):
    """
        Function to compute the proportion of female speakers
    param df_list: list of dataframes
    """
    df_all_years = pd.DataFrame()
    for df in df_list:
        df_prop_year = df.groupby(['media_country','gender']).quoteID.count().to_frame(name='count').reset_index()
        df_prop_year.sort_values(['media_country','gender'], inplace=True)
        df_total_per_media_country = df_prop_year.groupby(['media_country'])["count"].sum().to_frame(name="Total").reset_index()
        df_prop_year = df_prop_year.merge(df_total_per_media_country, on=['media_country'])
        df_prop_year['Proportion']  = (df_prop_year['count']/df_prop_year['Total'])*100
        df_prop_year['year'] = df['quoteID'].iloc[0][0:4]
        df_all_years = df_all_years.append(df_prop_year)
    return df_all_years.reset_index(drop=True)

def create_df_categories_per_gender(df):
    df_tags = df.groupby(["media_country","tags","gender"]).quoteID.count().to_frame(name="count").sort_values(['count'],ascending=False).reset_index()
    df_total_tags= df_tags.groupby(['media_country', 'gender'])["count"].sum().to_frame(name="Total").reset_index()
    df_tags = df_tags.merge(df_total_tags, on=['media_country','gender'])
    df_tags['Proportion']  = (df_tags['count']/df_tags['Total'])*100  
    return df_tags



def plot_quotes_categories_per_gender(df_tags):
    """
        Function to plot the number of quotes depending on `tags` and `gender`
    :param df: dataframe 
    """
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
    #f = plt.figure(figsize=(10,4))
    sns.barplot(data=df_tags[df_tags["gender"]=="Male"], x='tags',y='Proportion', hue='media_country', ax=axes[0])
    sns.barplot(data=df_tags[df_tags["gender"]=="Female"], x='tags',y='Proportion', hue='media_country', ax=axes[1])
    
    axes[0].set_title('Percentage of male quotes', size=25)
    axes[0].tick_params(axis='both', which='major', labelsize=15)
    axes[1].set_title('Percentage of female quotes', size=25)
    axes[1].tick_params(axis='both', which='major', labelsize=15)
    axes[0].set_xlabel('Categories')
    axes[0].set_ylabel('Percentage of quotes')
    axes[1].set_xlabel('Categories')
    axes[1].set_ylabel('')
    axes[0].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout(pad=5)


def create_df_categories_per_country(df):
    df_tags = df.groupby(["media_country","tags","gender"]).quoteID.count().to_frame(name="count").sort_values(['count'],ascending=False).reset_index()
    df_total_tags= df_tags.groupby(['media_country'])["count"].sum().to_frame(name="Total").reset_index()
    df_tags = df_tags.merge(df_total_tags, on=['media_country'])
    df_tags['Proportion']  = (df_tags['count']/df_tags['Total'])*100  
    return df_tags


def plot_quotes_categories_per_country(df_tags):
    """
        Function to plot the number of quotes depending on `tags` and `gender`
    :param df: dataframe 
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18,7), sharey=True)
    countries = sorted(df_tags.media_country.unique())
    sns.barplot(data=df_tags[df_tags["media_country"]==countries[0]], x='tags',y='Proportion', hue='gender', ax=axes[0])
    sns.barplot(data=df_tags[df_tags["media_country"]==countries[1]], x='tags',y='Proportion', hue='gender', ax=axes[1])
    sns.barplot(data=df_tags[df_tags["media_country"]==countries[2]], x='tags',y='Proportion', hue='gender', ax=axes[2])
    
    axes[0].set_title(countries[0] + '\nPercentage of quotes', size=15)
    axes[0].tick_params(axis='both', which='major', labelsize=15)
    axes[1].set_title(countries[1] + '\nPercentage of quotes', size=15)
    axes[1].tick_params(axis='both', which='major', labelsize=15)
    axes[2].set_title(countries[2] + '\nPercentage of quotes', size=15)
    axes[2].tick_params(axis='both', which='major', labelsize=15)
    axes[0].set_xlabel('Categories')
    axes[0].set_ylabel('Percentage of quotes depending on gender', size=12)
    axes[1].set_xlabel('Categories')
    axes[1].set_ylabel('')
    axes[2].set_xlabel('Categories')
    axes[2].set_ylabel('')
    axes[0].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='x', rotation=45)
    axes[2].tick_params(axis='x', rotation=45)
    plt.tight_layout(pad=5)
    

### Enf of functions for part 1 of the data story

### Functions for part 2 

def extract_media_interest(df, PATHYEAR, FILEYEAR, top_5_media, respected = True):
    """
        
    """
    df_expl_sitenames = df.explode(["sitenames"])
    df_expl_tags = df.drop(columns = ['speaker', 'qids', 'quoteID', 'quotation', 'date', 'urls', 'sitenames',
       'domain', 'gender', 'citizenship', 'Description',
       'date_of_birth', 'media_country_qid', 'numOcurrences', 'age',
       'age_range', 'Continent', 'quotation_length', 'media_country']).explode(["tags"])

    df_expl_sitenames["tags"] = df_expl_tags
    # Extract media of interest
    df_media = df_expl_sitenames[df_expl_sitenames["sitenames"].isin(top_5_media)]

    
    # Drop columns we do not wish to analyse
    df_media.drop(columns = [ 'date', 'urls', 
       'domain', 'Description',
       'date_of_birth', 'media_country_qid', 'numOcurrences',
         "media_country"], inplace = True)
    if respected:
        with open(PATHYEAR + f'M3_df_{FILEYEAR[12:16]}_respected_media.pkl', 'wb') as output:
            pickle.dump(df_media, output)
    else:
        with open(PATHYEAR + f'M3_df_{FILEYEAR[12:16]}_popular_media.pkl', 'wb') as output:
            pickle.dump(df_media, output)
    return df_media


# This function is used in order to add some transparency to the colors 
def make_rgb_transparent(rgb, bg_rgb, alpha):
    return tuple([alpha * c1 + (1 - alpha) * c2
            for (c1, c2) in zip(rgb, bg_rgb)])



def count_by_gender_without_occurences(df):
    """
        Function compute the number of quotes depending on `gender`
    :param df: dataframe 
    :return gender_count: dataframe of the number of quotes for one year
    """
    gender_count = df.groupby(by=['gender'])["speaker"].count().to_frame().T
    return gender_count


def gather_all_years_to_one_df(df_list):
    """
        Function to merge all the years in one dataframe
    :param df: list of Dataframes 
    :return gender_count_all_years: dataframe of the number of quotes for all the years 
    :return year_list: list of years (int)
    """
    gender_list = []
    year_list = []
    for df in df_list:
        year = df['quoteID'].iloc[0][0:4]
        gender_count = count_by_gender_without_occurences(df)
        gender_list.append(gender_count)
        year_list.append(int(year))
    gender_count_all_years = pd.concat(gender_list)
    return gender_count_all_years, year_list


def gender_all_years_extension(df_list):
    """
        Function to add columns with the relative number of quotes for both gender for all the Dataframes in `df_list`
    :param df_list: list of Dataframes 
    :return gender_all_years: DataFrame with added columns `% Female/Male` and the `year`
    """
    gender_all_years, year_list = gather_all_years_to_one_df(df_list)
    gender_all_years['percentage_female'] = gender_all_years['Female']/(gender_all_years['Female'] + gender_all_years['Male'])
    gender_all_years['percentage_male'] = gender_all_years['Male']/(gender_all_years['Female'] + gender_all_years['Male'])
    gender_all_years['year'] = year_list
    return gender_all_years


def plot_gender_all_years(gender_all_years, type_media = "respected"):
    """
        Function to plot the proportion of quotes depending on `gender`
    param gender_all_years: data frame with percentage of males/females
    param type_of_media: String used for the title of the plot in order to know whether respected media or popular
    """       
    fig2 = gender_all_years[["percentage_male","percentage_female"]].plot(kind='bar', title=f'Percentage of quotations per gender for the top 5 {type_media} media', rot=0, xlabel='Years', ylabel='% of quotations', figsize=(16,6))
    
    
    
def append_all_df(df_list, columns, with_year = False):
    df_appended = pd.DataFrame(columns = columns)
    for df in df_list:
        if with_year:
            year = df.iloc[0].quoteID[:4]
            df["Year"] = year
        df_appended = df_appended.append(df[columns])
    return df_appended


def create_df_sitenames_proportion(df, threshold_tot = 1000):
    """
        The function creates the proportion of female/male for each sitename
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    
    df_site = df.groupby(["sitenames","gender"]).quoteID.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
    df_site_tot = df_site.groupby(['sitenames']).Count.sum().to_frame(name="Total").reset_index()
    df_site = df_site.merge(df_site_tot, on='sitenames')
    df_site = df_site[df_site.Total > threshold_tot]
    df_site['Proportion']  = (df_site['Count']/df_site['Total'])*100
    year = df.iloc[0]["quoteID"][0:4]
    df_site["Year"] = year
    return df_site

def loop_all_sitenames_proportion(df_list):
    df_all_sites = pd.DataFrame(columns=['sitenames', 'gender', 'Count', 'Total', 'Proportion', 'Year'], dtype='object')
    for df in df_list:
        df_site = create_df_sitenames_proportion(df)
        df_all_sites = df_all_sites.append(df_site)
        
    return df_all_sites



def create_df_age_proportion(df, threshold_tot = 1000):
    """
            Function to compute the distribution of age for each gender
        param df: dataframe with at least "age_range" and "gender" column
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    
    df_age_range = df.groupby(["age_range","gender"]).age_range.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
    df_age_range_tot = df_age_range.groupby(['gender']).Count.sum().to_frame(name="Total").reset_index()
    df_age_range = df_age_range.merge(df_age_range_tot, on='gender')
    df_age_range = df_age_range[df_age_range.Total > threshold_tot]
    df_age_range['Proportion']  = (df_age_range['Count']/df_age_range['Total'])*100
    return df_age_range



def CI_95_percent(df):
    
    ci95_hi = []
    ci95_lo = []
    # Extract statistics of interest for quotation length 
    df_stats = df.groupby(['gender',"Year"])['quotation_length'].agg(['mean', 'count', 'std'])
    for i in df_stats.index:
        mean, count, std = df_stats.loc[i]
        ci95_hi.append(mean + 1.96*std/math.sqrt(count))
        ci95_lo.append(mean - 1.96*std/math.sqrt(count))
    
    df_stats['ci95_hi'] = ci95_hi
    df_stats['ci95_lo'] = ci95_lo
    return df_stats


def create_df_media(df):
    df_sitenames_explode = df.explode("sitenames")
    df_sitenames = df_sitenames_explode.groupby(["sitenames","gender"]).quoteID.count().to_frame(name="count").sort_values(['count'],ascending=False).reset_index()
    return df_sitenames


def plot_quotes_media(df_sitenames, threshold_nber, year): 
    """
        Function to plot the number of quotes depending on `gender` and `media_country`
    :param df: dataframe 
    """
    f = plt.figure(figsize=(18,6))
    ax = sns.barplot(data=df_sitenames[df_sitenames['count']>threshold_nber], x='sitenames',y='count', hue='gender')
    locs, labels = plt.xticks();
    plt.setp(labels, rotation=90);
    plt.ylabel('Number of quotes')
    plt.title("Number of quotes depending on gender and media's country for the year "+year)
    
    
def loop_media_gender(df_list):
    """
        Function that loops a list of df and outputs plots with the number of quotes based on gender depending on media
        param df_list: list of dataframes
    """
    for df in df_list:
        year = df['quoteID'].iloc[0][0:4]
        df_sitenames = create_df_media(df)
        plot_quotes_media(df_sitenames, threshold_nber=1, year =year)
        
        
def clean_citizenship(df, list_code_words, list_names):
    """
        Function to rename citizenship where the data was strangely named. For eg. Americans --> United States of America
        
        param df: dataframe with all citizenships including those needed to be changed
        param list_code_words:list with code words that need to be changed
        param list_names: list of strings that will be used to replace the list_code_words (Note: these two should be of equal length)
    """
    for codeword, name in zip(list_code_words, list_names):
        df.loc[df['citizenship'].str.contains(codeword, case=False), 'citizenship'] = name
    return df




def create_df_citizenship_proportion(df, threshold_tot = 1000, with_year = False):
    """
            Function to compute the proportion of females/males within a citizenship
        param df: data frame
        param threshold_tot: Keep only media with at least this number of quotes available
        param with_year: Boolean which indicates wheter or not we group by the years
    """
    if with_year:
            df_citizen = df.groupby(["citizenship","gender", "Year"]).citizenship.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
            df_citizen_tot = df_citizen.groupby(['citizenship', "Year"]).Count.sum().to_frame(name="Total").reset_index()
            df_citizen = df_citizen.merge(df_citizen_tot, on=['citizenship', 'Year'])
    else:
        df_citizen = df.groupby(["citizenship","gender"]).citizenship.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
        df_tot = df_citizen.groupby(['citizenship', "citizenship"]).Count.sum().to_frame(name="Total").reset_index()
        df_citizen = df.merge(df_tot, on=['citizenship'])
    df_citizen = df_citizen[df_citizen.Total > threshold_tot]
    df_citizen['Proportion']  = (df_citizen['Count']/df_citizen['Total'])*100
    

    return df_citizen
    
        
def create_df_categories_proportion(df, threshold_tot = 1000):
    """
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    df_explode = df.explode("tags")
    df_category = df_explode.groupby(["tags","gender"]).quoteID.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
    df_category_tot = df_category.groupby(['tags']).Count.sum().to_frame(name="Total").reset_index()
    df_category = df_category.merge(df_category_tot, on='tags')
    df_category = df_category[df_category.Total > threshold_tot]
    df_category['Proportion']  = (df_category['Count']/df_category['Total'])*100
    year = df.iloc[0]["quoteID"][0:4]
    df_category["Year"] = year
    return df_category

def loop_all_categories_proportion(df_list):
    df_all_category = pd.DataFrame(columns = ['tags', 'gender', 'Count', 'Total', 'Proportion', 'Year'], dtype='object')
    for df in df_list:
        df_category = create_df_categories_proportion(df)
        df_all_category = df_all_category.append(df_category)
        
    return df_all_category
        
def males_for_female_factor(df, media_type):
    """
        Function to compute the number of males quoted for each women quoted
    param df: dataframe containing the number of unique speaker and the gender of the speaker
    param media_type: string giving the type of media on which the function is used
    """
    
    df_male = df[df["gender"] == "Male"].reset_index()
    df_female = df[df["gender"] == "Female"].reset_index()

    df_males_for_female = df_female.copy()
    df_males_for_female["Factor"] = df_male["unique_speaker_per_tag"] / df_female["unique_speaker_per_tag"]
    df_males_for_female.drop(columns = ["index", "gender", "unique_speaker_per_tag"], inplace = True)
    df_males_for_female["type_of_media"] = f"{media_type}"
    return df_males_for_female




def df_proportion_category_unique_speaker(df, threshold_tot = 1000, with_year = False):
    """
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    if with_year:
            df_tot = df.groupby(['gender', "Year"]).unique_speaker_per_tag.sum().to_frame(name="Total").reset_index()
            df = df.merge(df_tot, on=['gender', 'Year'])
    else:
        df_tot = df.groupby(['gender']).unique_speaker_per_tag.sum().to_frame(name="Total").reset_index()
        df = df.merge(df_tot, on=['gender'])
    df = df[df.Total > threshold_tot]
    df['Proportion']  = (df['unique_speaker_per_tag']/df['Total'])*100
    return df



def df_proportion_citiz_unique_speaker(df, threshold_tot = 1000, with_year = False):
    """
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    if with_year:
            df_tot = df.groupby(['gender', "Year"]).unique_speaker_per_citiz.sum().to_frame(name="Total").reset_index()
            df = df.merge(df_tot, on=['gender', 'Year'])
    else:
        df_tot = df.groupby(['gender']).unique_speaker_per_citiz.sum().to_frame(name="Total").reset_index()
        df = df.merge(df_tot, on=['gender'])
    df = df[df.Total > threshold_tot]
    df['Proportion']  = (df['unique_speaker_per_citiz']/df['Total'])*100
    return df


def df_proportion_citiz_unique_speaker_gender(df, threshold_tot = 10, with_year = False):
    """
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    if with_year:
            df_tot = df.groupby(['citizenship', "Year"]).unique_speaker_per_citiz.sum().to_frame(name="Total").reset_index()
            df = df.merge(df_tot, on=['citizenship', 'Year'])
    else:
        df_tot = df.groupby(['citizenship']).unique_speaker_per_citiz.sum().to_frame(name="Total").reset_index()
        df = df.merge(df_tot, on=['citizenship'])
    df = df[df.Total > threshold_tot]
    df['Proportion']  = (df['unique_speaker_per_citiz']/df['Total'])*100
    return df



def create_df_sitename_category_proportion(df, threshold_tot = 10, with_year = False):
    """
        param threshold_tot: Keep only media with at least this number of quotes available
    """
    if with_year:
        df_sitenames_category = df.groupby(["tags","gender", "Year", "sitenames"]).tags.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
        df_sitenames_category_tot = df_sitenames_category.groupby(['tags', "Year", "sitenames"]).Count.sum().to_frame(name="Total").reset_index()
        df_sitenames_category = df_sitenames_category.merge(df_sitenames_category_tot, on=['tags', 'Year', "sitenames"])
    else:
        df_sitenames_category = df.groupby(["tags","gender", "sitenames"]).tags.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
        df_tot = df_sitenames_category.groupby(['tags', "sitenames"]).Count.sum().to_frame(name="Total").reset_index()
        df_sitenames_category = df.merge(df_tot, on=['tags', "sitenames"])
    
    df_sitenames_category = df_sitenames_category[df_sitenames_category.Total > threshold_tot]
    df_sitenames_category['Proportion']  = (df_sitenames_category['Count']/df_sitenames_category['Total'])*100
    

    return df_sitenames_category

### Enf of functions for part 2