# Underrepresentation of females in media: a myth or a truth?

## Project directory 

:file_folder: Milestone_2: Updated files given for Milestone 2

  |--- **M2_pre_processing.ipynb**: Notebook to clean and organize data for the project.\
  |--- **M2_cleaning.py**: Script containing functions for the data cleaning. Called as a module in `M2_pre_processing.ipynb`.\
  |--- **M2_initial_analysis.ipynb**: Notebook containing the analysis done.\
  |--- **M2_media_wikidata.py**: Script containing functions for extracting data through the wikidata API. Called as a module in both notebooks.\
  |--- **M2_plots.py**: Script containing functions for data analysis in `M2_initial_analysis.ipynb`\

:file_folder: Milestone_3: Files for Milestone 3

  |--- **M3_final_analysis.ipynb**: Final notebook extending the M2 pre-processing and initial analysis `M3_final_analysis.ipynb`\
  |--- **M3_utils.py**: Python file with functions used in the analysis

## Abstract 

Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, they have historically been underrepresented, including in mainstream media. [Studies](https://www.tandfonline.com/doi/full/10.1080/23257962.2016.1260445) have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to explore whether media coverage gives the same possibilities regardless of gender.
The goal is to highlight possible trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. The difference between media's countries of origin, year and media source will also be analysed as well as the impact of such factors on the length and frequency of female quotes.

## Dataset

We use the Quotebank [dataset](https://zenodo.org/record/4277311) for the years 2015-2020. For each quote, it includes information on the speaker (along with their qid from [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)) and the quote source.

The cleaned data is saved on this [drive](https://drive.google.com/drive/folders/1bP67GGJyPXD7bCr5c6f7O2fM40AWpXJN?usp=sharing). A `README_DRIVE.md` in the folder precises the data contained.

## Research questions 

Our main question is: "Is the representation equal between males and females in media?". The following questions guide us through the project:

- How does the distribution of quotes based on gender vary across countries and time?
- How is the age of the speakers distributed depending on gender?
- What if only few females are very often quoted? Look at the distinct speakers!
- Are males more likely to be quoted in highly respected media?
- Focusing on "Entertainment" and "Culture", are they differences between the media sources?

## Additional datasets

- Provided data from Wikidata 
- Dataset which contains the countries belonging to each continent in a [csv](https://github.com/dbouquin/IS_608/blob/master/NanosatDB_munging/Countries-Continents.csv) file. 
- The list of most respected media according to [Forbes](https://www.forbes.com/sites/berlinschoolofcreativeleadership/2017/02/01/10-journalism-brands-where-you-will-find-real-facts-rather-than-alternative-facts/?sh=1c18e04de9b5)
- The list of most read media according to [similarweb](https://www.similarweb.com/top-websites/category/news-and-media/)

## Methods 

**Data filtering**

We limited the dataset by:
- Computing the number of occurrences of each media source (by extracting the site name from the URL)
- Selecting the top 116 medias based on this [list](https://www.4imn.com/top200/)
- Filtering the data to keep only quotes that were mentioned in this top 116

**Data cleaning:**

The data is cleaned by: 
- Removing "None" speakers 
- Removing speakers having a low porbability (50% threshold)
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
splitted in 2 parts: 

1. Looks at the reprensentation of females in countries and then focus on three English speaking countries and digs into:
- the evolution over the years
- the number of unique speakers and the most quoted speakers
- the age distribution between males and females for each of the selected countries
- the media that quote the top speakers

2. Dives into the representation of women within a selected list of respected and popular media. 
- Distribution of females over the years for the two type of media
- Dig further into the categories were females are the most quoted 
- Assess the diversity of speakers within each gender
- Evaluate the quote length based on gender and the selected categories
- Measure the representation of unique female speakers for each of the medias 
- Proceed with some unclustered analysis in order to visualize what topics females really talk about and whether it is consistent with our previous analysis

**Results**

The main results can be found on [the datastory](https://lisalrt.github.io/females-in-media/).
Other interesting results are in the notebook `M3_final_analysis.ipynb`.

## Team contributions 

Lisa: Preliminary data analysis (M2), webmaster (M3), datastory (M3)

Sélène: Retrieving tags (M2), webmaster (M3), datastory (M3), LDA(M3)

Lavinia: Data scrapping from wikidata (M2), code and interpretation of part 2 of the data story (M3), README'S

Arhtur: Code and interpretation for part 1 of the data story (M3), preliminary data analysis (M2)
