
import requests
import json


url = "https://www.wikidata.org/w/api.php"

# Function to find page using QID
def get_parameters(QID):
    params_get = {
    "action": "wbgetentities",
    "format": "json",
    "ids" : QID,
    "languages" : "en",
    "sites" : "enwiki",
    }
    return params_get


def extract_country_wiki(name_of_journals):
    """
    input:
    name_of_journal: list of strings with the name of journal
    Note: even if it contains only one journal please pass a list ["string<"]
    
    return:
    country_of_origin: String containing the country of origin QID 

    """
    country_of_origin = []
    for name_of_journal in name_of_journals:
        

        # Wikidata ID 
        QID = ""
        # Parameters used to search wikiAPI using name of journal to extract QID
        params_search = {
        "action" : "wbsearchentities",
        "language" : "en",
        "format" : "json",
        "search" : name_of_journal ,
        "sites" : "enwiki",
        }


        """
            This is ugly but it works :/ 
        """
        
        try:
            data_search_QID = requests.get(url,params=params_search)

            QID = str(data_search_QID.json()["search"][0]["id"])
            
            data_get = requests.get(url,params=get_parameters(QID))
            
            try:
                country_of_origin.append(data_get.json()["entities"][QID]["claims"]["P17"][0]["mainsnak"]["datavalue"]["value"]["id"])
            
            except:
                try:
                    country_of_origin.append(data_get.json()["entities"][QID]["claims"]["P495"][0]["mainsnak"]["datavalue"]["value"]["id"])
            
                except:
                    print("No country information available for the given journal")


        except:
            """
                This print may be removed because it is quite long if you get several journals with no wikipedia page
            """
            print("Invalid, make sure it is an alias sited on the wikidata page, and be careful with spaces :); it is also possible that the website does not have a wikipedia page")
            country_of_origin.append(float('NaN'))
            
        
    return country_of_origin
