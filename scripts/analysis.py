import geopandas as gpd
import pandas as pd
import os

def perform_gap_analysis():
    # 1. Load your cleaned restaurant points
    restaurants_df = pd.read_csv("data/processed/cleaned_restaurants.csv")
    
    # Convert regular DataFrame to a GeoDataFrame (Points)
    restaurants_gdf = gpd.GeoDataFrame(
        restaurants_df, 
        geometry=gpd.points_from_xy(restaurants_df.longitude, restaurants_df.latitude),
        crs="EPSG:4326"
    )

    # 2. Load neighborhood boundaries (You'll download this as a GeoJSON)
    # For now, let's assume you have 'neighborhoods.geojson' in data/raw/
    neighborhoods = gpd.read_file("data/raw/neighborhoods.geojson")

    # 3. SPATIAL JOIN: Map restaurants to neighborhoods
    # This adds the neighborhood name to every restaurant row
    joined = gpd.sjoin(restaurants_gdf, neighborhoods, how="inner", predicate="within")

    # 4. AGGREGATE: Count restaurants per neighborhood
    supply_counts = joined.groupby('neighborhood_name').size().reset_index(name='restaurant_count')

    # 5. CALCULATE THE "GAP SCORE"
    # Merge with demographic data (population/income)
    # Gap Score = Population / (Restaurant Count + 1)
    analysis = neighborhoods.merge(supply_counts, on='neighborhood_name', how='left').fillna(0)
    analysis['gap_score'] = analysis['population'] / (analysis['restaurant_count'] + 1)

    # Save the result
    analysis.to_file("data/processed/neighborhood_scores.geojson", driver='GeoJSON')
    print("Gap Analysis Complete! High scores = High Opportunity.")

if __name__ == "__main__":
    perform_gap_analysis()