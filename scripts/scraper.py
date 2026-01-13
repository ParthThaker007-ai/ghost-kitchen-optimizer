import overpy
import pandas as pd
import os

def fetch_restaurant_data(bbox):
    api = overpy.Overpass()
    # Query for restaurants AND fast food to find the full landscape
    query = f"""
    [out:json];
    (
      node["amenity"~"restaurant|fast_food"]({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});
      way["amenity"~"restaurant|fast_food"]({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});
    );
    out center;
    """
    print("Fetching data from OpenStreetMap...")
    result = api.query(query)
    
    data = []
    # Combine nodes and ways into a single list
    for item in list(result.nodes) + list(result.ways):
        coords = (item.lat, item.lon) if hasattr(item, 'lat') else (item.center_lat, item.center_lon)
        data.append({
            "name": item.tags.get("name", "Unknown"),
            "cuisine": item.tags.get("cuisine", "Not Specified"),
            "latitude": coords[0],
            "longitude": coords[1],
            "brand": item.tags.get("brand", "Independent")
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # London Bounding Box
    london_bbox = (51.48, -0.15, 51.52, -0.05) 
    df = fetch_restaurant_data(london_bbox)
    
    # Save to raw data folder
    output_path = os.path.join("data", "raw", "london_restaurants.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} restaurants to {output_path}")