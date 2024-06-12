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
   - Sub-step or additional details if needed.

3. **Step 3**: Description of the third step.
   - Sub-step or additional details if needed.
   - Sub-step or additional details if needed.

## Tips and Considerations

- Once real time match half start/end are recorded, FootbalField implementation should be updated to cater to both halves separately to accomodate for added time in first half.

## Troubleshooting

- Looking into why some phases of the game do not showcase all 10 outfield players; missing data from PlayerTek modules or players who weren't given one on the pitch at certain times.

## Conclusion

This is the beginning of an exciting project. There are lots of cool directions that data insight can take with the data available at Union's Soccer team, and building off of this ground level implementation, solidifying data collection pipelines and practices will make for an abundant amount of reliable data and feature generation which will allow for a plethora of fruitful visualizations and metric revelations for the Soccer team in coming years.