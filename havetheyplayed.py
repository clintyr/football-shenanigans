from scrape_and_insert import scrape_wikipedia_and_insert_player_data
import logging
import sqlite3

logging.basicConfig(filename='scraping_errors.log', level=logging.INFO, filemode='a')

def find_player_ids(cursor, player_name):
    cursor.execute("SELECT player_id FROM Players WHERE full_name IS NOT NULL AND known_name LIKE ?", ('%' + player_name + '%',))
    return [row[0] for row in cursor.fetchall()]

def choose_from_multiple_players(conn, cursor, player_ids, player_name):
    print(f"Multiple possible matches found for '{player_name}'")
    for i, player_id in enumerate(player_ids):
        cursor.execute("SELECT full_name FROM Players WHERE player_id = ?", (player_id,))
        full_name = cursor.fetchone()[0]
        print(f"{i+1}. {full_name}")

    try:
        choice = int(input("Which one do you mean? Enter the corresponding number: "))
        if 1 <= choice <= len(player_ids):
            player_id = player_ids[choice-1]
        else:
            print('invalid. please enter a valid choice next time.')
            conn.close()
            return None
    except ValueError:
        print('Come on man..')
        conn.close()
        return None
    return player_id

def check_played_together_club(cursor, player1_id, player2_id, player1_name, player2_name):

    cursor.execute("""SELECT DISTINCT pt1.season_id, pt1.team_id 
                   FROM PlayerTeams pt1 JOIN PlayerTeams pt2 
                   ON pt1.season_id = pt2.season_id AND pt1.team_id = pt2.team_id 
                   WHERE pt1.player_id = ? AND pt2.player_id = ?""", (player1_id, player2_id))
    results = cursor.fetchall()

    if results:
        print(f"{player1_name} and {player2_name} played together at club level in ")
        for season_id, team_id in results:
            cursor.execute("SELECT season FROM Seasons WHERE season_id = ?", (season_id,))
            season = cursor.fetchone()[0]
            cursor.execute("SELECT team_name FROM Teams WHERE team_id = ?", (team_id,))
            team_name = cursor.fetchone()[0]
            print(f"* {season} for {team_name}.")
        print()
        return True
    else:
        print(f"{player1_name} and {player2_name} have never played together at club level.")
        return False

def check_played_same_league(cursor, player1_id, player2_id):
    cursor.execute("""SELECT DISTINCT pt1.season_id, pt1.team_id, pt2.team_id, t1.league_id FROM PlayerTeams pt1 
                   JOIN PlayerTeams pt2 on pt1.season_id = pt2.season_id AND pt1.team_id != pt2.team_id 
                   JOIN Teams t1 on t1.team_id = pt1.team_id JOIN Teams t2 on t2.team_id = pt2.team_id 
                   WHERE pt1.player_id = ? AND pt2.player_id = ? AND t1.league_id = t2.league_id""", 
                   (player1_id, player2_id))
    results = cursor.fetchall()

    return results

def check_same_league_verbose(cursor, results, player1_name, player2_name, prewords=''):
    if results:
        print(f"{prewords}{player1_name} and {player2_name} played in the same league for {len(results)} seasons.")
        for season_id, player1_team_id, player2_team_id, league_id in results:
            cursor.execute("SELECT season FROM Seasons WHERE season_id = ?", (season_id,))
            season = cursor.fetchone()[0]
            cursor.execute("SELECT team_name FROM Teams WHERE team_id = ?", (player1_team_id,))
            player1_team_name = cursor.fetchone()[0]
            cursor.execute("SELECT team_name FROM Teams WHERE team_id = ?", (player2_team_id,))
            player2_team_name = cursor.fetchone()[0]
            cursor.execute("SELECT league_name FROM Leagues WHERE league_id = ?", (league_id,))
            league = cursor.fetchone()[0]
            print(f"* {league} in {season} for {player1_team_name} and {player2_team_name} respectively.")
        print()
        return True
    else:
        print(f"{prewords}{player1_name} and {player2_name} have never played in the same league at the same time.")
        return False

def check_played_together_international(cursor, player1_id, player2_id, player1_name, player2_name):

    cursor.execute("""SELECT DISTINCT pt1.season_id, pt1.nation_id FROM IntlPlayerTeams pt1 JOIN IntlPlayerTeams pt2 
                    ON pt1.season_id = pt2.season_id AND pt1.nation_id = pt2.nation_id WHERE 
                    pt1.player_id = ? AND pt2.player_id = ?""", (player1_id, player2_id))
    results = cursor.fetchall()

    if results:
        print(f"{player1_name} and {player2_name} were called up for ")
        for season_id, nation_id in results:
            cursor.execute("SELECT season FROM Seasons WHERE season_id = ?", (season_id,))
            year = cursor.fetchone()[0]
            cursor.execute("SELECT nation FROM Nations WHERE nation_id = ?", (nation_id,))
            nation = cursor.fetchone()[0]
            print(f"* {nation} in {year}.")
        print()
        return
    else:
        print(f"{player1_name} and {player2_name} never played together internationally.")
        return

def check_players_played_together(player1_name, player2_name):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    player1_ids = find_player_ids(cursor, player1_name)
    player2_ids = find_player_ids(cursor, player2_name)

    if not player1_ids or not player2_ids:
        print("One or both players not yet in database. Adding...")

        if not player1_ids:
            print(f"Attempting to add {player1_name}")
            try:
                scrape_wikipedia_and_insert_player_data(player1_name)
                player1_ids = find_player_ids(cursor, player1_name)
            except Exception as e:
                logging.error(f'couldnt scrape {e}')
        
        if not player2_ids:
            print(f"Attempting to add {player2_name}")
            try:
                scrape_wikipedia_and_insert_player_data(player2_name)
                player2_ids = find_player_ids(cursor, player2_name)
            except Exception as e:
                logging.error(f'couldnt scrape {e}')

        if not player1_ids or not player2_ids:
            print("One or both players could not be scraped.")
            conn.close()
            return
    
    player1_id, player2_id = player1_ids[0], player2_ids[0]
    if len(player1_ids) > 1:
        player1_id = choose_from_multiple_players(conn, cursor, player1_ids, player1_name)
    if len(player2_ids) > 1:
        player2_id = choose_from_multiple_players(conn, cursor, player2_ids, player2_name)

    if any(id is None for id in [player1_id, player2_id]):
        return

    played_at_club = check_played_together_club(cursor, player1_id, player2_id, player1_name, player2_name)
    prewords = ''
    if played_at_club:
        prewords = "Excluding when they've played together, "
    league_results = check_played_same_league(cursor, player1_id, player2_id)
    check_same_league_verbose(cursor, league_results, player1_name, player2_name, prewords=prewords)

    check_played_together_international(cursor, player1_id, player2_id, player1_name, player2_name)

    conn.close()

if __name__ == "__main__":
    player1_name = input("Enter the name of the first player: ")
    player2_name = input("Enter the name of the second player: ")

    check_players_played_together(player1_name, player2_name)