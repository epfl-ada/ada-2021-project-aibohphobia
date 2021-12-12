# Underrepresentation of females in media: a myth or a truth?


TODO for M3 
- [ ] Upload drive readme
- [ ] Merge the final df, Lavi and Art 
- [ ] Make sure that code is documented
- [ ] Upgreade the research questions here
- [x] Link this github to the website for easy access
- [ ] List who did what 
- [x] Make folders for milestone 2 and 3


## Contents

* [Project directory](#project-directory)
* [Abstract](#abstract)
* [Dataset](#dataset)
* [Research questions](#research-questions)
* [Additional datasets](#additional-datasets)
* [Methods](#methods)
* [Team contributions](#team-contributions)


## Project directory 
:file_folder: Milestone_2: Updated files given for Milestone 2

  |--- **M2_pre_processing.ipynb**: Notebook to clean and organize data for the project.\
  |--- **M2_cleaning.py**: Script containing functions for the data cleaning. Called as a module in `M2_pre_processing.ipynb`.\
  |--- **M2_initial_analysis.ipynb**: Notebook containing the analysis done.\
  |--- **M2_media_wikidata.py**: Script containing functions for extracting data through the wikidata API. Called as a module in both notebooks.\
  |--- **M2_plots.py**: Script containing functions for data analysis in `M2_initial_analysis.ipynb`\

:file_folder: Milestone_3: Files for Milestone 3

  |--- **M3_final_analysis.ipynb**: Final notebook extending the M2 pre-processing and initial analysis `M3_final_analysis.ipynb`\

## Abstract 

Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, they have historically been underrepresented, including in mainstream media. [Studies](https://www.tandfonline.com/doi/full/10.1080/23257962.2016.1260445) have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to explore whether media coverage gives the same possibilities regardless of gender.
The goal is to highlight possible trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. The difference between countries, year and media source will also be analysed as well as the impact of such factors on the length and frequency of female quotes.

## Dataset

We use the Quotebank [dataset](https://zenodo.org/record/4277311) for the years 2016-2020. For each quote, it includes information on the speaker (along with their qid from [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)) as well as the quote source.

The cleaned data is saved on this [drive](https://drive.google.com/drive/folders/1bP67GGJyPXD7bCr5c6f7O2fM40AWpXJN?usp=sharing). A `README_DRIVE.md` in the folder precises the data contained.

## Research questions 

Throughout this study we aim to answer a main question: "Is the representation equal between males and females in media?". The following questions will guide us through the project:

- How does the distribution of quotes based on gender vary across countries, topics, location and time?
- Are males more likely to be quoted in highly respected media?
- Is there a difference in how females/males at a certain age are quoted?


## Additional datasets

- Provided data from Wikidata 
- Dataset which contains the countries belonging to each continent in a [csv](https://github.com/dbouquin/IS_608/blob/master/NanosatDB_munging/Countries-Continents.csv) file. 
- The list of most respected media according to [Forbes](https://www.forbes.com/sites/berlinschoolofcreativeleadership/2017/02/01/10-journalism-brands-where-you-will-find-real-facts-rather-than-alternative-facts/?sh=1c18e04de9b5)
- The list of most read media according to [similarweb](https://www.similarweb.com/top-websites/category/news-and-media/)

## Methods 

**Data filtering**

We limited the dataset by:
- Computed the number of occurrences of each media source (by extracting the site name from the URL)
- Selected the top 116 medias based on this [list](https://www.4imn.com/top200/)
- Filtered the data to keep only quotes that were mentioned in this top 116

**Data cleaning:**

The data is cleaned by: 
- Removing "None" speakers 
- Removing speakers havong a low porbability (50% threshold)
- Verifying quotes are non empty 

**Additional data extraction**

Using the URL and data from Wikidata: 
- Tags are added if the URL contains words of a topic from a predefined list (e.g.: sports, business, ...)
- Using the URLs from QuoteBank, we extract features from the newspaper (e.g.: country of origin) using WikiData API
- Change QIDs to labels (e.g.: "Q31" to "Belgium")
- Using the QID, find the speaker's nationality, date of birth and gender
- The speaker's age (up to 100 yrs) is calculated at the moment of the quote.

**Initial analysis of data (Milestone 2)**

1. Comparison of number of male versus female quotes
- Overall difference in count of males versus females, over all years 
- Overall count of male/female quotes, per year, per category, per geographical location and a combination of these

2. Tests for statistical significance to see if:
- the percentage of quotes said by females is evolving over the years (using linear regression)
- the difference in ages of quoted persons (regarding gender) is statistically significant.

**Deeper analysis**
For our final data story we split the story in *two*. 

The *first part* looks at the reprensentation of females in countries and then focus on three English speaking countries and digs into:
- the evolution over the years
- the number of unique speakers and the most quoted speakers
- the age distribution between males and females for each of the selected countries
- the media that quote the top speakers

The *second part* dives into the representation of women within a selected list of respected and popular media. 
- Distribution of females over the years for the two type of medias
- Looking at what females talk about in the respective media
- Dig further into the categories were females are the most quoted 
- Assess the divesity of speakers within each gender
- Evaluate the quote length based on gender and the selected categories
- Measure the representation of unique female speakers for each of the medias 
- Proceed with some unclustered analysis in order to visualize what topics females really talk about and whether it is cnosistent with our previous analysis


**Results**

The main results may be found in [the datastory](https://lisalrt.github.io/females-in-media/).
Other interesting results may be found in the notebook `M3_final_analysis.ipynb` with some interpretations



## Team contributions 

Lisa: Plotting graphs during data analysis, preliminary data analysis, webmaster, datastory

Sélène: Retrieving tags, webmaster, datastory, 

Lavinia:Data scrapping from wikidata, part 2 of the data story, README

Arhtur: Code for part 1 of the data story






