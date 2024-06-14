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

                    # if player_to_add.game_date==game_date:
                    field.add_player_data(player_to_add)
                except Exception as e:
                    print ('error',e)
                    pass
            else:
                print("Failed to fetch data:", response.status_code)
    
    def play_by_play_scraper(self,game_link="https://unionathletics.com/sports/mens-soccer/stats/2023/-15-suny-oneonta/boxscore/25179"):
        """
        Given a link to a Union College Game box score, returns the play-by-play in the form of a DataFrame Obj
        """
        html_tables = self.extract_table(game_link)
        first_half_plays = self.parse_html_table(html_tables[0])
        second_half_plays = self.parse_html_table(html_tables[1])
        return self.join_halves(first_half_plays,second_half_plays)
    
    def join_halves(self,half1,half2):
        return pd.concat([half1,half2])

    def extract_table(self,game_link):
        response = requests.get(game_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        period_1_section = str(soup.find('section', id='period-1'))
        period_2_section = str(soup.find('section', id='period-2'))
        return period_1_section,period_2_section

    def parse_html_table(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')
        data = []
        col_names = [th.text.strip() for th in rows[0].find_all('th')]
        for row in rows[1:]:
            cols = row.find_all('td')
            # print (cols)
            cols = [col.text.strip() for col in cols]
            # print (cols)
            data.append(cols)

        df = pd.DataFrame(data)
        # print ({i:col_names[i] for i in range(9)})
        df = df.rename(columns={i:col_names[i] for i in range(9)})
        # df['For_or_Against'] = df['Action'].str.contains('UNION')
        return df


if __name__ == "__main__":
    # gs=GameScraper()
    # f = open('./sample_data/sample_play_by_play.html','r')
    # df = gs.parse_html_table(f.read())
    # print (df['UNION - Play Description'])
    gs = GameScraper()
    # f = open('./sample_data/sample_play_by_play.html','w')  
    print(gs.play_by_play_scraper('https://unionathletics.com/sports/mens-soccer/stats/2023/ithaca/boxscore/25189'))
