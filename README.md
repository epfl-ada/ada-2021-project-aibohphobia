# The influence of women in time and domain
TODO: CHange title for "more catch" #Lisa
TODO: Change women to female and men to male  

## Abstract
Females' equal participation in all facets of society is a fundamental human right. Yet, around the world, from politics to entertainment to the workplace, they have historically been underrepresented, including in mainstream media. Studies (1) have shown that representation is important for inspiration and has positive feedback in spreading gender equality. We therefore want to see whether media coverage gives the same possibilities regardless of gender.
Throughout this project we want to see where females are given a voice to express themselves but also the topics that they speak about. The goal is to analyze trends about which media sources quote females and analyse their proportion of published quotations in comparison to males. Additionally, certain domains and subjects are known to have a gender gap. This study is therefore interested in understanding which fields present differences between genders, may it be politics, sports, culture or others. 

Word count: 146 words

TODO:Be inspired  
TODO: Careful when talking about journal, state media instead for now 


## Research questions

This study aims at answering the following questions:
 
- Is the representation equal between males and females in media?
- How does the distribution of quotes based on gender vary across countries?
- How does the distribution of quotes based on gender vary across domains? 
- If males have a higher tendency to be quoted, in which domains is it the case and by how much?
- How does the distribution of quotes between genders evolve in time, geographically and thematically?
- Is there a tendency in each category for a males to have longer quotes than females?
- Are males more likely to be quoted in highly respected media?  --> define highly respected
- Are there any blind spots in media where females are especially neglected?
- Is there a difference in how females/males at a certain age are quoted?

## Additional datasets

We are interested in linking the quote to a geographical place, we do so by taking the origin of location of the journal. We would use the WikidataAPI to extract the information of interest of a given journal.
Dataset which groups a list of words 
Subset of wikidata which links QID to name. 

## Methods
- Data cleaning: develop Lisa
- URL parsing 
- Merging dataframes
- Clustering etc please ADD HELP HELP HELP 

## Graphs to do
- Compare number of males vs females
- Group by country, redo females vs males
- Group by age group and look at the distribution of speakers by gender
- Group by topics and analyse men vs women 


## Timeline
# Lavi 

## Team organization 




## Questions for TA:
Arthur:
- Extract the gender of the journalist and see if one is more likely to quote a certain gender
- 

Lavi:
- Is there a prettier way to extract the QID/attributes than the python file API, how to deal with the url not necessarily
- being an alias known to wikidata
- "How" to deal with media which is not in the wikidata dump; where to find country of origin 

Souche:
- How to hand select news/media sources without too much bias ? 
- Same for url topics, how to define a list of categories to search?

Lisa: 

- Choose the prob style 
- verify QID 
- Check if quote is from a language 
