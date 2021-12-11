import requests

from urllib.parse import urlparse
import time
from tld import get_tld

url_API = "https://www.wikidata.org/w/api.php"
url_spaql = 'https://query.wikidata.org/sparql'


# Function to find page using QID
def get_parameters(QID):
    """
        Function to find page using QID
    @param QID: Wikidata identifier
    @return: A research dictionarry with the QID of interest
    """
    params_get = {
        "action": "wbgetentities",
        "format": "json",
        "ids": QID,
        "languages": "en",
        "sites": "enwiki",
    }
    return params_get


def get_delay(date):
    try:
        date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
        timeout = int((date - datetime.datetime.now()).total_seconds())
    except ValueError:
        timeout = int(date)
    return timeout

def query_ID_URL(URL):
    """
        Using the URL of the media we use the property P856 (original website) in order to find the QID of the website

    @param URL: parsed URL of the media
    @return: QID of the media
    """
    query = "SELECT ?entity ?value WHERE  {{ ?entity wdt:P856 <{}> .}}".format(URL)
    try:
        r = requests.get(url_spaql, params={'format': 'json', 'query': query})
        print("-----------------",r.status_code,"-----------------")
        if (r.status_code == 429):
            raise 
    
    except:
        timeout = get_delay(r.headers['retry-after'])
        print("timeout = ", timeout)
        
        time.sleep(timeout)
        r = requests.get(url_spaql, params={'format': 'json', 'query': query})
        print("2nd = ", r_status_code)
    data = r.json()
    

    return data["results"]["bindings"][0]["entity"]["value"].split("/")[-1]


def parse_URL(URL):
    """

    @param URL: Full URL
    @return: Part of the URL for eg. www.google.com/ instead of www.google.com/search:
    it also returns combinations such as https://www.news and https://news
    """

    URL_split = URL.split()
    results = []
    opposite_scheme_results = []
    www_removed_https = []
    www_removed_http = []

    for URL in URL_split:
        try:
            res = get_tld("h" + URL.split("h",1)[-1], as_object=True)
        except:
            break
        
        URL = res.parsed_url.scheme + "://"+res.parsed_url.netloc
        parsed_uri = urlparse("h" + URL.split("h", 1)[1])
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        if parsed_uri.scheme == "https":

            other_scheme = "http"
            opposite_scheme_result = '{}://{uri.netloc}/'.format(other_scheme, uri=parsed_uri)
            if result.find("://www.") != -1:

                www_removed_https.append(result.replace("www.", ""))
                www_removed_http.append(opposite_scheme_result.replace("www.", ""))
            else:
                www_removed_https.append(result.replace("://", "://www."))
                www_removed_http.append(opposite_scheme_result.replace("://", "://www."))

        else:

            other_scheme = "https"
            opposite_scheme_result = '{}://{uri.netloc}/'.format(other_scheme, uri=parsed_uri)

            if (result.find("://www.")) != -1:

                www_removed_http.append(result.replace("www.", ""))
                www_removed_https.append(opposite_scheme_result.replace("www.", ""))
            else:
                www_removed_http.append(result.replace("://", "://www."))
                www_removed_https.append(opposite_scheme_result.replace("://", "://www."))

        results.append(result)
        opposite_scheme_results.append(opposite_scheme_result)
    return results, opposite_scheme_results, www_removed_https, www_removed_http


def testing_try(URL_parsed, id_URL, other_parse, www_https, www_http, remove_backlash=False):
    """

    @param URL_parsed: The URL given in the quotebank parsed with main domain kept
    @param id_URL: current URL we are analysing
    @param other_parse: Using other scheme than the URL_parsed for eg: https instead of htpp
    @param www_https: https URLS with or without www. depending on initial URL
    @param www_http: https URLS with or without www. depending on initial URL
    @param remove_backlash: Boolean on whether or not to remove the backslash at the end of a URL
    @return: Dictionary with line and country associated to media
    """
    QID = 0
    if remove_backlash:
        other_parse = other_parse[id_URL][:-1]
        www_https = www_https[id_URL][:-1]
        www_http = www_http[id_URL][:-1]
    else:
        other_parse = other_parse[id_URL]
        www_https = www_https[id_URL]
        www_http = www_http[id_URL]

    for URL_test in URL_parsed, other_parse, www_https, www_http:

        try:
            QID = query_ID_URL(URL_test)
            if (QID != 0):
                break

        except:
            pass

    if (QID == 0):
        raise

    else:
        return QID


def extract_country(tmp_countries, data_get, QID):
    try:
        # Try country of origin
        tmp_countries.append(
            data_get.json()["entities"][QID]["claims"]["P17"][0]["mainsnak"]["datavalue"]["value"]["id"])

    except:
        try:
            # Try country
            tmp_countries.append(
                data_get.json()["entities"][QID]["claims"]["P495"][0]["mainsnak"]["datavalue"]["value"][
                    "id"])

        except:
            # The media has no information about country
            tmp_countries.append("No_country")

    return tmp_countries
def extract_info_wiki(URLS_websites):
    """
    Using the URL from the quote, we extract information about the media

    @param URLS_websites: list of strings with the URL from the quote
    @return:country_of_origin: String containing the country of origin QID (but others may be added if deemed interesting)

    """
    country_of_origin = {}
    dic_history = {}
    length_list = len(URLS_websites)
    for id_, URL in enumerate(URLS_websites):
        if (id_ %1000 == 0):
            print("{}/{} done of lines".format(id_ + 1, length_list))

        tmp_countries = []
        # Verify sfgate
        URLS_sfgate = [x for x in URL if 'sfgate' in x]
        
        if (len(URLS_sfgate)!= 0):
            URL = ["https://www.sfchronicle.com/" if x== URLS_sfgate[0] else x for x in URL]

        URLS_parsed, another_parse, www_https, www_http = parse_URL(str(URL))

        for id_URL, URL_parsed in enumerate(URLS_parsed):
            #print("{}/{} done of journals within line".format(id_URL + 1, len(URLS_parsed)))

            # Check if you've already saved information about the media in the dic
            if (www_https[id_URL] not in dic_history):

                try:
                    # Wikidata ID
                    QID = testing_try(URL_parsed, id_URL, another_parse, www_https, www_http)
                   #print(QID)

                    data_get = requests.get(url_API, params=get_parameters(QID))

                    tmp_countries = extract_country(tmp_countries, data_get, QID)
                    dic_history[www_https[id_URL]] = tmp_countries[-1]

                except:

                    try:
                        QID = testing_try(URL_parsed[:-1], id_URL, another_parse, www_https, www_http,
                                          remove_backlash=True)
                        #print(QID)

                        data_get = requests.get(url_API, params=get_parameters(QID))
                        tmp_countries = extract_country(tmp_countries, data_get, QID)
                        dic_history[www_https[id_URL]] = tmp_countries[-1]

                    except:
                        # The media does not have an attribute ""orginal"" website and may thus not be found
                        tmp_countries.append("None")
                        dic_history[www_https[id_URL]] = "None"
            else:
                tmp_countries.append(dic_history[www_https[id_URL]])

        country_of_origin[id_] = tmp_countries

    return country_of_origin
