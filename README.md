# Underrepresentation of females in media: a myth or a truth?

## Contents

* [Abstract](#abstract)
* [The dataset](#the-dataset)
* [Research questions](#research-questions)
* [Additional datasets](#additional-datasets)
* [Methods](#methods)
* [Libraries of interest](#libraries-of-interest)
* [Timeline](#timeline)
* [Team organization](#team-organization)
* [References](#references)

## Project directory

|__ M2_pre_processing.ipynb\
|__ M2_cleaning.py\
|__ Milestone_2.ipynb\
|__ M2_media_wikidata.py\
|__ M2_plots.py

**M2_pre_processing.ipynb**: Notebook to clean data and organize it for the data analysis.\
**M2_cleaning.py**: script containing functions for the data cleaning that are called as a module in `M2_pre_processing.ipynb`.\
**M2_initial_analysis.ipynb**: Notebook containing the analysis done on the cleaned data.\
**M2_media_wikidata.py**: script containing functions for extracting data through the wikidata API. Are called as a module in `M2_pre_processing.ipynb` and `M2_initial_analysis.ipynb`.\
**M2_plots.py**: script containing functions called as a module during the data analysis in `Milestone_2.ipynb`.\


## Abstract

Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, from politics, entertainment to the workplace, they have historically been underrepresented, including in mainstream media. [Studies](https://www.tandfonline.com/doi/full/10.1080/23257962.2016.1260445) have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to explore whether media coverage gives the same possibilities regardless of gender.
The goal is to highlight possible trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains and subjects are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. The difference between countries, year and media source will also be analysed as well as the impact of such factors on the length and frequency of female quotes.



## The dataset

The dataset contains the quotes from the Quotebank [dataset](https://zenodo.org/record/4277311) for the years 2016-2020. For each quote, this dataset includes information on the speaker (along with their qid from [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)), probability of being the speaker as well as the source of the quote.

Once the data has been cleaned for each year, it is saved on this [drive](https://drive.google.com/drive/folders/1bP67GGJyPXD7bCr5c6f7O2fM40AWpXJN?usp=sharing). The folder also contains a `README_DRIVE.md` precising the data that can be found.

## Research questions

Throughout this study we aim to answer a main question: "Is the representation equal between males and females in media?". In order to answer this complex question, we have identified the following research questions which will guide us in the project: 

- How does the distribution of quotes based on gender vary across countries?
- How does the distribution of quotes based on gender vary across topics?
- How does the distribution of quotes between genders evolve in time, geographically and thematically?
- Is there a tendency in each category for a males to have longer quotes than females?
- Are males more likely to be quoted in highly respected media? 
- Are there any blind spots in media where females are especially neglected?
- Is there a difference in how females/males at a certain age are quoted?
- Are countries known to promote gender equality more likely to reflect this in media compared to the rest of the world ?


## Additional datasets

As we are interested in linking the quote to a geographical place, we do so by taking the geographical location of the journal.
We currently use the URL given by the QuoteBank dataset to retrieve information about the journal though the wikidata API.

We also add a dataset which countains the countries belonging to each continent in a [csv](https://github.com/dbouquin/IS_608/blob/master/NanosatDB_munging/Countries-Continents.csv) file. 

As of now we do not plan on using any additional datasets.


## Methods

**Data filtering**

In order to limit the size of the data we are working on, for each year we:
- Computed the number of occurrences of each media source (by extracting the site name from the URL)
- Selected the top 10 media as a proxy for popularity 
- Filtered the data to keep only quotes that were mentioned in the top 10 media sources

**Data cleaning:**

A function is used to clean the data in the following ways:
- Remove "None" speakers 
- Remove speakers with a probability inferior to a certain threshold (50%)
- Make sure quotes are non empty 

**Additional data extraction**

Using the URL and data from Wikidata provided, we obtain further information:
- Tags are added if the url contains specific mentions of a topic from a predefined list (e.g.: sports, business, music...)
- Using the URLs from QuoteBank, we extract features such as the country of origin from the newspaper using WikiData API
- Change QIDs to labels (e.g.: "Q31"is changed to "Belgium")
- Using the QID the speaker's nationality, date of birth and gender are found
- The age (for the speakers still alive today) is calculated at the moment of the quote
- The URL is used to query the wikidata to find the country of origin of media which cited the quote

**Initial analysis of data**

1. Comparison of number of male versus female quotes

- Overall difference in count of males versus females, over all years 
- Overall count of male versus female quotes, per year
- Overall count of male versus female quotes, per category
- Overall count of male versus female quotes, per year and per category
- Overall count of male versus female quotes, per country/geographical location
- Overall count of male versus female quotes, per year and per country/geographical location

2. Tests for statistical significance 

- Perform statistical tests to see if the difference between counts of males and females per year is statistically significant
- Perform statistical tests to see if the difference per year and per category is statistically significant
- Perform statistical tests to see if the difference per year and per location is statistically significant

**Deeper analysis**

1. Comparison of media coverage depending on gender in highly repsected media

- Define a list of "highly respected" sources, and re-filter the data to keep only the quotes that were quoted in these sources
- Compare the number of males and females that have been quoted and test for statistical significance

2. Comparison in length of quote

- Perform statistical tests to analyse whether a difference in the length of quotes is significant between years and location or category

3. Media coverage in function of age

- Group speakers into classes of age and analyse trends that can appear with respect to aforementioned criteria between genders. 

4. Provided enough time, comparison of media coverage depending on gender in most popular media

- Instead of filtering the dataset to keep only the "top k media sources", filter the quotes based on a list of most popular media sources (e.g.: most printed/bought newspapers worldwide)
- Perform the same analysis as previously



**Results**

In this part, we want to study the findings obtained during our analysis in order to formulate and present the trends or any interesting results that we might have uncovered.

Results can be presented in several ways, depending on the information that needs to be transmitted:
- For geographical trends, we could present a world map indicating the male-female difference for the countries studied. We could also add the category where females are most (or least) quoted, or mention rapidly growing categories where females are increasingly gaining floor over the years. This would give indications concerning how the media in that country represents the genders. 
- The results could also be presented by category or subject, showing how quotes are distributed amongst genders within a certain subject.
- To these visualisations, we could add extra statistics on the average length of the quote or age of the speaker.
- Finally, we could present detailed results on a few known journals (from the "highly respected" set)



## Libraries of interest

- Request: for extracting data
- Pandas: for showing the data in jupyter
- Seaborn/Matplotlib: for graphs 
- URL parser: for parsing URLS in the way we need (for eg: media information)
- Statsmodel: Statistics library for making our analysis
- Bokeh: interactive plotting for advanced visualization 
- Nltk: tokenising words and finding synonyms

## Timeline

- **12/11**: Hand in Milestone 2 having done part of the initial analysis on data (for the top 10 media sources) 
- **15/11**: Having finished the updated cleaning using additional top sites or take the most popular news as my be found on the web. We will also add more quote categories to analyse in order to increase the number of tags.
- **19/11**: Finish the basic data analysis using the visualization libraries on the complete data set. 
- **3/12**: Complete with the deeper analysis
- **17/12**: Present results on a github page with our finalised data story

## Team organization 

For the initial analysis, the tasks can be split depending on whether the analysis is done per location or per category.
For the deeper analysis, the tasks can be split into 3 parts (analysis on quote length, on age and on the highly respected set)
The data visualisation and final presentation of the results can also be divided according to the message that we want to transmit. This means that team's efforts will be dedicated in part to preparing the map, the categories and the highly repsected journals/media respectively.


### Note:

Following the results of our initial analysis, we find that changing the top 10 medias who cite the most quotes to the top 100/1000 most famous medias will bring additional/more insightful information.

### *References:
(1) -  Michelle Caswell, Alda Allina Migoni, Noah Geraci & Marika Cifor (2017) ‘To Be Able to Imagine Otherwise’: community archives and the importance of representation, Archives and Records, 38:1, 5-26, DOI: 10.1080/23257962.2016.1260445 
*


