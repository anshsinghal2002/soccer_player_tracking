from datetime import datetime
from FootballField import FootballField
from Player import Player
import pandas as pd
from GameScraper import GameScraper
import pickle

def test_field_animation():
    player_1= Player('Ansh',pd.read_csv('./sample_data/sample_raw_session_data.csv'))
    player_1.show_data()
    point1=(42.819707, -73.936629) #College Park Hall Field Coordinates
    point2=(42.820238, -73.935354)
    point3=(42.819647, -73.934901)
    point4=(42.819106, -73.936110)
    field = FootballField(point1, point2, point3, point4)

    field.add_player_data(player_1)
    field.animate_field('test.mp4',0.5)

def test_scraping():
    slu_field = FootballField((44.584161, -75.163275),(44.585157, -75.163222),(44.585152, -75.162214),(44.584137, -75.162274))
    token = "76112:086d14180a56ebca246a67fd1003547d9353f851e1e7d9a7d2f15ce25dab0162"
    id_range=range(3561600,3561900)
    game_date = datetime.datetime(2023, 10, 18)
    init_time = datetime.time(16)
    scraper = GameScraper()
    scraper.game_scraper(token,id_range,game_date,slu_field,init_time)
    return slu_field

def save(obj,path):
    filehandler = open()

if __name__=="__main__":
    test_field_animation()
    slu_field = test_scraping()
