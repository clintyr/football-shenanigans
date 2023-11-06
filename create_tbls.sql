CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    known_name TEXT,
    full_name TEXT,
    date_of_birth DATE,
    place_of_birth TEXT,
    nationality VARCHAR(100),
    height DECIMAL(3,2),
    UNIQUE (full_name, date_of_birth, place_of_birth)
);

CREATE TABLE IF NOT EXISTS Positions (
    position_id INTEGER PRIMARY KEY AUTOINCREMENT,
    position TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS PlayerPositions (
    player_id INTEGER,
    position_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES Players (player_id),
    FOREIGN KEY (position_id) REFERENCES Positons (position_id)
);

CREATE TABLE IF NOT EXISTS Leagues (
    league_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_name VARCHAR(250) UNIQUE
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT UNIQUE,
    league_id INTEGER,
    FOREIGN KEY (league_id) REFERENCES Leagues (league_id)
);

CREATE TABLE IF NOT EXISTS Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season VARCHAR(10) UNIQUE
);

CREATE TABLE IF NOT EXISTS PlayerTeams (
    player_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    team_id INTEGER,
    season_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES Players (player_id),
    FOREIGN KEY (team_id) REFERENCES Teams (team_id),
    FOREIGN KEY (season_id) REFERENCES Seasons (season_id)
);

CREATE TABLE IF NOT EXISTS Nations (
    nation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nation VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS IntlPlayerTeams (
    player_nation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    nation_id INTEGER,
    season_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES Players (player_id),
    FOREIGN KEY (nation_id) REFERENCES Nations (nation_id),
    FOREIGN KEY (season_id) REFERENCES Seasons (season_id)
);

CREATE TABLE IF NOT EXISTS ClubGoalsAndAppearances (
    goal_appearance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_team_id INTEGER UNIQUE,
    league_appearances INTEGER,
    league_goals INTEGER,
    all_appearances INTEGER,
    all_goals INTEGER,
    FOREIGN KEY (player_team_id) REFERENCES PlayerTeams (player_team_id)
);

CREATE TABLE IF NOT EXISTS IntlGoalsAndAppearances (
    intl_goal_appearance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_nation_id INTEGER UNIQUE,
    competitive_apps INTEGER,
    competitive_goals INTEGER,
    caps INTEGER,
    goals INTEGER,
    FOREIGN KEY (player_nation_id) REFERENCES IntlPlayerTeams (player_nation_id)
);