# Underrepresentation of females in media: a myth or a truth?

## Abstract
Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, from politics, entertainment to the workplace, they have historically been underrepresented, including in mainstream media. Studies [1] have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to disocver whether media coverage gives the same possibilities regardless of gender.
Throughout this project we want to analyse whether females are given the floor to speak but also about which topics they are quoted on. 
The goal is to highlight possible trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains and subjects are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. 

Word_count: 146

## Research questions

This study aims at answering the following questions:
 
- Is the representation equal between males and females in media?
- How does the distribution of quotes based on gender vary across countries and across domains?
- How does the distribution of quotes between genders evolve in time, geographically and thematically?
- Is there a tendency in each category for a males to have longer quotes than females?
- Are males more likely to be quoted in highly respected media? 
- Are there any blind spots in media where females are especially neglected?
- Is there a difference in how females/males at a certain age are quoted?


Extra ideas (draft selene):
- can we identify speakers who were quoted and that triggered a change in trend? Example: a woman is quoted once as she talks about topic A. After that we see an increase of women quoted talking about topic A ? Like some turning points in media?
- Take data from countries who are known to be more "gender equal" or that have made statements for gender equality (like scandinavian countries) and compare with the rest of the world to see of this is actually reflected in media.



## Additional datasets

As we are interested in linking the quote to a geographical place, we do so by taking the origin of location of the journal.
We currently use the URL given by the QuoteBank dataset to retrieve information about the journal though the wikidata API. **

As of now we do not plan on using any additional datasets.

## Methods
**Data cleaning: **

A function is used to clean the data in the following ways:
- Remove "None" speakers 
- Remove speakers with a probability inferior to a certain threshold (50%)
- Make sure quotes are non empty 
- Change QID's to labels for eg. "Q31"-->"Belgium"
- Tags are added if the url contains specific mentions of a topic from a predefined list (e.g.: sports, business, music...)
     
**Extraction of information from journals:**
- Using the URL's from QuoteBank, we extract features such as the country of origin from the newspaper using WikiData API

**Initial analysis of data**

Comparison of number of male versus female quotes
- Overall difference in count of males versus females, over all years. 
- Overall count of male versus female quotes, per year.
- Overall count of male versus female quotes, per category.
- Overall count of male versus female quotes, per year and per category.
- Overall count of male versus female quotes, per country/geographical location.
- Overall count of male versus female quotes, per year and per country/geographical location.

Tests for statistical significance 
- Perform statistical tests to see if the difference between counts of males and females per year is statistically significant.
- Perform statistical tests to see if the difference per year and per category is statistically significant.
- Perform statistical tests to see if the difference per year and per location is statistically significant.

**Deeper analysis**

Comparison of media coverage depending on gender in highly repsected media
- Based on a set of media sources deemed to be "highly respected" (which will be defined and justified), compare the number of males and females that have been quoted and test if there is any statistical significance.

Comparison in length of quote
- Perform statistical tests to analyse whether a difference in the length of quotes between is significant between years and location or category.

Media coverage in function of age
- Group speakers into classes of age and analyse trends that can appear with respect to aforementioned criteria between genders. 


**Results**
In this part, we want to analyse the data obtained during our analysis in order to formulate and present the trends or any interesting results that we might have uncovered.

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

- 12/11: Hand in Milestone 2 having done part of the initial analysis on data (for a certain year only? Because then we cannot analyse temporality. It's not a problem, but in that case we should just specify that we won't do the analysis with respect to time or any of the statistical test)
- 19/11: Finish the basic data analysis using the visualization libraries and statistics on the year (again, year or years?) of interest. Have plots and numbers ready, which could possibly 
- 3/12: Complete with deeper analysis
- 17/12: Present results on a github page with our finalised data story

## Team organization 

For the initial analysis, the tasks can be split depending on whether the analysis is done per location or per category.
For the deeper analysis, the tasks can be split into 3 parts (analysis on quote length, on age and on the highly respected set)
The data visualisation and final presentation of the results can also be divided according to message that we want to transmit. This means that team's efforts will be dedicated in part to presenting the map, the categories and the highly repsected journals/media respectively.




## Questions for TA:
**: There seems to be a limit to the number of requests one can ask from wikidata which makes it hard to actually extract information about the journal, I am in touch with Akhil to figure this out



Reference:
(1) -  Michelle Caswell, Alda Allina Migoni, Noah Geraci & Marika Cifor (2017) ‘To Be Able to Imagine Otherwise’: community archives and the importance of representation, Archives and Records, 38:1, 5-26, DOI: 10.1080/23257962.2016.1260445 
