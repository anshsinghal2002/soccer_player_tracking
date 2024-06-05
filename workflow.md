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

- Any tips or considerations to keep in mind while following the workflow.
- Additional resources or links for further information.

## Troubleshooting

- Common issues users might encounter and how to resolve them.
- Troubleshooting tips or techniques.

## Conclusion

Summarize the workflow and highlight any key points or takeaways.
