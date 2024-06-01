import requests
from io import StringIO
from Player import Player
import pandas as pd
from bs4 import BeautifulSoup

class GameScraper():
    def __init__(self) -> None:
        pass
    def game_scraper(self,token,id_range,game_date,field,init_time):
        url = "https://apius.playertek.com//webinterface/RawDataService.php?token="+token+"&sessionID="
        for session_id in id_range:
            sp_url = url+str(session_id)
            response = requests.get(sp_url)
            if response.status_code == 200:
                csv_data = response.text
                # Now csv_data contains the CSV content from the URL
                csv_file = StringIO(csv_data)
                try:
                    player_csv = pd.read_csv(csv_file)
                    player_to_add = Player('player_'+str(session_id),player_csv,init_time)
                    print(player_to_add.data['Minute:Second'].min())
                    # if player_to_add.game_date==game_date:
                    field.add_player_data(player_to_add)
                except Exception as e:
                    print ('error',e)
                    pass
            else:
                print("Failed to fetch data:", response.status_code)
    
    def play_by_play_scraper(self,game_link="https://unionathletics.com/sports/mens-soccer/stats/2023/-15-suny-oneonta/boxscore/25179"):
        html_table = etract_table()



def parse_html_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'Time_Stamp', 1: 'Action'})
    df['For_or_Against'] = df['Action'].str.contains('UNION')
    return df[['Time_Stamp', 'Action', 'For_or_Against']]

# Example usage:
html = """
Your HTML table here
"""
df = parse_html_table(html)
print(df)



'''
<tr>
                                                
                                                    <td>
                                                00:00
                                                </td>
                                                <td class="text-right hide-on-medium-down" style="width:40%">
                                                    
                                                </td>
                                                
                                                    <td class="hide-on-medium-down"></td>
                                                    <td class="hide-on-medium-down"></td>
                                                    <td class="hide-on-medium-down"></td>
                                                
                                                <td class="hide-on-medium-down" style="width:40%">
                                                    Perry, Jacob at goalie for Union (NY)
                                                </td>   
                                                <td aria-hidden="true" class="hide-on-large text-center text-bold" style="min-width:50px">
                                                    
                                                </td>
                                                
                                                    <td aria-hidden="true" class="hide-on-large play team"></td>
                                                
                                                <td aria-hidden="true" class="hide-on-large">Perry, Jacob at goalie for Union (NY)</td>                                             
                                            </tr>
                                             
                                            <tr>
                                                
                                                    <td>
                                                00:00
                                                </td>
                                                <td class="text-right hide-on-medium-down" style="width:40%">
                                                    Hanna, Nate at goalie for SUNY Oneonta
                                                </td>
                                                
                                                    <td class="hide-on-medium-down"></td>
                                                    <td class="hide-on-medium-down"></td>
                                                    <td class="hide-on-medium-down"></td>
                                                
                                                <td class="hide-on-medium-down" style="width:40%">
                                                    
                                                </td>   
                                                <td aria-hidden="true" class="hide-on-large text-center text-bold" style="min-width:50px">
                                                    
                                                </td>
                                                
                                                    <td aria-hidden="true" class="hide-on-large play "></td>
                                                
                                                <td aria-hidden="true" class="hide-on-large">Hanna, Nate at goalie for SUNY Oneonta</td>                                             
                                            </tr>
'''