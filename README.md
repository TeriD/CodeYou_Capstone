<a name="top"></a>
# Analysis and Visualization of Traffic Accidents in Construction Work Zones in Kentucky

Disclaimer: While I am an employee of the Kentucky Transportation Cabinet (KYTC), this analysis is not an official KYTC analysis but a reflection of my interest in the analysis.
<p style="text-align:right;">- Teri Dowdy     </p>

## Table of Contents
- [Analysis and Visualization of Traffic Accidents in Construction Work Zones in Kentucky](#analysis-and-visualization-of-traffic-accidents-in-construction-work-zones-in-kentucky)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Abstract](#abstract)
  - [Problem Statement](#problem-statement)
  - [Goals and Objectives](#goals-and-objectives)
  - [Technical Insight](#technical-insight)
  - [Code You Data Analysis Project Requirements](#code-you-data-analysis-project-requirements)
  - [Code:You Features Utilized for the Project](#codeyou-features-utilized-for-the-project)
  - [Data](#data)
  - [Project Structure](#project-structure)
  - [How to Run](#how-to-run)
  - [Virtual Environment Commands](#virtual-environment-commands)
  - [Future Development](#future-development)

## Overview

* The goal of this project was to learn new techniques for visualization of data while performing analysis of traffic accidents in construction work zones within the state of Kentucky.

* In addition to downloaded crash data from the Kentucky State Police Collision Data search portal, I wanted to incorporate KYTC's newest roadway characteristics API to return the most accurate information for each incident reported. The API utilized in this study is a product of KYTC’s big data team and is public-facing (https://kytc-api-v100-lts-qrntk7e3ra-uc.a.run.app/docs#/).

* I wanted to create a standalone database for storage in SQLite and geojson and to become more familiar with using multiple visualization techniques outside of the purview of main stream GIS software using python as the main development instrumen

## Abstract
In 2023, there were over 1200 crashes in Kentucky roadway work zones, leading to 17 fatalities. This project aims to study traffic accident patterns within construction work zones across Kentucky. The project will use advanced data analysis and visualization techniques to integrate various datasets, identify key trends, and propose safety improvements. By combining KSP crash data with a comprehensive API of available roadway characteristics, the project aims to provide actionable insights to enhance roadway safety during construction activities. Tools such as Pandas, Matplotlib, Plotly, SQLite, Tableau, and Jupyter Notebook will ensure comprehensive and reproducible analysis.

## Problem Statement
Construction work zones are crucial areas where traffic accidents often occur due to changes in road conditions and traffic patterns. In 2023, Kentucky experienced a spike of over 1200 crashes in these zones, resulting in 17 fatalities. These accidents lead to significant economic losses and pose serious safety risks to workers and motorists. The project aims to understand and address the factors contributing to traffic accidents in these zones by analyzing historical crash data and correlating it with roadway characteristics. The goal is to identify patterns and propose safety improvements that can reduce the incidence and severity of these accidents.

## Goals and Objectives
- **Goal 1:** to conduct a thorough analysis of traffic accidents in construction work zones:
    1. Collect and clean traffic accident data from the Kentucky State Police (KSP) dataset.
        - download raw data from KSP online collision datasets by year and environmental factor (Work Zone)
        - select desired files and convert each year's file to csv format
    2. Integrate available Kentucky Transportation Cabinet (KYTC) roadway characteristics data by making API calls for each crash location.
    3. Analyze the merged dataset to identify trends, patterns, and key factors contributing to accidents in construction work zones.
- **Goal 2:** to develop Comprehensive and Interactive Visualizations
    1. Create visualizations using Matplotlib, Plotly, and Tableau and Panel to illustrate findings.
    2. Develop a Panel dashboard to present interactive and insightful visualizations for stakeholders.

## Technical Insight
- **Python Libraries:** To begin the project, I will begin by utilizing VS Code, Python and Jupyter Notebook extensions, and a Python virtual environment with libraries such as pandas, pyarrow, and requests for data importing, cleaning, and analysis.
- **Sources:** Collision data will be sourced from the Kentucky State Police (KSP) Collision Data website (http://crashinformationky.org/AdvancedSearch).  The raw text files downloaded for each year will be filtered to 3 of the 7 available files and converted to csv files. Optionally, if I have time I would also like to include OpenWeatherMap's API to access weather data for each collision to evaluate any potential weather-related factors.
- **Access Requirements:** No special access requirements are needed as the data is openly provided by KSP and the KYTC Spatial API for associated roadway attributes.
- **Data Cleaning:** A SQLite spatial database will be created and the raw KSP files will be filtered with standardize column names, data types (date/time), and parse/extract latitude and longitude.
- **Data Integration:** Merge/concatenate multiple annual KSP data sources. The KSP collision locations will be processed through the KYTC Spatial API.
- **Summary/Statistics:** Calculate descriptive statistics to understand the distribution of collisions in Work Zones by District, County, and Road Type.
- **Optional Summary/Statistics:** I may also perform an analysis by roadway characteristics and/or current weather conditions if time permits.
- **Data Visualization:** Utilize libraries such as Matplotlib, Plotly, and Panel to create visualizations for exploring patterns and trends in collision and road characteristics data.
- **Documentation:** Document the analysis process, including data preprocessing steps, exploratory data analysis, and insights gained.
- **Reporting:** Prepare a report/presentation summarizing key findings, insights, and visual outputs from the analysis.
- **Optional Reporting:** If time permits, I may also utilize PowerBI or Tableau to provide additional visualization of the data.

## Code You Data Analysis Project Requirements
- **Feature list #1 choice:** Read multiple data files (JSON, CSV, Excel, etc.) and set up a local database with SQLite.
- **Feature list #2 choice:** Clean the data and perform a pandas merge, perform SQL join with API retrieved data to calculate new values based on the query output.
- **Feature list #3 choice:** Make 3 visualizations to display data.
- **Feature list #4 choice:** Utilize a Python virtual environment and include instructions in the README on how the user should set one up.
- **Feature list #4 optional:** I may build a custom data dictionary if I have time.
- **Feature list #5 choice:** Annotate code with markdown cells in Python and Jupyter Notebook, write clear code comments, and have a well-written README.md.

## Code:You Features Utilized for the Project

| Feature List | Choice                   | Description                           |
|--------------|--------------------------|---------------------------------------|
| 1            |Read multiple data files  | Used 2 CSV files from KSP             |
| 2            |Clean the data and perform a pandas merge, perform SQL join with API retrieved data to calculate  new values based on the query ouptut.                                   | Cleaned my data and merged them with pandas. Calculated stats from various data points used within visualizations.|
| 3            |Make 3 visualizations to display data | Made 13 plots and graphs using Bokeh, Dash, Folium, Matplotlib, Panel and Plotly. |
| 3            |Make a Tableau dashboard  | Time permitting - Make a dashboard with my findings. [Tableau](https://public.tableau.com/app/discover/viz-of-the-day) |
| 4            |Utilize a Python virtual environment and include instructions in the README on how the user should set one up | Created a venv and included instructions to reproduce.|
| 4            |Optional: Data Dictionary | Created a data dictionary for all datasets used in project. |
| 5            |Annotate code with markdown cells in Python and Jupyter Notebook, write clear code comments, and have a well-written README.md.| Included markdown cells in Jupyter Notebook and inline comments to describe each step and code block. |

## Data

- Data Sources:
  - Kentucky State Police Collision Data [http://crashinformationky.org/AdvancedSearch]
  - Parameters:
    - Environmental Factor: "Collision Work Zone"
    - Collision Dates: January 2020-June 2024
    - Each year's data was downloaded individually due to limitations of KSP site.

![Query Parameters](data/reference_data/KSP_Website.png)



- KYTC Spatial API Services:
   - [API Website](https://kytc-api-v100-lts-qrntk7e3ra-uc.a.run.app/docs#/)
-
- Dataset Structure:
	- Describe the structure of each dataset (columns, data types, etc.)
	- Size and format of datasets (e.g., CSV, JSON)
- Preprocessing Steps:
	- Cleaning, standardizing column names, data types, and extracting geolocation data.
- Merging multiple datasets.

## Project Structure

- Data Exploration:
	- Jupyter notebooks or scripts to explore the dataset.
	- Analysis:
	    - Using Python with the Pandas package to clean the data.
	- Visualizations:
	    - Using Matplotlib, Plotly, and Panel to visualize findings.
	    - Dashboard:
    	    - Using Panel or Tableau to combine multiple visualizations together.


## How to Run
To run this project, follow these steps:

1. Clone the repository to your local machine: [https://github.com/TeriD/CodeYou_Capstone from git bash](https://github.com/TeriD/CodeYou_Capstone.git)
2. After you have cloned the repo to your local machine, navigate to the project folder in GitBash/Terminal.
3. Create a virtual environment in the project folder.
4. Activate the virtual environment.
5. Jupyter Notebooks is required to run this project.
6. Install the required packages: `pip install -r requirements.txt`.  Note:  the 'pipfreeze' command rendered an extensive list of packages, not all of which are required for the operation of this project.  I have included a shorter list of just those packages actually called in the Jupyter notebooks utilized for the analyses and visualizations. This shorter list is 'requirements_minimal.txt'.
7. Navigate to the repository directory.
8. A Data Dictionary has been created for reference purposes.
9. If you intend to run the database setup, please run the Database_Precheck.ipynb first to clean the database.  Otherwise, you may end up with duplicate records.
10. There are two main files that build the project datasets:
   a. Database_Setup_n_Data_Ingestion.ipynb - You can choose to Run all or step through the cells individually.
      - This Jupyter notebook builds the SQLite database if necessary
      - It iterates through the raw KSP datasets and imports them in order into cleaned dataset csv files and tables within the database.
      - It also loads lookup tables needed for labels within the visualizations.
   b. RetrieveRoadwayCharacteristicsFromKYTC_API.ipynb
      - be aware that there are 4105 incidents to be processed.  The main function call to the API for all incidents has averaged 8 minutes to be processed completely.  If you see a record count greater than 4105, then the database has not been cleared completely.  This can happen if the 1st process is stopped before completion and not reset.
   c. Create_County_Extents.ipynb
      - This Jupyter notebook builds the latitude and longitude extents used in zoom functionality within the Folium map.
      - While this notebook functions as written, it has not been implemented in the Folium map product successfully. This is a work in progress.
11. There are multiple visualizations available. No specific order is recommended. They are presented in alphabetical order.
   a. Deaths and Speed Visualizations.ipynb
      - This Jupyter notebook uses plotly to build six graphs that look at the fatalities that occurred for the incidents reported in this project
      - The first two graphs (line and bar graphs) are two different representations of fatalities by year and month.
      - The third graph represents both fatalities and injuries by year and month.
      - The forth graph add the factor of PersonType to graph 3.  The next step for this graph will be to change the numeric value for PersonType to the Code Description (i.e. PersonType=1 is the driver of a vehicle)
      - Graph five represents the total fatalities by PersonType
      - Graph six represents the total incidents on state-maintained routes by route type where excessive speed was involved.
   b. Drivers_By_Age_and_Gender.ipynb
      - This Jupyter notebook uses plotly.express to build a graph that categorizes the age and gender of drivers involved in incidents for 2023-2024.
      - The ages were grouped to make the data easier to display.
      - Of note, the query was made on the entire database, but only data was retrieved for 2023-2024.  This is probably due to reporting changes for prior years.  A next step for this graph would be a deeper investigation of the differences between the prior years records to make the query work for the entire dataset.
   c. Folium_Incidents_Locations_Map.ipynb
      - This visualization uses Folium and Panel to create an html page to display spatial data.
      - The Jupyter notebook imports the geojson data from the RoadwayCharacteristics
      - The process creates a map showing the locations of each incident overlying a base map, and county and KYTC District layers.
      - The map includes a layer list that allows you to turn off the auxillary layers.
   d. HumanFactor_Visualizations.ipynb
      - This Jupyter notebook uses wordcloud and matplotlib to build the visualizations
      - It joins the ksp_factors table to the unit_code lookup table to display readable descriptions of the factors that may have caused or influenced an incident.
      - Three separate visualizations are produced for comparison of the same data.
        - Word Cloud
        - Bar Graph
        - Pie Chart
   e. Incidents_By_District_and_Year_Bar_Graph.ipynb
      - This Jupyter notebook uses dash to perform the visualization
      - It performs a join between the incidents and the county lookup table to allow the data to be viewed by District and Year.
      - There are 12 KYTC Districts shown on the graph from west to east, numerically.
      - An interesting feature of the dash app is the ability to change the graph to display each year in the dataset by selecting the desired year by a dropdown list at the top of the graph.
   f. Traffic_Controls_Visualizations.ipynb
      - This Jupyter notebook uses plotly express to build a stacked bar chart to display Traffic Control Devices by Route Type and District in Place for Traffic Incidents in Construction Work Zones on State-maintained Routes 2020-2024.
      - The data was grouped by KYTC District to show the variations in the distribution of Interstates and Parkways across the state.
   g. VehicleType_Visualization_Bokeh.ipynb
        - This Jupyter notebook uses Bokeh to provide the visualization
        - The output pie chart plot shows the different vehicle type categories that were involved in all incidents within the range of data.
12. Workzone_Dashboard
   a. This final visualization is a work in progress.
   b. The workzone_dashboard.py builds components for a Panel application giving an overview of the project and a visualization of the KSP_Incidents data table.
   c. The Run_Workzone_Dashboard.ipynb will open the Panel application in a web browser.
   d. Note that if you execute the Run_Workzone_Dashboard.ipynb to display the Panel application, you must stop the process in the code IDE.  Closing the browser does not accomplish this.  This step is a workaround to having the Panel application hosted on a third-party site.
13. When you are done working on your repo, deactivate the virtual environment.

## Virtual Environment Commands

| Command | Linux/Mac | GitBash |
|---------|-----------|---------|
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |

## Future Development
   - Expand the project to include additional years of data to gain a better understanding of progress (if any) toward reducing the number of incidents in Construction Work Zones.
   - Design and build an entire Panel application to include these and other panes from the project into a cohesive site.  Next steps include:
      1. get the Folium map pane to function within the Panel application.
      2. add the VehicleType_Visualization_Bokeh pane
      3. add the HumanFactor_Visualization Bar Graph to the Panel application
      4. host the Panel application for a more cohesive product.
   - Expand the data visualizations for other queries to analyze the data further.
   - Investigate ways to integrate/bind panes together to make them more interactive.
   - Extract historical weather data from the NOAA website and integrate conditions as factors for analysis of accident conditions.

[Back to top](#top)
