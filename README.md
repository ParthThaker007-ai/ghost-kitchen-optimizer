# 📍 Ghost Kitchen Optimizer: Geospatial Gap Analysis
**An end-to-end data pipeline to identify "Delivery Deserts" and high-potential restaurant locations.**

## 🎯 Business Problem
Opening a physical restaurant is high-risk. Ghost Kitchens (delivery-only) reduce overhead, but success depends entirely on location. This project identifies urban areas where **food demand (population density)** outweighs **food supply (existing restaurants)**.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Acquisition:** OpenStreetMap (Overpass API)
- **Data Engineering:** Pandas, GeoPandas (Spatial Joins)
- **Visualization:** Folium (Interactive Choropleth Maps)
- **Version Control:** Git/GitHub

## 🚀 The Data Pipeline
1. **Extraction:** Scraped thousands of restaurant locations and cuisine types using the Overpass API.
2. **Standardization:** Cleaned messy OSM tags into a uniform "Cuisine" schema and identified chain vs. independent businesses.
3. **Spatial Analysis:** Performed a spatial join between restaurant points and neighborhood polygons.
4. **Scoring:** Developed an "Opportunity Score" formula:  
   `Score = Population / (Restaurant Count + 1)`

## 📊 Findings & Critical Analysis
- **Primary Opportunity:** Neighborhoods like [Insert Neighborhood Name] show the highest ROI potential.
- **Data Nuance:** Identified a "Suburban Data Gap" where OSM density decreases in outer zones. This highlights the need for multi-source validation (e.g., combining OSM with Google Places) in a production environment.

## 📦 How to Run
1. `git clone https://github.com/YOUR_USERNAME/ghost-kitchen-optimizer.git`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python scripts/scraper.py` -> `python scripts/cleaner.py` -> `python scripts/analysis.py` -> `python scripts/mapper.py`