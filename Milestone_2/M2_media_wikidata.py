import requests

from urllib.parse import urlparse
import time

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


def query_ID_URL(URL):
    """
        Using the URL of the media we use the property P856 (original website) in order to find the QID of the website

    @param URL: parsed URL of the media
    @return: QID of the media
    """
    query = "SELECT ?entity ?value WHERE  {{ ?entity wdt:P856 <{}> .}}".format(URL)
    try:
        r = requests.get(url_spaql, params={'format': 'json', 'query': query})
        if (r.status_code == 429):
            raise
    except:
        time.sleep(1.5)
        r = requests.get(url_spaql, params={'format': 'json', 'query': query})

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
    length_list = len(URLS_websites)
    for id_, URL in enumerate(URLS_websites):
        print("{}/{} done of lines".format(id_ + 1, length_list))

        tmp_countries = []

        URLS_parsed, another_parse, www_https, www_http = parse_URL(str(URL))

        for id_URL, URL_parsed in enumerate(URLS_parsed):
            #print("{}/{} done of journals within line".format(id_URL + 1, len(URLS_parsed)))

            try:
                # Wikidata ID
                QID = testing_try(URL_parsed, id_URL, another_parse, www_https, www_http)

                data_get = requests.get(url_API, params=get_parameters(QID))

                tmp_countries = extract_country(tmp_countries, data_get, QID)


            except:

                try:
                    QID = testing_try(URL_parsed[:-1], id_URL, another_parse, www_https, www_http, remove_backlash=True)

                    data_get = requests.get(url_API, params=get_parameters(QID))
                    tmp_countries = extract_country(tmp_countries, data_get, QID)

                except:
                    # The media does not have an attribute ""orginal"" website and may thus not be found
                    tmp_countries.append("None")

        country_of_origin[id_] = tmp_countries

    return country_of_origin
