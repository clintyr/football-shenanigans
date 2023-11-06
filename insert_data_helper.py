from wiki_scraping import *
from datetime import datetime

def gather_player_info(player_name, player_info):
    known_name = player_name
    try:
        full_name = process_text(player_info['Full name'])
    except Exception as e:
        logging.warning(f"different-biography table {e}.")
        full_name = known_name

    try:    
        date_str = process_text(player_info['Date of birth'])
        date_match = re.search(r'(\d{1,2} \w+ \d{4})', date_str)
        date_of_birth = datetime.strptime(date_match.group(1), '%d %B %Y') if date_match else None
    except Exception as e:
        logging.warning(f"date of birth error {e}")
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', process_text((player_info['Born'])))
        date_of_birth = datetime.strptime(date_match.group(1), '%Y-%m-%d') if date_match else None

        date_end_index = date_match.end() if date_match else 0

    try:
        place_of_birth = process_text(player_info['Place of birth'])
        nationality = place_of_birth.split(',')[-1].strip()
        place_of_birth = place_of_birth.rsplit(',', 1)[0].strip()
        place_of_birth = re.sub(r',\s*', ', ', place_of_birth)    
    except Exception as e:
        logging.warning(f"place of birth error {e}")
        place_of_birth = process_text(player_info['Born'])[date_end_index:]
        nationality = place_of_birth.split(',')[-1]
        place_match = re.search(r'([^,()]+)\s*,', place_of_birth)
        place_of_birth = place_match.group(1).strip() if place_match else None

    height = extract_height_in_metres(player_info["Height"], player_name)
    return known_name, full_name, date_of_birth, place_of_birth, nationality, height

def gather_position_info(player_info):

    # positions
    position_keys = ["Position", "Position(s)", "Positions"]
    for key in position_keys:
        if key in player_info:
            position = key
            break
    
    position = process_text(player_info[position])
    positions = re.split(r'\s*,\s*', position)
    position_ids = []
    
    return positions, position_ids


def gather_club_info(season_recap):
    season, team, league, league_apps, league_goals, all_apps, all_goals = season_recap
    league_apps, all_apps = fix_numbers(league_apps), fix_numbers(all_apps)
    league_goals, all_goals = fix_numbers(league_goals), fix_numbers(all_goals)

    return season, team, league, league_apps, league_goals, all_apps, all_goals

def gather_intl_info(year_recap):
    year, nation, competitive_apps, competitive_goals, caps, goals = year_recap
    competitive_apps, caps = fix_numbers(competitive_apps), fix_numbers(caps)
    competitive_goals, goals = fix_numbers(competitive_goals), fix_numbers(goals)

    return year, nation, competitive_apps, competitive_goals, caps, goals