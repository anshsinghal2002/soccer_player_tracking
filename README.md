# README

## Overview

This repository contains the work and outcomes of an independent study conducted by Ansh Singhal under the guidance of Coach Matt Brown and Professor Nicholas Webb. The study focuses on analyzing player performance data, generating metrics, and developing a framework to automate data extraction and visualization for soccer matches and training sessions.

## Table of Contents
- [Summary](#summary)
- [Data Sources](#data-sources)
- [Framework and Tools](#framework-and-tools)
- [Methods and Functionality](#methods-and-functionality)
- [Recommendations](#recommendations)
- [Future Work](#future-work)

## Summary

Over the course of this independent study, the following achievements were made:

- Successfully onboarded and accessed various data sources provided by Coach Matt Brown.
- Performed exploratory data analysis and cleaning on player fitness and wellness survey data.
- Developed a reproducible framework for loading and processing player tracking data from multiple sessions.
- Implemented geometric transformations to convert raw positional data into a defined coordinate frame.
- Created classes to facilitate data scraping, transformation, and visualization.
- Generated initial metrics and showcased them through insightful visualizations.
- Delivered an end-to-end workflow for loading session data and producing analytical insights and visualizations.
- Documented all outputs and provided sample data for testing and development.

## Data Sources

The data sources used in this study include:

- **10 Hz GPS Data** from player trackers (all games and training sessions).
- **Player fitness and wellness survey data** (all games and training sessions).
- **Union Soccer Website** for play-by-play annotation.

## Framework and Tools

The framework and tools developed during this study include:

- A well-documented structure to load player tracking data and compile it for all players in a session.
- A `FootballField` class for coordinate translation and rotation.
- A `GameScraper` class for scraping and compiling player data from the PlayerTek website and other relevant sources.
- Methods to draw player coordinates and animate soccer pitch events.
- Methods to adjust game start time and account for halftime intervals.
- Scraping functionality for play-by-play annotation from the Union Soccer Website.
- Visualization tools for showcasing metrics and generating video replays.

## Methods and Functionality

The following methods and functionalities were developed:

- Initial exploratory data analysis and cleaning of player fitness and wellness survey data.
- Framework for loading and processing player tracking data.
- Geometric transformations to convert raw positional data into a defined coordinate frame.
- Scraping and compiling player data from various sources.
- Visualization of player coordinates and animation of soccer pitch events.
- Generation of initial in-game metrics and visualizations.
- End-to-end workflow for loading session data and producing analytical insights.

## Recommendations

It is recommended that one or two students be onboarded to the project to utilize the codebase and research tools to produce analytical insights and develop additional features for on-pitch performance analysis. Acquiring new sources of data through video recordings and manual annotation can further enhance the project's potential.

## Future Work

Suggested future work includes:

- Development of additional features and metrics for on-pitch performance analysis.
- Integration of new data sources, such as video recordings and manual annotations.
- Expansion of the `GameScraper` class to include other relevant data sources.
- Further research and implementation of metrics based on positional data.

For detailed guidelines and scope, refer to `research.md`.

---
