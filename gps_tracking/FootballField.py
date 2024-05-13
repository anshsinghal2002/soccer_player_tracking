import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import animation


class FootballField:
    """
    Any input given to this class is in (Latitude,Longitude) format and internally, those values are flipped since Longitude is the supposed x value in a coordinate frame, and the Latitude is the supposed y value.
    Methods:
    - calculate_rectangle(): approximates the closest rectangle to the given field corners
    - calculate_tilt(): initialises a rotational matrix whose angle is calculated using the tilt of the field
    - add_player_data(player_data): takes a df with columns [latitude,longitude] and rows with minute:second timestamped data. Merges latitude, longitude cols into one column (longitude,latitude) with the name <player_name>, drops original and joins <player_name> series along time_stamp, and
    """
    def __init__(self, point1, point2, point3, point4):
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
        halfway_point = (self.rotated_points[2][0]+self.rotated_points[3][0])/2
        self.ax.plot([halfway_point,halfway_point], [self.rotated_points[0][1], self.rotated_points[2][1]], color='white')
        self.ax.add_patch(rect)
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
        self.ax.plot([x for x,_ in xy],[y for _,y in xy], marker='.', markersize=10, linestyle='-', linewidth=1, label=player_name)


    def animate_field(self, path,speed_up=1):
 
        # Function to update each frame
        def update(frame):
            self.ax.clear()
            minutes = int(frame // 60)
            seconds = int(frame % 60)
            minute_second = "{:02d}:{:02d}".format(minutes, seconds)
            print(minute_second)
            self.draw_field_at_time(minute_second,show=False)

        # Calculate frames and interval
        frames = 100 #len(self.coordinate_frame)
        interval = 1000 // (30 * speed_up)  # Adjust interval for speed up

        # Create animation
        anim = animation.FuncAnimation(self.fig, update, frames=frames, interval=interval, repeat=False)
        # plt.show()
        # Set up formatting for the movie files
        writer = animation.writers['ffmpeg'](fps=30*speed_up)

        # Save animation
        anim.save(path, writer=writer)

if __name__=="__main__":
    # Example usage:
    point1=(42.819707, -73.936629) #College Park Hall Field Coordinates
    point2=(42.820238, -73.935354)
    point3=(42.819647, -73.934901)
    point4=(42.819106, -73.936110)

    field = FootballField(point1, point2, point3, point4)

    field.draw_field_rotated(show=True)
