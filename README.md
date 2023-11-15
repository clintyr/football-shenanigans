# football-shenanigans
## Goals
### Wikipedia scraper
Web crawling application which extracts footballer biographic information (name, date of birth, place of birth, height (m))
alongside career team data and statistics (appearances, goals) from a player's Wikipedia page in this first iteration.
#### Requirements
 - Python 3+
   - bs4 (BeautifulSoup)
   - requests
#### Methodology
1. Assess structure of typical footballer wikipedia page. (HTML classes of biographical info box and career tables)
2. Retrieve JSON data using HTML parser for relevant data.
3. Data processing and wrangling: regular expressions, handling missing values.
4. Error handling, logging errors for improvement.
5. Iteratively improving scraping ability by allowing robustness to variations in page structure
   (using the log file).
##### Special Cases handled
 - Disambiguation pages on Wikipedia (footballers with common names)
### Database
#### Database structure
Described fully by [create_tbls.sql](https://github.com/clintyr/football-shenanigans/blob/main/create_tbls.sql)
##### Tables
 - Players (Biographic Info), Positions (goalkeeper etc.), PlayerPositions (associative table between player and positions)
 - Leagues, Teams, Seasons, PlayerTeams (assoc. table), Nations, IntlPlayerTeams (assoc. table)
 - ClubGoalsAndAppearances, IntlGoalsAndAppearances
##### Purpose
Scraper inserts directly into our database to avoid making excessive requests to the website and speeds up our initial program and
problem of interest, "Have these players played together?"
### Queries and Analysis
#### Have these players played together?
 - Input: two names of footballers
 - Process: checks if they are in the database, if not extracts their information from Wikipedia and populates the database.
   - Then determines if they were on the same team at the same time at any point in their careers.
 - Output: whether or not they played together or in the same league at any point.

##### Sample Outputs
```
Cristiano Ronaldo and Lionel Messi have never played together at club level.
Cristiano Ronaldo and Lionel Messi played in the same league for 9 seasons.
* La Liga in 2009–10 for Real Madrid and Barcelona respectively.
* La Liga in 2010–11 for Real Madrid and Barcelona respectively.
* La Liga in 2011–12 for Real Madrid and Barcelona respectively.
* La Liga in 2012–13 for Real Madrid and Barcelona respectively.
* La Liga in 2013–14 for Real Madrid and Barcelona respectively.
* La Liga in 2014–15 for Real Madrid and Barcelona respectively.
* La Liga in 2015–16 for Real Madrid and Barcelona respectively.
* La Liga in 2016–17 for Real Madrid and Barcelona respectively.
* La Liga in 2017–18 for Real Madrid and Barcelona respectively.

Cristiano Ronaldo and Lionel Messi never played together internationally.
```
```
Gareth Bale and Aaron Ramsey have never played together at club level.
Gareth Bale and Aaron Ramsey played in the same league for 6 seasons.
* Championship in 2006–07 for Southampton and Cardiff City respectively.
* Premier League in 2008–09 for Tottenham Hotspur and Arsenal respectively.
* Premier League in 2009–10 for Tottenham Hotspur and Arsenal respectively.
* Premier League in 2010–11 for Tottenham Hotspur and Arsenal respectively.
* Premier League in 2011–12 for Tottenham Hotspur and Arsenal respectively.
* Premier League in 2012–13 for Tottenham Hotspur and Arsenal respectively.

Gareth Bale and Aaron Ramsey were called up for 
* Wales in 2008.
* Wales in 2009.
* Wales in 2010.
* Wales in 2011.
* Wales in 2012.
* Wales in 2013.
* Wales in 2014.
* Wales in 2015.
* Wales in 2016.
* Wales in 2017.
* Wales in 2018.
* Wales in 2019.
* Wales in 2020.
* Wales in 2021.
* Wales in 2022.
```
```
Bale and Modric played together at club level in 
* 2008–09 for Tottenham Hotspur.
* 2009–10 for Tottenham Hotspur.
* 2010–11 for Tottenham Hotspur.
* 2011–12 for Tottenham Hotspur.
* 2013–14 for Real Madrid.
* 2014–15 for Real Madrid.
* 2015–16 for Real Madrid.
* 2016–17 for Real Madrid.
* 2017–18 for Real Madrid.
* 2018–19 for Real Madrid.
* 2019–20 for Real Madrid.
* 2021–22 for Real Madrid.

Excluding when they've played together, Bale and Modric have never played in the same league at the same time.
Bale and Modric never played together internationally.
```
