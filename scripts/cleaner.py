import pandas as pd
import os

def clean_restaurant_data(input_file, output_file):
    # 1. Load the raw data
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    df = pd.read_csv(input_file)
    print(f"Original records: {len(df)}")

    # 2. Drop duplicates (important for OSM data)
    df = df.drop_duplicates(subset=['latitude', 'longitude', 'name'])

    # 3. Clean 'cuisine' column
    # Fill missing with 'other', convert to lowercase, and take the first tag if multiple exist (e.g., 'pizza;pasta' -> 'pizza')
    df['cuisine'] = df['cuisine'].fillna('other').str.lower()
    df['cuisine'] = df['cuisine'].apply(lambda x: x.split(';')[0].strip())

    # 4. Feature Engineering: Identify Chains
    # If the brand is not 'Independent', mark as chain
    df['is_chain'] = df['brand'].apply(lambda x: 0 if x == 'Independent' else 1)

    # 5. Filter out junk
    # We want to keep records that at least have a name
    df = df[df['name'] != 'Unknown']

    # 6. Save the cleaned data to the 'processed' folder
    df.to_csv(output_file, index=False)
    print(f"Cleaned records: {len(df)}")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    raw_path = os.path.join("data", "raw", "london_restaurants.csv")
    processed_path = os.path.join("data", "processed", "cleaned_restaurants.csv")
    clean_restaurant_data(raw_path, processed_path)
    