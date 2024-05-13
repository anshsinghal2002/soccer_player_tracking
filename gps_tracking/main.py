from FootballField import FootballField
from Player import Player
import pandas as pd



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
    pass

if __name__=="__main__":
    test_field_animation()
