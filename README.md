# SQLALCHEMY CHALLENGE
## Challenge number 10 
---

**This repository contains the following:**

A folder called  <mark>SurfsUp</mark>  where you will find the sql and python files organized as follows:

- climate_hawaii.ipynb with the queries and solutions for the challenge

- app.py with the Flask code to generate an API

A subfolder called <mark>Output</mark> with the images of the results

A subfolder called <mark>Resources</mark> that gathers the given csv files with the data used for the analysis

---
---
## Climate in Hawaii
We analyzed the climate in Hawaii during the period between August 23 2016 and 2017. The data was provided by ther readings of 9 stations situated along the islands.

The table with the results is found here:

![Precipitation](/./SurfsUp/Output/Max_prcp.png)

We also calculated a summary for the max percipitation what show the strong variability of the rain in Hawaii.  

![Summary Rain](/./SurfsUp/Output/Summary_stats.png)

The temperature for the region show a mild weather with most of the readings between 65F and 80F. 

Summary results can be found here:

![Summary Temperature](/./SurfsUp/Output/Summary_temps.png)

![Temperature Histogram](/./SurfsUp/Output/Hist_tobs.png)

# API
The Api was designed to give access to five routes from the root directory. Below are samples of the outputs

## route("/")

![Root Menu](/./SurfsUp/Output/Main_menu.png)

## /api/v1.0/precipitation

![Precipitation](/./SurfsUp/Output/Precipitation.png)

## /api/v1.0/station

![Stations](/./SurfsUp/Output/Stations.png)

## /api/v1.0/tobs

![Temperatures](/./SurfsUp/Output/Tobs.png)

## /api/v1.0/start

### Example:
![Example with dynamic start date](/./SurfsUp/Output/Start.png)

### Error Handling:
![Error Handling](/./SurfsUp/Output/Error_start.png)

## /api/v1.0/start/end

### Example:
![Example with dynamic start and end dates](/./SurfsUp/Output/Start_end.png)

### Error Handling:
![Error Handling](/./SurfsUp/Output/Error.png)
