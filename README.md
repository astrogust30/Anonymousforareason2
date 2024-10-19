<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="200" height="200"/>
</div>


##  About

Welcome to the Real-Time Weather Monitoring System, an application designed to monitor and analyze weather conditions in real-time. This system retrieves data from the OpenWeatherMap API for major metros in India and provides summarized insights, including daily weather summaries, alerting thresholds, and visualizations of historical trends.

### Read about the project in detail at :  https://reinvented-handle-6e0.notion.site/Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates-11e04110e05f80bc9cd8fe86aadf91ff?pvs=4

### Warning

**Please Note:** The code and content within this project are provided for reference purposes only. Unauthorized copying, reproduction, or distribution of the code without permission is prohibited. If you wish to use any part of this project, please contact the repository owner at khushisharmasre30@gmail.com for appropriate permissions.


## Table of Content  <div id="header" align="center">
  <img src="https://media.giphy.com/media/Qo2dupDib32rkTY4hX/giphy.gif?cid=ecf05e47viopwlm7lo1gou3g05zpjr1edr7jzyf2pqpv70ny&ep=v1_gifs_related&rid=giphy.gif&ct=s" width="100"/>
</div>

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Design Choices](#design-choices)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Build Instructions and Design Choices](#build-instructions-and-design-choices)
- [License](#license)
- [Contact Information](#contact-information)

## Introduction

It consists of:

- **Backend**: Python application using Flask for API endpoints and data processing.
- **Frontend**: HTML templates styled with Bootstrap and Chart.js for interactive visualizations.
- **Database**:SQLite for storing weather data, alerts, and daily summaries.

## Features

- **Real-Time Data Retrieval**: Continuously fetches weather data from the OpenWeatherMap API for selected cities.
- **Daily Summaries**: Calculates daily aggregates like average, maximum, and minimum temperatures, as well as dominant weather conditions.
- **Alerting System**: Triggers alerts when user-defined thresholds are breached, such as high temperatures or specific weather conditions.
- **Visualizations**: Displays interactive charts for temperature trends, historical data, and forecasted weather conditions.
- **Additional Weather Parameters**: Supports extended parameters like humidity and wind speed in the rollups and aggregates.
- **Weather Forecast Integration**: Incorporates forecast data to provide predictive summaries based on upcoming weather conditions.

  ![image](https://github.com/user-attachments/assets/65d7613a-9dd0-4126-bb11-c05dc5f7e9c1)

  ![image](https://github.com/user-attachments/assets/e4bd26d0-7d8a-4bdf-817c-8554692c995e)

  ![image](https://github.com/user-attachments/assets/60230bfc-13e3-4324-88f2-e8eebb25bb9c)

  ![image](https://github.com/user-attachments/assets/ca127723-a0dc-4153-abed-42b6d9fbb091)
  
  <img width="957" alt="image" src="https://github.com/user-attachments/assets/3825e697-4e6d-4925-9877-4c0606d11738">


  <img width="959" alt="image" src="https://github.com/user-attachments/assets/5741d304-f197-42b1-bf2d-2b789ae284e0">




## Technologies Used

- **Python 3.8+**: Core programming language for backend development.
- **Flask**: Web framework for the backend API and server.
- **SQLite**: Lightweight database for storing weather data and alerts.
- **Bootstrap**: For responsive and modern UI components.
- **jQuery**: Simplifies JavaScript interactions.
- **Chart.js**: JavaScript library for interactive charts and visualizations.
- **OpenWeatherMap API**: Source of real-time and forecast weather data

## Design Choices

- **Modular Architecture**: The application is structured to separate concerns by organizing code into modules for data retrieval, processing, alerting, and visualization. This improves maintainability and scalability.

- **Threading for Real-Time Processing**: Utilizes Python threading to fetch and process data concurrently, ensuring that the main application remains responsive and efficient.

- **Database Utilization**: Employs SQLite for efficient data storage and retrieval, enabling robust historical data analysis and quick access to weather information.

- **Interactive Frontend**: Integrates Chart.js and AJAX calls to provide dynamic data updates and an interactive user experience, allowing users to visualize data trends in real-time.

- **User Preferences**: Implements configuration options that allow users to customize alert thresholds and choose preferred temperature units, enhancing user control and personalization.

- **Error Handling**: Includes comprehensive error handling mechanisms for API calls and data processing, ensuring the application is robust and resilient against failures.


## Prerequisites

Before setting up the Weather Monitoring System, ensure you have the following prerequisites:

- **Python 3.8 or higher**: Make sure Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

- **pip**: The package installer for Python, which is typically included with Python installations. You can verify its installation by running `pip --version` in your command line.

- **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/) to obtain a free API key. This key is necessary to access the weather data API.


 <div id="header" align="center">
  <img src="https://media.giphy.com/media/jzuSsejVh8EYRfdOTz/giphy.gif?cid=ecf05e47vbyg4kvtrcv9fhy38lkc9a67y8tp03v7oy8xcfbt&ep=v1_gifs_related&rid=giphy.gif&ct=s" width="300" height="300"/>
</div>

## Usage

### Configure Alert Thresholds
1. Navigate to the "Configure Alert Thresholds" section on the dashboard.
2. Set the desired temperature threshold and select the temperature unit (Celsius or Fahrenheit).
3. Click "Update Threshold" to save your preferences.

### View Daily Summaries
- The "Daily Weather Summaries" section displays aggregated data for each city.
- Summaries include average, maximum, and minimum temperatures, humidity, wind speed, and dominant weather conditions.

### Monitor Historical Trends
- The "Historical Trends" section features interactive charts showing temperature trends over time.
- Hover over data points to see exact values.

### View Triggered Alerts
- The "Triggered Alerts" section lists recent alerts that have been triggered based on your configured thresholds.
- Alerts include the city, alert message, and timestamp.

### View Forecast Summaries
- The "Forecast Summaries" section provides predictive insights based on upcoming weather conditions.
- Forecasts include expected temperatures, humidity, wind speed, and dominant weather.

## API Endpoints

- **GET /**  
  Description: Renders the main dashboard.

- **POST /update_threshold**  
  Description: Updates user-configurable thresholds for alerts.  
  Parameters:
  - `threshold_temp`: The temperature threshold value.
  - `temp_unit`: Temperature unit ('Celsius' or 'Fahrenheit').

- **GET /get_daily_summaries**  
  Description: Retrieves daily weather summaries for all cities.

- **GET /get_triggered_alerts**  
  Description: Fetches the list of recently triggered alerts.

- **GET /get_temperature_data**  
  Description: Provides temperature data for all cities to generate historical trend charts.

- **GET /get_forecast_summaries**  
  Description: Retrieves forecasted weather summaries for predictive analysis.

## Dependencies

To run the Weather Monitoring System, ensure the following dependencies are installed:

- **Flask**:  
  Install with: `pip install flask`

- **Requests**:  
  Install with: `pip install requests`

- **SQLite3**:  
  Built-in with Python.

- **Chart.js**:  
  Included via CDN in HTML templates.

- **jQuery**:  
  Included via CDN in HTML templates.

- **Bootstrap**:  
  Included via CDN in HTML templates.

- **Threading**:  
  Built-in with Python.

## Build Instructions and Design Choices

### Build Instructions

### **How to Run the Application**

1. **Install Dependencies**:
    
    ```bash
    pip install flask
    
    ```
    
2. **Run the Application**:

   Remove weather_data.db file
    
    ```bash
    python app.py
    
    ```
    
4. **Access the UI**:
    - Open a web browser and navigate to **`http://localhost:5000`**.
5. Add your API key in "config.py".

## Docker Instructions

Follow these steps to build and run the application using Docker.

### Build the Docker Image

First, ensure you have Docker installed on your machine. Then, build the Docker image using the following command:

 ```bash
   docker login
   docker build -t your-container-name .
   docker run -d -p 5000:5000 your-container-name  
    
 ```
Access application through : http://localhost:5000

## Design Choices

### Backend Processing

- **Threading**: Utilized Python threading to fetch and process weather data in the background without blocking the main thread. This ensures that the application remains responsive while handling real-time data.

- **Data Storage**: Chose SQLite for its simplicity and ease of integration with Python, making it suitable for storing weather data and alerts efficiently.

- **Modular Code**: Organized code into distinct functions and routes to enhance clarity and maintainability, allowing for easier updates and debugging.

### Frontend Interface

- **Bootstrap**: Adopted Bootstrap for its responsive design capabilities and ease of use, providing a consistent and modern look across different devices.

- **Chart.js**: Selected Chart.js for its ability to create interactive and visually appealing charts, which are used to display weather trends effectively.

- **AJAX Calls**: Implemented AJAX requests to update data on the dashboard dynamically, avoiding full page reloads and enhancing user experience.

### User Interaction

- **Configuration Options**: Provided forms for users to set their preferences, such as temperature units and alert thresholds, allowing for a personalized experience.

- **Real-Time Updates**: Set intervals to refresh data on the frontend, ensuring that the dashboard displays the most current weather information available.

### Error Handling

- **API Response Checks**: Included checks for API response statuses to gracefully handle errors, ensuring that users receive informative messages rather than abrupt failures.

- **Exception Handling**: Wrapped critical sections in try-except blocks to catch and log exceptions, preventing crashes and maintaining application stability.


## File Structure
 ```sh
weather-monitoring-system/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── styles.css
│   └── scripts.js
├── weather_data.db
└── README.md
```

## Details of Key Files

### app.py
- **Description**: The main Flask application file responsible for the core functionality of the application.
- **Key Components**:
  - **Routes**: Defines endpoints for the dashboard, updating thresholds, and providing data for AJAX calls.
  - **Background Tasks**: Implements threading for real-time data fetching and processing, ensuring the application remains responsive.
  - **Database Operations**: Manages interactions with the SQLite database for storing and retrieving weather data and alerts.

### config_example.py
- **Description**: A template configuration file where users can insert their OpenWeatherMap API key.
- **Contents**:
  - Configurable parameters such as update intervals and default alert thresholds, allowing users to customize the application settings.

### templates/index.html
- **Description**: The main HTML template for rendering the dashboard.
- **Features**:
  - Includes sections for configuring alerts, viewing daily summaries, and displaying interactive charts.

### static/styles.css
- **Description**: Custom CSS styles to enhance the visual appearance of the dashboard.
- **Purpose**: Provides styling for various elements to ensure a consistent and appealing user interface.

### static/scripts.js
- **Description**: Contains JavaScript code for managing user interactions and AJAX requests.
- **Functionality**:
  - Handles dynamic updates to the dashboard by fetching the latest data without requiring a full page reload.
    
Visualization of DB

<img width="728" alt="image" src="https://github.com/user-attachments/assets/2ef14dfb-bdd7-4e07-a8a3-df523273f6fe">

<img width="721" alt="image" src="https://github.com/user-attachments/assets/3446e1c5-1ac5-4095-9865-68fa25c377fb">



## License

All rights reserved with khushisharmasre30@gmail.com

## Contact Information

For any questions or suggestions, please open an issue or contact the repository owner at khushisharmasre30@gmail.com.


