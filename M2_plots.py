import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats import diagnostic
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf




from M2_cleaning import *

#Settings for the plots 
sns.set_style("ticks")
colors= sns.color_palette('colorblind')
plt.rc('xtick', labelsize=14) 
plt.rc('ytick', labelsize=14) 
plt.rc('axes', titlesize=18)
plt.rc('axes', labelsize=13)
plt.rcParams['ytick.major.size'] = 7
plt.rcParams['ytick.minor.size'] = 6
sns.set_style("darkgrid", {'axes.grid' : False, 'ytick.left': True, 'xtick.bottom': True})


##### Functions to compute/calculate #####
### Number of quotes per gender    
def count_by_gender(df):
    """
        Function compute the number of quotes depending on `gender`
    :param df: dataframe 
    :return gender_count: dataframe of the number of quotes for one year
    """
    year = df['quoteID'][0][0:4]
    gender_count = df.groupby(by=['gender'])['quotation'].count().to_frame(name=year).T
    return gender_count

def gather_all_years_to_one_df(df_list):
    """
        Function to merge all the years in one dataframe
    :param df: list of Dataframes 
    :return gender_count_all_years: dataframe of the number of quotes for all the years 
    :return year_list: list of years (integer format)
    """
    gender_list = []
    year_list = []
    for df in df_list:
        year = df['quoteID'][0][0:4]
        gender_count = count_by_gender(df)
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

### Number of quotes per age 
def dateofbirth_to_timestamp(df):
    """
        Function to transform the date of birth to a timestamp format
    :param df: dataframe 
    :return: dataframe with transformed columns `date_of_birth`
    """
    df['date_of_birth'] = extract_element_from_series(df['date_of_birth'])
    df['date_of_birth'] = df['date_of_birth'].replace(to_replace='[\+Z]',value='', regex=True)                                                                              
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    return df

def compute_age(df):
    """
        Function to compute the age from the `date_of_birth` and today's date
    :param df: dataframe
    :return: dataframe with added column `age`
    """
    quote_date = pd.to_datetime(df["quoteID"].apply(lambda x: x[:10]), format='%Y-%m-%d', errors='coerce') #to replace with date column in the future
    df['age'] = (quote_date.dt.year - df.date_of_birth.dt.year) - ((quote_date.dt.month - df.date_of_birth.dt.month) < 0)
    return df

def compute_age_range(df, bins):
    """
        Function to compute the age range in intervals of 10 years
    :param df: dataframe
    :param bins: array to define the length if intervals 
    :return: dataframe with added column `age_range`
    """
    df["age_range"] = pd.cut(df["age"], bins)
    return df

def compute_age_and_agerange(df, bins):
    """
        Function to call functions computing age and age range
    :param df: dataframe
    :param bins: array to define the length if intervals
    :return: dataframe with added columns `age` and `age_range`
    """
    df = dateofbirth_to_timestamp(df)
    df = compute_age(df)
    df = compute_age_range(df, bins)
    return df

### Number of quotes per continent 
def add_continent(df, countries_to_continent):
    """
        Function to associate the corresponding continent the country of citizenship
    :param df: dataframe
    :param countries_to_continent: dataframe with all the countries and their corresponding continent
    :return: column `Continent`
    """
    df = pd.merge(df, countries_to_continent, left_on='citizenship', right_on='Country', copy=False)
    df = df.drop('Country', axis=1)
    return df["Continent"]

### Number of quotes per categories
def transform_tags(df):
    """
        Function to transform the nested tags to a usable string, keeping only the first tag if several
    :param df: dataframe
    :return: array of string of the tags
    """
    col_tags = []
    for i in range(len(df)):
        array = df['tags'][i]
        tags = [var for var in array if var]
        if tags : 
            tags = tags[0][0]
        else :
            tags = 'undefined'
        col_tags.append(tags)
    return col_tags

### Quotes length 
def compute_quotation_length(df):
    """
        Function to compute the length of the quote 
    :param df: dataframe
    :return: dataframe with added column `quotation_length`
    """
    df['quotation_length'] = df['quotation'].str.len()
    return df 

### compute_country_from_qid
def compute_country_from_qid(df, qids_to_country):
    """
        Function to compute the name of the countries based on their qid
    :param df: dataframe
    :return: dataframe with added column `media_country`
    """
    df["media_country_qid"] = extract_element_from_series(df['media_country_qid'])
    df = pd.merge(df, qids_to_country, left_on = 'media_country_qid', right_on='QID', how='left').drop('QID', axis=1)
    df = df.rename(columns = {"Country": "media_country"})
    return df["media_country"]

