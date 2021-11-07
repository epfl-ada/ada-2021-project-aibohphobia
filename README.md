# Underrepresentation of females in media: a myth or a truth

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

## Additional datasets

We are interested in linking the quote to a geographical place, we do so by taking the origin of location of the journal.
We currently use the URL given by the QuoteBank to retrieve information about the journal though the wikidata API. **

As of now we do not plan on adding any additional datasets.

## Methods
**Data cleaning: **

A function is used to clean the data in the following ways:
- Remove "None" speakers 
- Remove speakers with a probabily inferior to a certain threshold (50%)
- Make sure quotes are non empty 
- Change QID's to labels for eg. "Q31"-->"Belgium"
- Output json file for each year ??
- Please add Lisa/Souche
     
**Extraction of information from journals:**
- Using the URL's from QuoteBank, we extract features such as the country of origin from the newspaper using WikiData

** **

## Graphs to do
- Compare number of males vs females
- Group by country, redo females vs males
- Group by age group and look at the distribution of speakers by gender
- Group by topics and analyse men vs women 


## Libraries of interest
- Request: for extracting data
- Pandas: for showing the data in jupyter
- Seaborn/Matplotlib: for graphs 
- URL parser: for parsing URLS in the way we need (for eg: media information)
- Statsmodel: Statistics library for making our analysis
- Bokeh: interactive plotting for advanced visualization 

## Timeline

- 12/11: Hand in Milestone 2 with the goal of having a dataframe which may be used for our analysis (for a certain year to start)
- 17/11: Finish the basic data analysis using the visualization libraries and statistics on the year of interest
- 19/11: Proceed in similar fashion for the other years
- 

## Team organization 





## Questions for TA:
**: There seems to be a limit to the number of requests one can ask from wikidata which makes it hard to actually extract information about the journal, I am in touch with Akhil to figure this out



Reference:
(1) -  Michelle Caswell, Alda Allina Migoni, Noah Geraci & Marika Cifor (2017) ‘To Be Able to Imagine Otherwise’: community archives and the importance of representation, Archives and Records, 38:1, 5-26, DOI: 10.1080/23257962.2016.1260445 
