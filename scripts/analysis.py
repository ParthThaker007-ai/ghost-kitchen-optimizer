import geopandas as gpd
import pandas as pd
import os

def perform_gap_analysis():
    # 1. Load your cleaned restaurant points
    restaurants_df = pd.read_csv("data/processed/cleaned_restaurants.csv")
    
    # Convert to GeoDataFrame
    restaurants_gdf = gpd.GeoDataFrame(
        restaurants_df, 
        geometry=gpd.points_from_xy(restaurants_df.longitude, restaurants_df.latitude),
        crs="EPSG:4326"
    )

    # 2. Load neighborhood boundaries
    neighborhoods = gpd.read_file("data/raw/neighborhoods.geojson")

    # --- THE FIX: Identify the correct column name ---
    # We look for a column that looks like a name. 
    # Usually 'name', 'NAME', or 'neighborhood'
    possible_names = ['name', 'NAME', 'neighborhood', 'boroname', 'LSOA11NM']
    target_col = None
    for col in possible_names:
        if col in neighborhoods.columns:
            target_col = col
            break
    
    if not target_col:
        print(f"Available columns: {neighborhoods.columns}")
        raise KeyError("Could not find a neighborhood name column. Please update the script with one of the names above.")

    # Standardize the name column so the rest of our code works
    neighborhoods = neighborhoods.rename(columns={target_col: 'neighborhood_name'})
    # ------------------------------------------------

    # 3. SPATIAL JOIN
    joined = gpd.sjoin(restaurants_gdf, neighborhoods, how="inner", predicate="within")

    # 4. AGGREGATE
    supply_counts = joined.groupby('neighborhood_name').size().reset_index(name='restaurant_count')

    # 5. CALCULATE THE GAP SCORE
    # Note: If your GeoJSON doesn't have a 'population' column, 
    # we will use '1' as a placeholder for now so the code runs.
    if 'population' not in neighborhoods.columns:
        neighborhoods['population'] = 1000 # Default placeholder

    analysis = neighborhoods.merge(supply_counts, on='neighborhood_name', how='left').fillna(0)
    analysis['gap_score'] = analysis['population'] / (analysis['restaurant_count'] + 1)

    # Save the result
    analysis.to_file("data/processed/neighborhood_scores.geojson", driver='GeoJSON')
    print(f"Gap Analysis Complete using column: '{target_col}'!")

if __name__ == "__main__":
    perform_gap_analysis()