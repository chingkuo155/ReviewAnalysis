```
# Product Review Analysis System

## 1. Project Overview

This is a product review analysis system designed to collect, manage, and analyze product reviews. The system provides functionalities for adding, deleting, and viewing reviews, as well as data visualization capabilities including bar charts, word clouds, and area charts.

## 2. Features

- Add product reviews
- Delete specific reviews
- Display random reviews
- Show all reviews
- Generate bar charts of review data
- Create word clouds from review text
- Produce area charts of sentiment distribution over a specified time range

## 3. Technology Stack

- Backend: Python, FastAPI, Pandas, Matplotlib, Seaborn, WordCloud
- Frontend: HTML, CSS, JavaScript, jQuery

## 4. File Structure

- Backend:
  - `main.py`: Main application entry point
  - `routes.py`: API route definitions
  - `review_manager.py`: Review management class
  - `data_visualizer.py`: Data visualization class
- Frontend:
  - `static/index.html`: Main frontend page
  - `static/scripts.js`: Frontend JavaScript functionality
  - `static/styles.css`: CSS styles for the frontend

## 5. Installation Guide

1. Clone this repository
2. Install required Python packages:
   ```
   pip install fastapi pandas matplotlib seaborn wordcloud
   ```
3. Install the ASGI server for running FastAPI:
   ```
   pip install uvicorn
   ```

## 6. Usage Instructions

1. Run the following command in the terminal to start the server:
   ```
   uvicorn main:app --reload
   ```
2. Open a browser and navigate to `http://localhost:8000` to use the application
3. Use the web interface to add reviews, view existing reviews, and access data visualizations

## 7. Frontend Overview

The frontend provides an intuitive interface for users to interact with the review system. Key features include:
- A form to submit new product reviews
- Display of all reviews with the ability to toggle between short and full review text
- Random review display
- Integration of data visualization charts (bar chart, word cloud, and area chart)
- A form to delete reviews by index
- Responsive design for better user experience across devices

## 8. API Endpoints

- POST `/add_review/`: Add a new review
- POST `/delete_review/`: Delete a review
- GET `/random_reviews/`: Retrieve random reviews
- GET `/all_reviews/`: Retrieve all reviews
- GET `/bar_chart/`: Get a bar chart of review label distribution
- GET `/word_cloud/`: Get a word cloud of review text
- GET `/area_chart/`: Get an area chart of sentiment distribution over a specified time range

## 9. Data Visualization

The system provides three types of data visualization:
1. Bar Chart: Displays the number of reviews for different sentiment labels
2. Word Cloud: Visually represents high-frequency words in reviews
3. Area Chart: Shows sentiment distribution over time

## 10. Contribution Guidelines

Contributions are welcome. Please feel free to submit a Pull Request.
```