##### Perform any t-test #####
def perform_t_test(Series1,Series2):
    """
        Function to perform at t-test between two distributions (Null hypothesis stating that the two independant distributions have equal means)
    :param Series1: Series of values 
    :return pvalue: pvalue of the t-test
    """
    stattest, pvalue = stats.ttest_ind(Series1,Series2, equal_var = True)
    return pvalue

def perform_linear_regression(outcome, pred, df):
    """
        Function to compute the linear regression using the formula: outcome ~ pred
        param outcome: outcome of the linear model
        param pred: predictor of the linear model
        return: results (df containing coefficients, standard deviations and pvalues)
    """
    # Declares the model
    mod = smf.ols(formula=outcome +'~'+pred, data=df)
    np.random.seed(2) # Fits the model (find the optimal coefficients, adding a random seed ensures consistency)
    res = mod.fit()
    print(res.summary())

    # coefficients
    coeff = pd.Series(res.params.values)
    m = res.params.values[1]

    # p-values
    p_value0 = float(res.pvalues[0])
    p_value1 = float(res.pvalues[1])
    p_values = [p_value0, p_value1]
    
    # standard errors
    std_errors = pd.Series(res.bse.values)
    
    #results 
    results = pd.DataFrame()
    results['coeff'] = coeff
    results['std'] = std_errors
    results['p_value'] = p_values
    results.rename(index={0: "b", 1: "m"})
    return results


##### Keep only the first category tag per url #####

def keep_first_tag(df):
    for row_nbr in range(len(df['tags'])):
        row = df['tags'][row_nbr]
        for tag_nbr in range(len(row)):
            tag_list = row[tag_nbr]
            if len(tag_list)>1: #when there are multiple tags for one site
                tag_to_keep = [tag_list[0]] #keep only the first one
                df['tags'][row_nbr][tag_nbr] = tag_to_keep 
    
    return df

##### Create a datatframe with the proportion of genders in each category #####

def create_df_categories_proportion(df):
    df_tags_explode = df.explode("tags").explode("tags")
    df_tags = df_tags_explode.groupby(["tags","gender"]).quoteID.count().to_frame(name="Count").sort_values(['Count'],ascending=False).reset_index()
    df_total_per_cat = df_tags.groupby(['tags']).Count.sum().to_frame(name="Total").reset_index()
    df_tags = df_tags.merge(df_total_per_cat, on='tags')
    df_tags['Proportion']  = (df_tags['Count']/df_tags['Total'])*100
    return df_tags


##### Plots functions #####
### Plot number of quotes per gender 

def plot_gender_all_years(gender_all_years):
    """
        Function to plot the number of quotes depending on `gender`
    :param gender_all_years: data frame with percentage of males/females
    """    
    
    fig1 = (gender_all_years[['Male','Female']]/1000000).plot(kind='bar', title='Number of quotations depending on the gender in absolute value for each year', rot=0, xlabel='Years', ylabel='Number of quotations \n [in Millions]', figsize=(16,6))
    fig2 = gender_all_years[['percentage_male','percentage_female']].plot(kind='bar', title='Number of quotations depending on the gender in % for each year', rot=0, xlabel='Years', ylabel='% of quotations', figsize=(16,6))

### Plot number of quotes per age 
def plot_quotes_age(df, age_threshold):
    """
        Function to plot the number of quotes depending on `age_range` and `gender`
    :param df: dataframe
    :param age_threshold: consider only speakers with an age smaller than `age_threshold`
    """
    f = plt.figure(figsize=(16,6))
    ax = sns.countplot(data=df[df["age"]<age_threshold], x='age_range', hue ='gender')
    plt.xlabel('Age intervals')
    plt.ylabel('Number of quotes')
    year = df['quoteID'][0][0:4]
    plt.title('Number of quotes depending on age and gender for the year '+ year)
    #labels = ['[0,10]','[10,20]','[20,30]','[30,40]','[50,60]','[60,70]','[70,80]','[80,90]','[90,100]']
    #ax.set_xticklabels(labels)

