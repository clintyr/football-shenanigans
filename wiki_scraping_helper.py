import re
import warnings
import logging
import math

warnings.simplefilter(action='ignore', category=FutureWarning)

# saving exceptions to a log file
logging.basicConfig(filename='scraping_errors.log', level=logging.INFO, filemode='a')

def process_text(input_text):
    if not isinstance(input_text, str):
        return input_text
    # remove_square_brackets_and_newlines
    new_text = re.sub(r'\[.*?\]', '', input_text).replace('\n', '')
    
    return new_text

def get_club_stats(df):
    """gets desired stats and info from career statistics table wikipedia"""
    club_info = []
    for row in df.iterrows():
        team, season, league = row[1][0], row[1][1], row[1][2]
        league_apps, league_goals = row[1][3], row[1][4]
        all_apps, all_goals = row[1][-2], row[1][-1]

        row_info = [season, team, league, league_apps, league_goals, all_apps, all_goals]
        # print(row_info)

        if not any('total' in str(elem) or 'Total' in str(elem) for elem in row_info):
            club_info.append(row_info)
    club_info = [[process_text(elem) for elem in season] for season in club_info]
    return club_info

def get_intl_stats(df):
    """gets desired info and stats from international career table wikipedia"""
    intl_info = []
    for row in df.iterrows():
        nation, year = row[1][0], row[1][1]
        competitive_apps, competitive_goals = row[1][2], row[1][3]
        caps, goals = row[1][-2], row[1][-1]
        row_info = [year, nation, competitive_apps, competitive_goals, caps, goals]
        if not any('total' in str(elem) or 'Total' in str(elem) for elem in row_info):
            intl_info.append(row_info)
    
    intl_info = [[process_text(elem) for elem in unique_season] for unique_season in intl_info]
    return intl_info

def get_biographics(infobox, player_url):
    player_info = {}
    try:
        for row in infobox.find_all('tr'):
            label = row.find('th', {'scope': 'row'})
            if label:
                label_txt = label.text.strip()
                data = row.find('td')
                if data:
                    data_txt = data.get_text(strip=True)
                    player_info[label_txt] = data_txt
    except Exception as e:
        logging.error(f"failed to get bio info. {e} {player_url}.")
    finally:
        return player_info
    
def fix_numbers(stat):
    try:
        if isinstance(stat, int) or isinstance(stat, float) or stat[0].isdigit():
            try:
                if not math.isnan(float(stat)):
                    return int(stat)
            except ValueError:
                stat = stat.replace('+', '')
                if not math.isnan(float(stat)):
                    return int(stat)
    except Exception:
        return -1 

def extract_height_in_metres(height_string, player_name):
    pattern = r'\d\.\d{2}'
    height_in_metres = re.search(pattern, height_string)
    if height_in_metres:
        height_in_metres = float(height_in_metres.group())
        return height_in_metres
    
    logging.error(f'height formatted weird {player_name}')
    return None