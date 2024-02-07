import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://www.ea.com"
base_ratings_url = "https://www.ea.com/games/ea-sports-fc/ratings"
response = requests.get(base_ratings_url)

soup = BeautifulSoup(response.text, 'html.parser')

# Find the player stats

player_stats = []
cl_teams=["Arsenal","Atlético de Madrid","FC Barcelona","FC Bayern München","F.C. København","Borussia Dortmund","FC Porto","Inter","Latium","RB Leipzig","Manchester City","Napoli FC","Paris SG","PSV","Real Madrid","Real Sociedad"]

# Loop through multiple pages
for page_num in range(1, 174):  # Change the range according to the number of pages you want to scrape
    url = f"{base_ratings_url}?page={page_num}"
    print(f"Scraping page {page_num} of {base_ratings_url}...")
    #time.sleep(0.5)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_players = soup.find_all('tr', class_='Table_row__4INyY')

    for player_row in all_players:
        team = player_row.find_all('a', class_='Table_centerCell__RWh19')[1].find('img')['alt'].strip() if player_row.find_all('a', class_='Table_centerCell__RWh19') and len(player_row.find_all('a', class_='Table_centerCell__RWh19')) > 1 else "N/A"
        if team not in cl_teams:
            continue
        team_uri = player_row.find_all('a', class_='Table_centerCell__RWh19')[1].find('img')['src'].strip() if player_row.find_all('a', class_='Table_centerCell__RWh19') and len(player_row.find_all('a', class_='Table_centerCell__RWh19')) > 1 else "N/A"
        flag_uri = player_row.find_all('a', class_='Table_centerCell__RWh19')[0].find('img')['src'].strip() if player_row.find_all('a', class_='Table_centerCell__RWh19') and len(player_row.find_all('a', class_='Table_centerCell__RWh19')) > 1 else "N/A"
        player_name = player_row.find('a', class_='Table_profileCellAnchor__L23hq').text.strip() if player_row.find('a', class_='Table_profileCellAnchor__L23hq') else "N/A"
        player_uri = player_row.find('div', class_='Table_profileImageForeground__NOMts').find('img')['src'].strip() if player_row.find('div', class_='Table_profileImageForeground__NOMts') else "N/A"
        nation = player_row.find_all('a', class_='Table_centerCell__RWh19')[0].find('img')['alt'].strip() if player_row.find_all('a', class_='Table_centerCell__RWh19') and len(player_row.find_all('a', class_='Table_centerCell__RWh19')) > 1 else "N/A"
        
        overall_rating = player_row.find('div', class_='Table_statCellValue__0G9QI').text.strip() if player_row.find('div', class_='Table_statCellValue__0G9QI') else "N/A"
        

        player_stats.append({
            'playerName': player_name,
            'Team': team,
            'OverallRating': overall_rating,
            'playerImg': player_uri,
            'TeamImg': team_uri,
            'FlagImg': flag_uri,
            'Nation': nation
        })

        # Extract additional stats
        stats_element = player_row.find('td', class_='Table_rowBlock__Ym9Qr')
        pac = stats_element.find('div', {'data-label': 'PAC'}).find('div', class_='Table_statCellValue__0G9QI').text
        sho = stats_element.find('div', {'data-label': 'SHO'}).find('div', class_='Table_statCellValue__0G9QI').text
        pas = stats_element.find('div', {'data-label': 'PAS'}).find('div', class_='Table_statCellValue__0G9QI').text
        dri = stats_element.find('div', {'data-label': 'DRI'}).find('div', class_='Table_statCellValue__0G9QI').text
        defending = stats_element.find('div', {'data-label': 'DEF'}).find('div', class_='Table_statCellValue__0G9QI').text
        phy = stats_element.find('div', {'data-label': 'PHY'}).find('div', class_='Table_statCellValue__0G9QI').text

        player_stats[-1].update({
            'Pace': pac,
            'Shooting': sho,
            'Passing': pas,
            'Dribbling': dri,
            'Defending': defending,
            'Physicality': phy,
        })

# Write to CSV
csv_file_path = 'player_stats.csv'
fieldnames = ['playerName', 'Team', 'OverallRating','playerImg','TeamImg','FlagImg','Nation', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(player_stats)

print(f"Player stats have been written to {csv_file_path}")
