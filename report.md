# Report intended for Nicholas Webb

## Summary

Over the course of this indpendent study I was able to accomplish the following:

- Successfully **inquire about and onboard myself** with the different sources of data made available by Coach Matt Brown
  - 10 Hz GPS Data from Player trackers (all games and training sessions)
  - Player fitness and wellness survey form data (all games and training sessions)
  - Union Soccer Website - play by play annotation
  - Coach recommended an acceptable average build-up time of 30 seconds, to be taken into account while engineering features with a rolling window
- Performed **initial exploratory data analysis and cleaning** on player fitness and wellness survey data in this [initial data loading notebook](https://colab.research.google.com/drive/1ggifz3PwI9fvgWVSsqz_rDPON5w8WDQo) which goes into detail regarding the data sources.
- Create a reproduceable framework and well documented structure to load in [player tracking data](https://playertekplus.catapultsports.com/hc/en-us/categories/7437070143375-PlayerTek-Software) from any session and compile it for all players in a session.
  - Initally tested and developed framework on [this notebook](https://colab.research.google.com/drive/1bk9DZoagOEQ6YeCIBqD1XmLjd5WBl_X8)
  - Converted raw data to workable timestamps and **applied various geometric transformations** to achieve player positional data in the form of a contained coordinate frame within the context of a defineable Soccer Pitch.
  - Adapted a method to **scrape raw player data** from the PlayerTek website and compile it.
  - Fixed distortion to player coordinates due to longitude curvature.
  - **Packaged** coordinate translation and rotation in a `FootballField` class to allow for easily loading a training/game session instance for all players into a pitch representation. 
  - **Packaged** player data scraping framework into a `GameScraper` class, intending on expanding this to scrape and compile other relevant data from sources such as the Union Soccer Website.
  - Created methods to **draw a player's coordinates** for a given timestamp, and reduced mean based sampling to 1Hz for more reliable positional readings.
  - Created functionality to adjust game start time and account for halftime interval.
  - Utilised existing methods to **animate the events of a soccer pitch** completely using the player positional data, incredibly useful for post game analysis, as well as sanity checks during subsequent development of project.
  - **Developed reliable scraping for play by play annotation** from Union Soccer Website, and extracted a plethora of binary features representing in game outcomes.
  - **Conducted research** to justify creation of metrics from available positional data, listed out achievable suggested future work, with clear guidelines and scope as well as links to all relevant papers for easy implementation and production; listed out in `research.md`.
  - Generated initial crop of in game metrics. Developed methods to **showcase metrics in an insightful visual manner**.
  - **Delivered end-to-end functionality** and produced a workflow to go from one link to a fully loaded in session with available metrical insights through auto generated graphs, and a robust video containing a display of all available metrics, birds eye view game replay, in game action notifications. Workflow described in `workflow.md`.
  - **Documented** iterations of various outputs, and sample data for ready testing and further development. (Sample outputs pertaining to Elmiras vs Union at CPH Field (Union) which ended in a 5-0 win for Union)
  - **Prepared** examples of usage in `main.py`.

