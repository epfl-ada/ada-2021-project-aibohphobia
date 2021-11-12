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

## Project directory

|__ **M2_pre_processing.ipynb**: Notebook to clean data and organize it for the data analysis.\
|__ **M2_cleaning.py**: Script containing functions for the data cleaning that are called as a module in `M2_pre_processing.ipynb`.\
|__ **Milestone_2.ipynb**: Notebook containing the analysis done on the cleaned data.\
|__ **M2_media_wikidata.py**: Script containing functions for extracting data through the wikidata API. Are called as a module in `M2_pre_processing.ipynb` and `M2_initial_analysis.ipynb`.\
|__ **M2_plots.py**: Script containing functions called as a module during the data analysis in `Milestone_2.ipynb`

## Abstract

Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, from politics, entertainment to the workplace, they have historically been underrepresented, including in mainstream media. [Studies](https://www.tandfonline.com/doi/full/10.1080/23257962.2016.1260445) have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to explore whether media coverage gives the same possibilities regardless of gender.
The goal is to highlight possible trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains and subjects are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. The difference between countries, year and media source will also be analysed as well as the impact of such factors on the length and frequency of female quotes.



## The dataset

We use the Quotebank [dataset](https://zenodo.org/record/4277311) for the years 2016-2020. For each quote, it includes information on the speaker (along with their qid from [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)) as well as the quote source.

Once the data has been cleaned, it is saved on this [drive](https://drive.google.com/drive/folders/1bP67GGJyPXD7bCr5c6f7O2fM40AWpXJN?usp=sharing). A `README_DRIVE.md` in the folder precises the data that can be found.

## Research questions

Throughout this study we aim to answer a main question: "Is the representation equal between males and females in media?". The following questions which will guide us in the project: 

- How does the distribution of quotes based on gender vary across countries, topics, location and time?
- Do males have longer quotes than females?
- Are males more likely to be quoted in highly respected media? 
- Are there any blind spots in media where females are neglected?
- Is there a difference in how females/males at a certain age are quoted?
- Are countries known to promote gender equality more likely to reflect this in media compared to the rest of the world ?


## Additional datasets

We use the provided data from Wikidata and add a dataset which contains the countries belonging to each continent in a [csv](https://github.com/dbouquin/IS_608/blob/master/NanosatDB_munging/Countries-Continents.csv) file. 

## Methods

**Data filtering**

We limited the dataset by:
- Computed the number of occurrences of each media source (by extracting the site name from the URL)
- Selected the top 10 media as a proxy for popularity 
- Filtered the data to keep only quotes that were mentioned in the top 10 media sources

**Data cleaning:**

The data is cleaned by: 
- Removing "None" speakers 
- Removing speakers havong a low porbability (50% threshold)
- Verifying quotes are non empty 

**Additional data extraction**

Using the URL and data from Wikidata: 
- Tags are added if the URL contains words of a topic from a predefined list (e.g.: sports, business, ...)
- Using the URLs from QuoteBank, we extract features such as the country of origin from the newspaper using WikiData API
- Change QIDs to labels (e.g.: "Q31" to "Belgium")
- Using the QID the speaker's nationality, date of birth and gender are found
- The speaker age (up to 100 yrs) is calculated at the moment of the quote.

**Initial analysis of data**

1. Comparison of number of male versus female quotes
- Overall difference in count of males versus females, over all years 
- Overall count of male versus female quotes, per year, per category, per geographical location and a combination of these

2. Tests for statistical significance 
Perform statistical tests to see if the difference:
- Between counts of males and females per year is statistically significant
- Per year and per location/(resp. category) is statistically significant

**Deeper analysis**

1. Comparison of media coverage depending on gender in highly repsected media
- Define a list of "highly respected" sources, re-filter the data to keep only these sources and redo previous analysis.

2. Comparison in length of quote
- Perform statistical tests to analyse whether a difference in the length of quotes is significant between years and location or category

3. Media coverage in function of age
- Group speakers into age grpoups and analyse trends between genders. 

4. Provided enough time, comparison of media coverage depending on gender in most popular media
- Filter the quotes based on a list of most popular media sources to bring additional/more insightful information instead of filtering the dataset to keep only the "top k sources of the highest count".


**Results**

Results will be presented according to the information that needs to be transmitted:
- Geographical trends; could present a world map indicating the male-female difference for the countries studied. We could also add the category where high differences were found, or ones where proportions aremale/female seel to be chaning over the years.
- Media topics: show how quotes are distributed amongst genders within a certain subject.
- To these visualisations, we could add extra statistics on the average length of the quote or age of the speaker.
- Finally, we could present detailed results from the "highly respected sources" set.


## Timeline

- **12/11**: Hand in Milestone 2 having done part of the initial analysis on data (for the top 10 media sources) 
- **15/11**: Having finished the updated cleaning using additional top sites or take the most popular news as my be found on the web. We will also add more quote categories to analyse in order to increase the number of tags.
- **19/11**: Finish the basic data analysis using the visualization libraries on the complete data set. 
- **3/12**: Complete with the deeper analysis
- **17/12**: Present results on a github page with our finalised data story

## Team organization 

- Initial analysis: tasks can be split in analysis per location, category and year. 
- Deeper analysis: tasks can be split into analysis on quote length, on age and on the highly respected set
- The data visualisation and final presentation can be divided into putting results onto a map, presenting results per media topics, highly respected media, speaker age and quote length.


