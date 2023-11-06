# %pip install bs4
from insert_data_helper import *
import sqlite3
    
def scrape_wikipedia_and_insert_player_data(player_name):
    print('starting..')
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    player_data = scrape_wikipedia_page(player_name)
    for player_name, player_info, club_info, intl_info in player_data:

        if player_info:
            known_name, full_name, date_of_birth, place_of_birth, nationality, height = gather_player_info(player_name, player_info)

            cursor.execute("""INSERT OR IGNORE INTO Players (known_name, full_name, date_of_birth,
                        place_of_birth, nationality, height) VALUES (?, ?, ?, ?, ?, ?)""", 
                        (known_name, full_name, date_of_birth, place_of_birth, nationality, height))
            
            cursor.execute("""SELECT player_id FROM Players where (full_name, date_of_birth, place_of_birth) = (?, ?, ?)""",
                        (full_name, date_of_birth, place_of_birth))
            player_id = cursor.fetchone()[0]

            # positions
            positions, position_ids = gather_position_info(player_info)

            for position in positions:
                position = position.lower()
                pos = []
                if '/' in position:
                    pos = position.split('/')
                if pos:
                    for position in pos:
                        cursor.execute("""INSERT OR IGNORE INTO Positions (position) VALUES (?)""", (position,))
                        cursor.execute("""SELECT position_id FROM Positions WHERE position = ?""", (position,))
                        position_id = cursor.fetchone()[0]
                        position_ids.append(position_id)
                else:
                    cursor.execute("""INSERT OR IGNORE INTO Positions (position) VALUES (?)""", (position,))
                    cursor.execute("""SELECT position_id FROM Positions WHERE position = ?""", (position,))
                    position_id = cursor.fetchone()[0]
                    position_ids.append(position_id)

            for position_id in position_ids:
                cursor.execute("""INSERT INTO PlayerPositions (player_id, position_id) VALUES (?, ?)""", (player_id, position_id))
        else:
            cursor.execute("""
                        INSERT OR IGNORE INTO Players (known_name) 
                        VALUES (?)""", (player_name,))
            cursor.execute("""SELECT player_id FROM Players where (known_name) = (?)""", (player_name,))
            player_id = cursor.fetchone()[0]

        if club_info:
            # print('club')
            for season_recap in club_info:
                season, team, league, league_apps, league_goals, all_apps, all_goals = gather_club_info(season_recap)

                if '(loan)' in team:
                    team = team[:-7]
                
                if '(loan)' in season:
                    season = season[:-7]
                
                cursor.execute("""INSERT OR IGNORE INTO Leagues (league_name) VALUES (?)""", (league,))
                cursor.execute("""SELECT league_id FROM Leagues WHERE league_name = ?""", (league,))
                league_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO Teams (team_name, league_id) VALUES (?, ?)""", (team, league_id))
                cursor.execute("""SELECT team_id FROM Teams WHERE team_name = ?""", (team,))
                team_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO Seasons (season) VALUES (?)""", (season,))
                cursor.execute("""SELECT season_id FROM Seasons WHERE season = ?""", (season,))
                season_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO PlayerTeams (player_id, team_id, season_id) VALUES
                                (?, ?, ?)""", (player_id, team_id, season_id))
                cursor.execute("""SELECT player_team_id FROM PlayerTeams WHERE (player_id, team_id, season_id) = (?, ?, ?)""",
                            (player_id, team_id, season_id))
                player_team_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO ClubGoalsAndAppearances (player_team_id, league_appearances, league_goals, all_appearances, all_goals) 
                            VALUES (?, ?, ?, ?, ?)""", (player_team_id, league_apps, league_goals, all_apps, all_goals))

        if intl_info:
            # print('intl')
            for year_recap in intl_info:
                year, nation, competitive_apps, competitive_goals, caps, goals = gather_intl_info(year_recap)

                cursor.execute("""INSERT OR IGNORE INTO Nations (nation) VALUES (?)""", (nation,))
                cursor.execute("""SELECT nation_id FROM Nations WHERE nation = ?""", (nation,))
                nation_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO Seasons (season) VALUES (?)""", (year,))
                cursor.execute("""SELECT season_id FROM Seasons WHERE season = ?""", (year,))
                season_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO IntlPlayerTeams (player_id, nation_id, season_id)
                                VALUES (?, ?, ?)""", (player_id, nation_id, season_id))
                cursor.execute("""SELECT player_nation_id FROM IntlPlayerTeams WHERE (player_id, nation_id, season_id) = (?, ?, ?)""",
                            (player_id, nation_id, season_id))
                player_nation_id = cursor.fetchone()[0]

                cursor.execute("""INSERT OR IGNORE INTO IntlGoalsAndAppearances (player_nation_id, competitive_apps, competitive_goals,
                            caps, goals) VALUES (?, ?, ?, ?, ?)""", (player_nation_id, competitive_apps, competitive_goals, caps, goals))

    print('database done')
    conn.commit()
    conn.close()
    return 
    

# reading names in from files for scraping and adding to database
if __name__ == "__main__":
    with open('create_tbls.sql', 'r') as sql_schema:
        sql_script = sql_schema.read()

    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

    files = ['player_names.txt', 'ambig_names.txt']
    for filename in files:
        with open(filename, "r") as file:
            player_names = file.read().splitlines()

        for player_name in player_names:
            scrape_wikipedia_and_insert_player_data(player_name)

