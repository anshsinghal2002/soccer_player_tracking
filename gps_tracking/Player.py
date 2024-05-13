
import datetime
import pandas as pd

class Player:
  def __init__(self,player_name,raw_gps,init_time=None):
    self.player_name=player_name
    self.data=raw_gps
    self.data['DateTime'] = self.data['Excel Timestamp'].apply(lambda x: self.excel_timestamp_to_datetime(x))
    if init_time==None:
      self.init_time = self.data['DateTime'][0].time()
    else:
      self.init_time=init_time
    self.game_date = self.data['DateTime'][0].date()
    self.data['Minute:Second']=self.data['DateTime'].apply(lambda x: self.datetime_to_minute(x.time(),self.init_time))
    self.data = self.data.groupby('Minute:Second').agg({' Speed': 'mean', ' Latitude': 'mean', ' Longitude': 'mean',' Accel X':'mean', ' Accel Y':'mean',' Accel Z':'mean'}).reset_index()
    self.data=self.data.rename(columns={column: str.strip(column) for column in self.data.columns})

  def show_data(self):
    print (self.data.head())

  def excel_timestamp_to_datetime(self,timestamp):
    """
    Convert an Excel date serial number to a datetime object.

    Args:
    timestamp (float): Excel timestamp in serial format.

    Returns:
    datetime.datetime: Corresponding datetime object.
    """
    base_date = datetime.datetime(1899, 12, 30)  # Excel base date for Windows
    days = int(timestamp)
    fraction_of_day = timestamp - days
    time_of_day = datetime.timedelta(days=fraction_of_day)
    result_date = base_date + datetime.timedelta(days=days) + time_of_day
    return result_date

  def datetime_to_minute(self,x,init_time):
    """
    Convert a date time value to a minute:second format
    """
    time_diff = datetime.datetime.combine(datetime.date.min, x) - datetime.datetime.combine(datetime.date.min, init_time)

    total_seconds = time_diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    minute_second = "{:02d}:{:02d}".format(minutes, seconds)

    return minute_second
  


if __name__=="__main__":
  player_1= Player('Ansh',pd.read_csv('./sample_data/sample_raw_session_data.csv'))
  player_1.show_data()