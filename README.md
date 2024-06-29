# CodeYou_Capstone
## Analysis and Visualization of Traffic Accidents in Construction Work Zones in Kentucky
**Disclaimer** While I am an employee of the Kentucky Transportation Cabinet (KYTC), this analysis is not an official KYTC analysis, but a reflection of my interest in the analysis.  The datasets analyzed in this study do not contain all traffic accidents records for the time period investigated.  They are extracts from downloads from the Kentucky State Police (KSP) collision data search website for the specific case being studied.  The API utilized in this study is a product of KYTC's big data team and is public facing (https://kytc-api-v100-lts-qrntk7e3ra-uc.a.run.app/docs#/).
**-_Teri Dowdy_**
## Table of Contents
- [CodeYou\_Capstone](#codeyou_capstone)
  - [Analysis and Visualization of Traffic Accidents in Construction Work Zones in Kentucky](#analysis-and-visualization-of-traffic-accidents-in-construction-work-zones-in-kentucky)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [Problem Statement](#problem-statement)
  - [Goals and Objectives](#goals-and-objectives)
  - [Technical Insight:](#technical-insight)
  - [Code You Data Analysis Project Requirements:](#code-you-data-analysis-project-requirements)

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
    1.	Create visualizations using Matplotlib, Plotly, and Tableau and Panel to illustrate findings.
    2.	Develop a Panel dashboard to present interactive and insightful visualizations for stakeholders.

## Technical Insight:
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

## Code You Data Analysis Project Requirements:
- Feature list #1 choice: Read multiple data files (JSON, CSV, Excel, etc.) and set up a local database with SQLite.
- Feature list #2 choice: Clean the data and perform a pandas merge, perform SQL join with API retrieved data to calculate  new values based on the query ouptut.
- Feature list #3 choice: Make 3 visualizations to display data.
- Feature list #4 choice: Utilize a Python virtual environment and include instructions in the README on how the user should set one up
- Feature list #4 optional: I may build a custom data dictionary if I have time.
- Feature list #5 choice: Annotate code with markdown cells in Python and Jupyter Notebook, write clear code comments, and have a well-written README.md.
