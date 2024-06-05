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
        html_table = self.extract_table(game_link)
        self.parse_html_table(html_table)

    def extract_table(self,game_link):
        pass

    def parse_html_table(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')
        data = []
        col_names = [th.text.strip() for th in rows[0].find_all('th')]
        print (col_names)
        print (len(rows))
        for row in rows[1:]:
            cols = row.find_all('td')
            # print (cols)
            cols = [col.text.strip() for col in cols]
            # print (cols)
            data.append(cols)

        df = pd.DataFrame(data)
        print ({i:col_names[i] for i in range(9)})
        df = df.rename(columns={i:col_names[i] for i in range(9)})
        # df['For_or_Against'] = df['Action'].str.contains('UNION')
        return df


if __name__ == "__main__":
    gs=GameScraper()
    f = open('./sample_data/sample_play_by_play.html','r')
    df = gs.parse_html_table(f.read())
    print (df.head())