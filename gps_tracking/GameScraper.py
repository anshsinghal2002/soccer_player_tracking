import requests
from io import StringIO
from Player import Player
import pandas as pd

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