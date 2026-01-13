import folium
import geopandas as gpd
import os
import json

def create_interactive_map():
    data_path = "data/processed/neighborhood_scores.geojson"
    if not os.path.exists(data_path):
        print("Error: neighborhood_scores.geojson not found.")
        return

    # 1. Load the data
    gdf = gpd.read_file(data_path)

    # 2. FIX: Convert all Timestamp/Datetime columns to strings
    # This prevents the 'JSON serializable' error
    for col in gdf.columns:
        if gdf[col].dtype == 'datetime64[ns]' or 'datetime' in str(gdf[col].dtype):
            gdf[col] = gdf[col].astype(str)

    # 3. Initialize Map (Centered on London)
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=11, tiles="CartoDB positron")

    # 4. Create the Choropleth
    folium.Choropleth(
        geo_data=gdf,
        name="Gap Score",
        data=gdf,
        columns=["neighborhood_name", "gap_score"],
        key_on="feature.properties.neighborhood_name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Kitchen Opportunity Score",
    ).add_to(m)

    # 5. Add Tooltips (Optional but makes it look very professional)
    # This allows you to hover over a neighborhood to see its name and score
    folium.GeoJson(
        gdf,
        style_function=lambda x: {'fillColor': '#ffffff00', 'color': '#ffffff00'},
        tooltip=folium.GeoJsonTooltip(
            fields=['neighborhood_name', 'restaurant_count', 'gap_score'],
            aliases=['Neighborhood:', 'Restaurants:', 'Opportunity Score:'],
            localize=True
        )
    ).add_to(m)

    # 6. Save the map
    output_path = "output/maps/opportunity_map.html"
    m.save(output_path)
    print(f"Interactive map created successfully at: {output_path}")

if __name__ == "__main__":
    create_interactive_map()