# Step-by-Step Workflow Description

## Overview

This is a brief overview of how you would go about utilizing the wrapper classes and functions given to collect data on a game to perform analysis.

## Steps

1. **Step 1**: Playertek.
   - Login details with Coach Matt Brown
   - [Playertek Setup Details](https://playertekplus.catapultsports.com/hc/en-us/articles/7443881265423-Pre-Session-Setup)

2. **Step 2**: Scraping a game
   - The GameScraper class can be used to get a game's coordinate data for all of the players. The extract table function can be used to scrape the XML play-by-play data from [the Union Men's Soccer Website](https://unionathletics.com/sports/mens-soccer/stats)
   
   ```python
   scraper = GameScraper()
   scraper.game_scraper(token,id_range,game_date,cph_field,init_time)
    ```
   - Create a CONFIG.json file in the working directory and initialize a TOKEN.
   ```json
   {"TOKEN":""}
   ```
   - To acquire token, complete a download of the raw data for any of the players' sessions on PlayerTek, and grab token from request.
   - Note down the session ID from the request as well, we will use this individual session ID and search for nearby session IDs to acquire the session data for all other players as well.

3. **Step 3**: Implementation
   - Once everything is in place, refer to the example usages in `main.py`
   - Example Framework for loading in data:
      ```python
      token = load_config()['TOKEN']
      sessionID=3471220
      id_range = range(sessionID-200,sessionID+200)
      play_by_play = "https://unionathletics.com/sports/mens-soccer/stats/2023/elmira/boxscore/25193"

      #cph field corner flag coordinates (Look up coordinates manually if at game, otherwise utilize sattelite view of google maps for any field)
      point1=(42.819707, -73.936629)
      point2=(42.820238, -73.935354)
      point3=(42.819647, -73.934901)
      point4=(42.819106, -73.936110)

      # play by play data is scraped at initialization of Field obj given correct link
      cph_field = FootballField(point1, point2, point3, point4,play_by_play)
      cph_field.draw_field_rotated()

      #elmira game
      game_date = datetime.datetime(2023, 10, 3)
      init_time = datetime.time(17,00) # accurate init time should be recorded manually moving forward
      scraper = GameScraper()
      scraper.game_scraper(token,id_range,game_date,cph_field,init_time)
      save(cph_field,'./sample_data/<game>.pkl')
      ```

4. **Step 4**: Generating Insights
   - Utilise the following example usage to generate evaluative metrics, a 2D replay of the game with togglable metric display and graphs to visualize in game metrics and outcomes.
   ```python
   f = open('./sample_data/<game>.pkl','rb')
   cph_field = pickle.load(f)
   # if the game was delayed by 5 mins, half ended at 53:00, started at 69:00 and final whistle was at 118:00
   cph_field.alter_match_times("5:00","53:00","69:00","118:00")
   # removes subs, can be improved
   cph_field.clean_coordinate_frame()
   # runs evaluation for all the metrics being studied
   cph_field.evaluate_metrics()
   cph_field.animate_field('./sample_outputs/<video_name>.mp4',show_def_line=True)
   cph_field.reorder_df()
   cph_field.generate_binary_columns()
   cph_field.generate_metric_graph('def_line_height')

   ```

## Tips and Considerations

- Once real time match half start/end are recorded, FootbalField implementation should be updated to cater to both halves separately to accomodate for added time in first half. Currently, the alter time method is able to trim the time properly, however also overlooks added time in both halves. An updated implementation with seperate coordinate frames for both halves will allow to retain this data as well as linearize the second half.

## Troubleshooting

- Looking into why some phases of the game do not showcase all 10 outfield players; missing data from PlayerTek modules or players who weren't given one on the pitch at certain times.

## Conclusion

This is the beginning of an exciting project. There are lots of cool directions that data insight can take with the data available at Union's Soccer team, and building off of this ground level implementation, solidifying data collection pipelines and practices will make for an abundant amount of reliable data and feature generation which will allow for a plethora of fruitful visualizations and metric revelations for the Soccer team in coming years.