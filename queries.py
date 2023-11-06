import sqlite3

conn = sqlite3.connect('players.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT p.full_name AS player_name, t.team_name, l.league_name, s.season
FROM Players p
JOIN PlayerTeams pt ON p.player_id = pt.player_id
JOIN Teams t ON pt.team_id = t.team_id
JOIN Leagues l ON t.league_id = l.league_id
JOIN Seasons s ON pt.season_id = s.season_id
WHERE p.known_name = 'Gareth Bale' OR p.known_name = 'Juan Mata';
"""

# q = "DELETE FROM ClubGoalsAndAppearances WHERE player_team_id IN (SELECT player_team_id FROM PlayerTeams WHERE player_id IN (SELECT player_id FROM Players WHERE known_name = 'Andrea Pirlo'));"
# q = "DELETE FROM IntlGoalsAndAppearances WHERE player_nation_id IN (SELECT player_nation_id FROM IntlPlayerTeams WHERE player_id IN (SELECT player_id FROM Players WHERE known_name = 'Andrea Pirlo'));"
# q = "DELETE FROM PlayerPositions WHERE player_id IN (SELECT player_id FROM Players WHERE known_name = 'Andrea Pirlo');"
# q = "DELETE FROM IntlPlayerTeams WHERE player_id IN (SELECT player_id FROM Players WHERE known_name = 'Andrea Pirlo');"
# q = "DELETE FROM PlayerTeams WHERE player_id IN (SELECT player_id FROM Players WHERE known_name = 'Andrea Pirlo');"
# q ="DELETE FROM Players WHERE known_name = 'Andrea Pirlo';"


cursor.execute(query)
results = cursor.fetchall()

for result in results:
    print(result)

conn.close()