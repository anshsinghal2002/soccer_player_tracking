import datetime
from FootballField import FootballField
from Player import Player
import pandas as pd
from GameScraper import GameScraper
import pickle
import json

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

def test_scraping(token):
    print(token)
    point1=(42.819707, -73.936629)
    point2=(42.820238, -73.935354)
    point3=(42.819647, -73.934901)
    point4=(42.819106, -73.936110)

    cph_field = FootballField(point1, point2, point3, point4)
    cph_field.draw_field_rotated()
    token = token
    #3343393
    id_range=range(3343300,3343500)
    game_date = datetime.datetime(2023, 9, 13)
    init_time = datetime.time(16,30)
    scraper = GameScraper()
    scraper.game_scraper(token,id_range,game_date,cph_field,init_time)
    return cph_field

def save(obj,path):
    filehandler = open(path,'wb')
    pickle.dump(obj,filehandler)
    filehandler.close()

def load_config():
    f = open('CONFIG.json','r')
    return json.load(f)

def test_framework():
    token = load_config()['TOKEN']
    sessionID=3471220
    id_range = range(sessionID-200,sessionID+200)
    play_by_play = "https://unionathletics.com/sports/mens-soccer/stats/2023/elmira/boxscore/25193"

    #cph
    point1=(42.819707, -73.936629)
    point2=(42.820238, -73.935354)
    point3=(42.819647, -73.934901)
    point4=(42.819106, -73.936110)
    cph_field = FootballField(point1, point2, point3, point4,play_by_play)
    cph_field.draw_field_rotated()

    #ithica game
    game_date = datetime.datetime(2023, 10, 3)
    init_time = datetime.time(17,00)
    scraper = GameScraper()
    scraper.game_scraper(token,id_range,game_date,cph_field,init_time)
    save(cph_field,'./sample_data/elmira_game.pkl')

    # Based on video: game_start = 5', half_end = 53', half start = 69', game_end=118'
    return cph_field

if __name__=="__main__":
    # test_field_animation()
    # cph_field = test_scraping(load_config()['TOKEN'])
    # save(cph_field,'sample_filled_field_cph.pkl')
    f = open('./sample_data/elmira_game.pkl','rb')
    cph_field = pickle.load(f)
    # cph_field = test_framework()
    cph_field.alter_match_times("5:00","53:00","69:00","118:00")
    cph_field.animate_field('./sample_outputs/elmiras_altered_time.mp4')
    # cph_field = test_framework()
