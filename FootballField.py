import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import animation
from GameScraper import GameScraper
import pickle
from Utils import seconds_to_minsec,coordinates_to_yds

class FootballField:
    """
    Any input given to this class is in (Latitude,Longitude) format and internally, those values are flipped since Longitude is the supposed x value in a coordinate frame, and the Latitude is the supposed y value.
    Methods:
    - calculate_rectangle(): approximates the closest rectangle to the given field corners
    - calculate_tilt(): initialises a rotational matrix whose angle is calculated using the tilt of the field
    - add_player_data(player_data): takes a df with columns [latitude,longitude] and rows with minute:second timestamped data. Merges latitude, longitude cols into one column (longitude,latitude) with the name <player_name>, drops original and joins <player_name> series along time_stamp, and
    """
    def __init__(self, point1, point2, point3, point4,link=None):
        self.points = [(x,y) for y,x in [point1, point2, point3, point4]] #flipping latitude-longitude to x,y
        self.coordinate_frame = pd.DataFrame({'Minute:Second':["{:02d}:{:02d}".format(minutes, seconds) for minutes in range(0,60) for seconds in range(0,150)]})
        self.players={}
        self.calculate_rectangle() #calculates a still tilted, but now geometric rectangle
        self.calculate_rotational_angle() #calculates tilt of fielTrued from bottom edge (edge between point3 and point4)
        self.calculate_rotational_matrix() #calculates the matrix which any point can be multiplied by to yield a rotated point
        self.translation_factor = self.points[3] #sets the bottom left corner as the expected origin for the coordinate system
        self.translated_points = [self.translate_point(point) for point in self.points] #
        self.rotated_points = [self.rotate_point(point) for point in self.translated_points]
        self.fig,self.ax = plt.subplots(figsize=(12, 9))
        self.init_metrics_table
        if link!=None:
            self.add_play_by_play(link)
        else:
            self.has_play_by_play=False

    def calculate_rectangle(self):
        """
        Adjusts self.points to calculate a rectangle to rely on as coordinate axes and relabel self.points (Assumes measured reliability of one of the lines of the field)
        """
        # centre = (sum([x for x, _ in self.points]) / 4, sum([y for _, y in self.points]) / 4)
        self.field_len = math.dist(self.points[2],self.points[3])#sum((math.dist(self.points[0], self.points[1]), math.dist(self.points[2], self.points[3]))) / 2
        self.field_wid = math.dist(self.points[1],self.points[2])#sum((math.dist(self.points[0], self.points[3]), math.dist(self.points[2], self.points[1]))) / 2
        m_bottom_edge = (self.points[2][1]-self.points[3][1])/(self.points[2][0]-self.points[3][0])
        self.m = m_bottom_edge
        m_side_edge = -1/m_bottom_edge
        translation_vec_wid_down = (self.field_wid/math.sqrt(1+m_side_edge**2),self.field_wid*m_side_edge/math.sqrt(1+m_side_edge**2))
        bottom_left=self.points[3]
        top_left = (bottom_left[0]-translation_vec_wid_down[0],bottom_left[1]-translation_vec_wid_down[1])
        translation_vec_len = (self.field_len/math.sqrt(1+m_bottom_edge**2),self.field_len*m_bottom_edge/math.sqrt(1+m_bottom_edge**2))
        top_right = (top_left[0]+translation_vec_len[0],top_left[1]+translation_vec_len[1])
        bottom_right = (bottom_left[0]+translation_vec_len[0],bottom_left[1]+translation_vec_len[1])
        self.points = [top_left,top_right,bottom_right,bottom_left]

    # def draw_player_90_map(self,player_name):
    #     self.players[player_name].plot_on_map()


    def translate_point(self,point):
        return (point[0]-self.translation_factor[0],point[1]-self.translation_factor[1])

    def rotate_point(self,point):
        """
        Given a point (x, y), rotates it using self.rotational_matrix
        """
        point_array = np.array(point)
        rotated_point = np.dot(self.rotational_matrix, point_array)

        return rotated_point

    def calculate_rotational_matrix(self):
        """
        Calculates a matrix, which when a 2d point is multipled by, will rotate the point's frame of reference
        """

        # Calculate sine and cosine of the angle
        cos_angle = np.cos(self.angle)
        sin_angle = np.sin(self.angle)

        # Construct the rotational matrix
        self.rotational_matrix = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])



    def calculate_rotational_angle(self):
        """
        Calculates the angle that the bottom edge of the field is tilted
        Instantiate self.angle as this angle
        """
        self.angle = -math.atan(self.m)

    def draw_field(self):
        plt.plot([x for x,_ in self.points], [y for _,y in self.points], marker='o', linestyle='-')

    def draw_field_rotated(self,show=False):
        # fig, ax = plt.subplots()
        rect = patches.Rectangle((self.rotated_points[3][0], self.rotated_points[3][1]), self.field_len,self.field_wid,  facecolor='green', edgecolor='black',alpha=0.5)
        center_circle = patches.Circle((sum([i[0] for i in self.rotated_points])/4, sum([i[1] for i in self.rotated_points])/4), self.field_wid / 10, color='white', fill=False)
        halfway_point = (self.rotated_points[2][0]+self.rotated_points[3][0])/2
        penalty_area_height = 0.15*self.field_len
        penalty_area_width = 0.4*self.field_wid
        left_penalty_area = patches.Rectangle((self.rotated_points[3][0], self.field_wid/2-penalty_area_width/2), penalty_area_height, penalty_area_width, edgecolor='white', fill=False)
        right_penalty_area = patches.Rectangle((self.rotated_points[1][0] - penalty_area_height, self.field_wid/2-penalty_area_width/2), penalty_area_height, penalty_area_width, edgecolor='white', fill=False)
        self.ax.plot([halfway_point,halfway_point], [self.rotated_points[0][1], self.rotated_points[2][1]], color='white')
        self.ax.add_patch(rect)
        self.ax.add_patch(center_circle)
        self.ax.add_patch(left_penalty_area)
        self.ax.add_patch(right_penalty_area)
        min_x = min([point[0] for point in self.rotated_points])
        max_x = max([point[0] for point in self.rotated_points])
        min_y = min([point[1] for point in self.rotated_points])
        max_y = max([point[1] for point in self.rotated_points])
        self.ax.set_xlim(min_x,max_x)
        self.ax.set_ylim(min_y,max_y)

        if show:
            plt.show()

    def combine_lat_long(self,lat,long):
        return ((long,lat)) #flip because x,y is longitude latitude

    def draw_player_90(self,player_name,show=True):
        xy = self.coordinate_frame[player_name].dropna().values
        self.draw_field_rotated()
        self.ax.plot([x for x,_ in xy],[y for _,y in xy], marker='.', markersize=10, linestyle='-', linewidth=1, color='white', markerfacecolor='black', markeredgecolor='white', alpha=0.5)
        self.fig.suptitle('Player 90')
        if show:
            plt.show()

    def add_player_data(self,player):
        self.players.update({player.player_name:player})
        player_coords = player.data[['Minute:Second','Latitude','Longitude']]
        player_coords[player.player_name]=player_coords.apply(lambda x: self.combine_lat_long(x.Latitude,x.Longitude),axis=1)
        self.test_var2=player_coords[player.player_name].values
        player_coords[player.player_name]=player_coords[player.player_name].apply(lambda x: self.translate_point(x))
        player_coords[player.player_name]=player_coords[player.player_name].apply(lambda x: self.rotate_point(x))
        self.coordinate_frame = self.coordinate_frame.merge(right=player_coords[['Minute:Second',player.player_name]],on='Minute:Second',how='outer')
        self.coordinate_frame.head()

    def draw_field_at_time(self,time_stamp,show=True):
        self.draw_field_rotated()
        for player_name in self.players:
            try:
                self.draw_player_at_time(time_stamp,player_name)
            except Exception as e:
                pass
        self.fig.suptitle(f'Field at {time_stamp}')
       
        if show:
            plt.show()

    def draw_player_at_time(self,time_stamp,player_name):
        xy = self.coordinate_frame.loc[self.coordinate_frame['Minute:Second'] == time_stamp][player_name].values
        self.ax.plot([x for x,_ in xy],[y for _,y in xy], marker='.', markersize=15, linestyle='-', linewidth=1, label=player_name)

    def timestamp_to_seconds(self,x):
        mins,seconds=x.split(':')
        mins=int(mins)
        seconds=int(seconds)
        if x[0]=='-':
            return mins*60-seconds
        else:
            return mins*60+seconds
        
    def animate_field(self, path,speed_up=1,max_frames=140*60,show_def_line=False):
        
        previous_notification = ""
        # Function to update each frame
        def update(frame):
            nonlocal previous_notification
            self.ax.clear()
            minutes = int(frame // 60)
            seconds = int(frame % 60)
            minute_second = "{:02d}:{:02d}".format(minutes, seconds)
            print(minute_second)
            self.draw_field_at_time(minute_second,show=False)

            play_text.set_text(current_notification[0])
            self.ax.add_artist(play_text)
            
            # Check if there is a play-by-play entry for the current timestamp
            if self.has_play_by_play and minute_second in self.play_by_play['Clock'].values:
                play_desc = self.play_by_play.loc[self.play_by_play['Clock'] == minute_second, 'Play'].values[0]
                current_notification[0] = f"{minute_second} - {play_desc}"

            if show_def_line:
                if 'def_line_height' in self.coordinate_frame:
                    def_height = self.coordinate_frame['def_line_height'].iloc[frame]
                    if not pd.isna(def_height):
                        self.ax.axvline(x=def_height, color='red', linestyle='--', linewidth=2)
                        self.ax.text(0.5, def_height, ' Defensive Line ', color='red', fontsize=12, ha='center', va='center')


        # Calculate frames and interval

        frames = min(self.coordinate_frame['Minute:Second'].apply(lambda x: self.timestamp_to_seconds(x)).max(),max_frames)
        print ("Total Frames: ",frames)
        interval = 1000 // (30 * speed_up)  # Adjust interval for speed up

        # Create a text element for play-by-play notifications
        current_notification = [""]  # List to retain notification text across frames
        play_text = self.ax.text(0.02, 0.95, 'test', transform=self.ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
       
        # Create animation
        anim = animation.FuncAnimation(self.fig, update, frames=frames, interval=interval, repeat=False)
        # plt.show()
        # Set up formatting for the movie files
        writer = animation.writers['ffmpeg'](fps=30*speed_up)

        # Save animation
        anim.save(path, writer=writer)

    def add_play_by_play(self,play_by_play_link):
        """
        Adds play_by_play data to the field object
        play_by_play df must be derived from GameSraper.play_by_play_scraper(link)
        """
        self.has_play_by_play = True
        gs = GameScraper()
        try:
            self.play_by_play = gs.play_by_play_scraper(play_by_play_link)
        except:
            print ("Could not scrape play by play")
            self.has_play_by_play = False

    def clean_coordinate_frame(self, threshold=0.00065):
        """
        Sets all entries in the coordinate frame with a y-coordinate value greater than the threshold to NaN.
        Accounts for substitute bench. Reduces to only on-field players for easier metric extraction.
        """
        def clean_value(value):
            if value[1] > threshold:
                return np.nan
            return value

        for player_name in self.players:
            self.coordinate_frame[player_name] = self.coordinate_frame[player_name].apply(clean_value)    

    def init_metrics_table(self):
        self.metrics = pd.DataFrame({'Minute:Second':["{:02d}:{:02d}".format(minutes, seconds) for minutes in range(0,150) for seconds in range(0,60)]})

    def evaluate_defensive_line_height(self,first_half_left=True):

        def calculate_defensive_height(row):
            timestamp_seconds = self.timestamp_to_seconds(row['Minute:Second'])
            # x_coords = [
            #     row[player_name][0]
            #     for player_name in self.players
            #     if isinstance(row[player_name], tuple)]
            x_coords=[]
            for player_name in self.players:
                try:
                    x_coords.append(row[player_name][0])
                except:
                    pass
            if first_half_left:
                if timestamp_seconds <= 45 * 60:
                    return min(x_coords)
                else:
                    return self.field_len-max(x_coords)
            else:
                if timestamp_seconds <= 45 * 60:
                    return self.field_len-max(x_coords)
                else:
                    return min(x_coords)
        
        self.coordinate_frame['def_line_height'] = self.coordinate_frame.apply(calculate_defensive_height, axis=1)


    def evaluate_team_length(self):
        def calculate_team_length(row):
            timestamp_seconds = self.timestamp_to_seconds(row['Minute:Second'])
            # x_coords = [
            #     row[player_name][0]
            #     for player_name in self.players
            #     if isinstance(row[player_name], tuple)]
            x_coords=[]
            for player_name in self.players:
                try:
                    x_coords.append(row[player_name][0])
                except:
                    pass
            return coordinates_to_yds(max(x_coords)-min(x_coords))
        
        self.coordinate_frame['team_len'] = self.coordinate_frame.apply(calculate_team_length, axis=1)

    def reorder_df(self):
        df_sorted = self.coordinate_frame.sort_values(by='timestamp')
        
        df_sorted = df_sorted.reset_index(drop=True)
    
        self.coordinate_frame = df_sorted

    def evaluate_team_width(self):
        def calculate_team_width(row):
            timestamp_seconds = self.timestamp_to_seconds(row['Minute:Second'])
            y_coords=[]
            for player_name in self.players:
                try:
                    y_coords.append(row[player_name][1])
                except:
                    pass
            return coordinates_to_yds(max(y_coords)-min(y_coords))
        
        self.coordinate_frame['team_wid'] = self.coordinate_frame.apply(calculate_team_width, axis=1)

    def generate_binary_columns(self):
        self.play_by_play['union_goal'] = (self.play_by_play['Union - Play Description'].notnull()) & (self.play_by_play['Play'].str.contains('GOAL', case=True))
        self.play_by_play['away_goal'] = (self.play_by_play['Union - Play Description'].isnull()) & (self.play_by_play['Play'].str.contains('GOAL', case=True))
        self.play_by_play['union_shot'] = (self.play_by_play['Union - Play Description'].notnull()) & (self.play_by_play['Play'].str.contains('shot', case=False))
        self.play_by_play['away_shot'] = (self.play_by_play['Union - Play Description'].isnull()) & (self.play_by_play['Play'].str.contains('shot', case=False))

        binary_columns = ['union_goal', 'away_goal', 'union_shot', 'away_shot']
        self.play_by_play[binary_columns] = self.play_by_play[binary_columns].astype(int)

        print(self.play_by_play)

    def generate_metric_graph(self, metric_name,save_path=None):
        """
        Given a metric, plots a time vs metric graph for the entirety of the game, and uses the binary columns from the play_by_play to show in game actions with their corresponding time_stamps
        For a Union Goal, a G appears above the metric line in Red, for an away goal a G appears above the metric line in black
        """
        metric_table = self.coordinate_frame[['Minute:Second', 'timestamp', metric_name]].copy()
        
        metric_table['timestamp'] = metric_table['Minute:Second'].apply(self.timestamp_to_seconds)
        
        metric_table['minute'] = metric_table['timestamp'] // 60
        
        # Aggregate metric_name by 'minute' and calculate mean
        metric_table = metric_table.groupby('minute').agg({metric_name: 'mean'}).reset_index()

        binary_columns = ['union_goal', 'away_goal', 'union_shot', 'away_shot']
        self.play_by_play['minute']=self.play_by_play['Clock'].apply(lambda x: int(x.split(':')[0]))
        play_by_play_aggregated = self.play_by_play.groupby('minute')[binary_columns].sum().reset_index()

        
        # Plot the graph
        plt.figure(figsize=(12, 6))
        plt.plot(metric_table['minute'], metric_table[metric_name], linestyle='-', color='blue', label=f'Average {metric_name}')
        plt.axvline(x=45, color='b', linestyle='--', linewidth=1.5, label='Halftime')
        goals_scored=0
        goals_conceded=0
        for idx, row in play_by_play_aggregated.iterrows():
            minute = row['minute']
            if row['union_goal'] > 0:
                goals_scored+=1
                plt.axvline(x=minute, linestyle='--', color='g',linewidth=1.5, label=f'{goals_scored}-{goals_conceded}')
            if row['away_goal'] > 0:
                goals_conceded+=1
                plt.axvline(x=minute, linestyle='--', color='r',linewidth=1.5, label=f'{goals_scored}-{goals_conceded}')

        plt.xlabel('Minute')
        plt.ylabel(metric_name)
        plt.title(f'Minute vs {metric_name} Graph')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Save the plot if a save_path is provided
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show()

    def evaluate_metrics(self):
        self.evaluate_defensive_line_height()
        self.evaluate_team_length()
        self.evaluate_team_width()

    def evaluate_average_formation(self):
        pass

    def evaluate_third_breakdowns(self, vertical=False):
        """
        Present a visualization with a percentage breakdown of the vertical/horizontal thirds of the pitch
        """
        pass
    def evaluate_average_team_height(self):
        pass

    def alter_match_times(self,actual_game_start="00:00",end_first_half="45:00",start_second_half="60:00",end_second_half="105:00"):
        self.coordinate_frame = self.coordinate_frame[self.coordinate_frame['Minute:Second'].str.split(':').str[1].astype(int) <= 59]

        game_start_adjustment = self.timestamp_to_seconds(actual_game_start)
        first_half_end_seconds = self.timestamp_to_seconds(end_first_half)
        start_second_half_adjustment = self.timestamp_to_seconds(start_second_half)
        game_end_seconds = self.timestamp_to_seconds(end_second_half)

        self.coordinate_frame['timestamp']=self.coordinate_frame['Minute:Second'].apply(lambda x: self.timestamp_to_seconds(x))
        first_half = self.coordinate_frame[(self.coordinate_frame['timestamp']>=game_start_adjustment)&(self.coordinate_frame['timestamp']<game_start_adjustment+45*60)]

        first_half['timestamp']=first_half['timestamp'].apply(lambda x: x-game_start_adjustment)
        first_half['Minute:Second']=first_half['timestamp'].apply(lambda x: seconds_to_minsec(x))

        second_half = self.coordinate_frame[(self.coordinate_frame['timestamp']>=start_second_half_adjustment)&(self.coordinate_frame['timestamp']<start_second_half_adjustment+45*60)]
        second_half['timestamp']=second_half['timestamp'].apply(lambda x: x-start_second_half_adjustment+45*60)
        second_half['Minute:Second']=second_half['timestamp'].apply(lambda x: seconds_to_minsec(x))

        self.coordinate_frame = pd.concat([first_half,second_half])

if __name__=="__main__":
    # Example usage:
    f = open('./sample_data/elmira_game.pkl','rb')
    cph_field = pickle.load(f)
    cph_field.alter_match_times("5:00","53:00","69:00","118:00")
    cph_field.clean_coordinate_frame()
    cph_field.evaluate_metrics()
    # cph_field.animate_field('./sample_outputs/elmiras_with_notifs.mp4',show_def_line=True)
    cph_field.reorder_df()
    cph_field.generate_binary_columns()
    for metric in ['def_line_height','team_len','team_wid']:
        cph_field.generate_metric_graph(metric,f'./sample_outputs/{metric}_vs_elmira_graph')
