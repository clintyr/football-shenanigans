import io
import warnings
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from wiki_scraping_helper import *

warnings.simplefilter(action='ignore', category=FutureWarning)

# saving exceptions to a log file
logging.basicConfig(filename='scraping_errors.log', level=logging.INFO, filemode='a')

def scrape_disambiguation_page(page_url, page_id, links_params):
    """scrapes all footballer pages when a disambiguation page is encountered"""
    try:
        response = requests.get(page_url, params=links_params)
        if response.status_code != 200:
            logging.warning(f"Failed to fetch {page_url}")
            return
        data = response.json()
        links = data["query"]["pages"][page_id]["links"]

        footballer_links = [link["title"] for link in links if "footballer" in link["title"]]
        return footballer_links

    except Exception as e:
        logging.error(f"Error processing disambiguation {page_url} {e}.")
        return []

def scrape_non_disambiguation_page(player_name):
        page_title = player_name.replace(' ', '_')
        player_url = f"https://en.wikipedia.org/wiki/{page_title}"
        response = requests.get(player_url)

        if response.status_code == 200:
            print(player_name)
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table', {'class': 'wikitable'})
            infobox = soup.find('table', {'class': 'infobox vcard'})
            if infobox is None:
                infobox = soup.find('table', {'class': 'infobox biography vcard'})

            club_info, intl_info = [], []
            player_info = get_biographics(infobox, player_url)

            for tbl in tables:
                df = pd.read_html(io.StringIO(str(tbl)))
                df = pd.DataFrame(df[0])
                
                if 'Club' in df.columns and not club_info:
                    club_info = get_club_stats(df)
                
                elif ('Team' in df.columns or 'National team' in df.columns) and not intl_info:

                    intl_info = get_intl_stats(df)
            return player_name, player_info, club_info, intl_info
        
        else:
            logging.error(f"Failed to retrieve player page. {player_url}.")
            return player_name, [], [], []
        
def scrape_wikipedia_page(player_name):
    """gets club career and international career info for a given player"""
    api_url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": player_name,
        "prop": "categories",
        "format": "json",
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        player_data = []
        data = response.json()

        pages = data["query"]["pages"]
        page_id, page_info = next(iter(pages.items()))
        footballer_links = [] # to store disambig data

        is_disambiguation_page = any("disambiguation" in cat["title"] for cat in page_info.get("categories", []))

        if is_disambiguation_page:
            links_params = {
                "action": "query",
                "titles": player_name,
                "prop": "links",
                "pllimit": "max",
                "format": "json",
            }

            footballer_links = scrape_disambiguation_page(api_url, page_id, links_params)
        
        page_title = player_name.replace(' ', '_')
        player_url = f"https://en.wikipedia.org/wiki/{page_title}"

        player_name, player_info, club_info, intl_info = scrape_non_disambiguation_page(player_name)
        player_data.append([player_name, player_info, club_info, intl_info])

        if footballer_links:
            for disambig_title in footballer_links:
                player_name, player_info, club_info, intl_info = scrape_non_disambiguation_page(disambig_title)
                player_data.append([player_name, player_info, club_info, intl_info])
        
        return player_data   
    else:
        logging.error(f"Failed to reach Wiki page{player_url}")
        return [[player_name, [], [], []]]