### Plot number of quotes per country    
def plot_quotes_country(df, threshold_nber):
    """
        Function to plot the number of quotes depending on `citizenship` and `gender`
    :param df: dataframe
    :param threshold_nber: consider only countries of citizenship for which there is at least `threshold_nber` of quotes
    """
    df_citizenship_count = df.groupby(['gender', 'citizenship'])['quoteID'].count().sort_values(ascending=False).to_frame(name='count').reset_index()
    df_citizenship_count = df_citizenship_count[df_citizenship_count['count']>threshold_nber]
    
    f = plt.figure(figsize=(18,6))
    ax = sns.barplot(data=df_citizenship_count, x='citizenship',y='count', hue='gender')
    plt.xlabel('Citizenship')
    plt.ylabel('Number of quotes')
    plt.legend(loc = 'upper right')
    year = df['quoteID'][0][0:4]
    plt.title('Number of quotes above '+ str(threshold_nber) +' depending on gender and citizenship for the year '+year)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    ax.set_yscale('log')
    
### Plot number of quotes per continent  
def plot_quotes_continent(df):
    """
        Function to plot the number of quotes depending on `continent` and `gender`
    :param df: dataframe
    """
    f = plt.figure(figsize=(12,6))
    ax = sns.countplot(data=df, x='Continent', hue='gender', order=df['Continent'].value_counts().index)
    plt.xlabel('Continent')
    plt.ylabel('Number of quotes')
    year = df['quoteID'][0][0:4]
    plt.title('Number of quotes depending on gender and continent for the year '+year)
    
### Plot number of quotes per media
def plot_quotes_media(df):
    """
        Function to plot the number of quotes depending on `sitenames` and `gender`
    :param df: dataframe
    """
    f = plt.figure(figsize=(14,6))
    ax = sns.countplot(data=df, x='sitenames', hue='gender', order=df['sitenames'].value_counts().index)
    plt.xlabel('Media')
    plt.ylabel('Number of quotes')
    plt.title('Number of quotes depending on gender and media')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45,  horizontalalignment='right')

### Plot number of quotes per categories 
def plot_quotes_categories(df):
    """
        Function to plot the number of quotes depending on `tags` and `gender`
    :param df: dataframe 
    """
    f = plt.figure(figsize=(14,6))
    ax = sns.countplot(data=df, x='tags', hue='gender', order=df['tags'].value_counts().index)
    plt.xlabel('Category')
    plt.ylabel('Number of quotes')
    ax.set_yscale('log')
    year = df['quoteID'][0][0:4]
    plt.title('Number of quotes depending on gender and media for the year '+year)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45,  horizontalalignment='right')
    
def plot_quotes_categories_proportion(df_tags):
    """
        Function to plot the number of quotes depending on `tags` and `gender`
    :param df: dataframe 
    """
    #create plot
    f = plt.figure(figsize=(18,6))
    ax = sns.barplot(data=df_tags, x='tags',y='Proportion', hue='gender')
    plt.xlabel('Category')
    plt.ylabel('Proportion of quotes')
    plt.title('Proporion of quotes between genders, per category')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45,  horizontalalignment='right')

### Plot length of quotes
def plot_quotes_distribution(df):
    """
        Function to plot the distribution of the quotes length depending on `gender`
    :param df: dataframe
    """ 
    f = plt.figure(figsize=(14,6))
    f = sns.histplot(data = df, y='quotation_length', hue='gender', bins=200, alpha=0.8, log_scale = [True,False], 
                     hue_order = ['Female', 'Male'], palette=[colors[1], colors[0]])
    #f = sns.histplot(y=df.loc[df['gender'] == 'Female']['quotation'].str.len(), bins=200, alpha=0.8, color=colors[1], label = 'Female')
    plt.ylabel('Quotation length')
    year = df['quoteID'][0][0:4]
    plt.title('Quotation length distribution per gender for the year '+year)
    plt.show()
    
def plot_avg_quotes_length(df, conf_int):
    """
        Function to plot average length of quotes and confidence intervals depending on `gender`
    :param df: dataframe 
    :param conf_int: confidence interval for the plot
    """
    year = df['quoteID'][0][0:4]
    f = plt.figure(figsize=(8,10))
    sns.catplot(data = df, x='gender', y='quotation_length', kind='bar', height=5, aspect=0.8, ci=conf_int)
    plt.title('Average quotation length depending on gender for the year '+ year)
    plt.ylabel('Quotation length')
    plt.tight_layout()
    plt.ylim(113,126)
    plt.show()

    
def plot_quotes_media_country(df):
    """
        Function to plot the number of quotes depending on `gender` and `media_country`
    :param df: dataframe 
    """
    f = plt.figure(figsize=(12,6))
    ax = sns.countplot(data=df, x='media_country', hue='gender', order=df['media_country'].value_counts().index)
    plt.xlabel("Top media's country")
    plt.ylabel('Number of quotes')
    year = df['quoteID'][0][0:4]
    plt.title("Number of quotes depending on gender and media's country for the year "+year)