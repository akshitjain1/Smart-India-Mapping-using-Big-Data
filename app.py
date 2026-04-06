import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import cv2

# ---------------- BIG DATASET ---------------- #

print("\nLoading big dataset...\n")

big_df = pd.read_csv("data/city_day.csv")

print("Big Dataset Loaded!\n")
print(big_df.head())

# ---------------- BIG DATA CLEANING ---------------- #

print("\nCleaning big dataset...\n")

big_df['Date'] = pd.to_datetime(big_df['Date'], errors='coerce')
big_df['AQI_Bucket'].fillna("Moderate", inplace=True)
print("Missing values before cleaning:\n")
print(big_df.isnull().sum())

big_df.fillna(big_df.mean(numeric_only=True), inplace=True)
big_df.dropna(subset=['City'], inplace=True)

print("\nMissing values after cleaning:\n")
print(big_df.isnull().sum())

print("\nBig dataset cleaned successfully!\n")

# ---------------- BIG DATA ANALYSIS ---------------- #

print("\nPerforming big data analysis...\n")

city_aqi = big_df.groupby("City")["AQI"].mean().sort_values(ascending=False)

print("Top 10 Most Polluted Cities (AQI):\n")
print(city_aqi.head(10))

# Graph for AQI
city_aqi.head(10).plot(kind='bar', figsize=(10,5))
plt.title("Top 10 Most Polluted Cities (AQI)")
plt.ylabel("AQI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/top10_aqi.png")

print("Top 10 AQI graph saved!\n")

# ---------------- SMALL DATASET ---------------- #

print("\nLoading small dataset...\n")

df = pd.read_csv("data/city_data.csv")

# Cleaning
df.replace("*", pd.NA, inplace=True)

for col in df.columns:
    if col not in ["Cities", "Month"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(df.mean(numeric_only=True), inplace=True)

print("Small dataset cleaned!\n")

# Analysis
avg_pm10 = df.groupby("Cities")[["2013-14 - PM10", "2014-15 - PM10", "2015-16 - PM10"]].mean()

print("Average PM10 levels:\n")
print(avg_pm10)

# Graph
avg_pm10.plot(kind='bar', figsize=(10,5))
plt.title("Average PM10 Levels Across Cities")
plt.ylabel("PM10")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/pm10_analysis.png")

print("PM10 graph saved!\n")

# ---------------- BASIC MAP ---------------- #

print("Creating basic map...\n")

city_coords = {
    "Agra": [27.1767, 78.0081],
    "Allahabad": [25.4358, 81.8463],
    "Amritsar": [31.6340, 74.8723],
    "Delhi": [28.7041, 77.1025],
    "Faridabad": [28.4089, 77.3178],
    "Ghaziabad": [28.6692, 77.4538],
    "Gwalior": [26.2183, 78.1828],
    "Jaipur": [26.9124, 75.7873],
    "Kanpur": [26.4499, 80.3319],
    "Lucknow": [26.8467, 80.9462],
    "Meerut": [28.9845, 77.7064],
    "Varanasi": [25.3176, 82.9739]
}

india_map = folium.Map(location=[28.0, 77.0], zoom_start=5)

avg_latest = avg_pm10["2015-16 - PM10"]

for city in avg_latest.index:
    if city in city_coords:
        value = avg_latest[city]

        folium.Marker(
            location=city_coords[city],
            popup=f"{city} PM10: {value:.2f}",
            icon=folium.Icon(color="red" if value > 200 else "green")
        ).add_to(india_map)

india_map.save("outputs/india_pollution_map.html")

print("Basic map saved!\n")

# ---------------- ADVANCED MAP (BIG DATA) ---------------- #

print("Creating advanced AQI map...\n")

top_cities = city_aqi.head(10)

city_coords_big = {
    "Ahmedabad": [23.0225, 72.5714],
    "Delhi": [28.7041, 77.1025],
    "Patna": [25.5941, 85.1376],
    "Gurugram": [28.4595, 77.0266],
    "Lucknow": [26.8467, 80.9462],
    "Talcher": [20.9500, 85.2167],
    "Jorapokhar": [23.7167, 86.4167],
    "Brajrajnagar": [21.8167, 83.9167],
    "Mumbai": [19.0760, 72.8777],
    "Kolkata": [22.5726, 88.3639]
}

india_map2 = folium.Map(location=[22.0, 78.0], zoom_start=5)

heat_data = []

for city, value in top_cities.items():
    if city in city_coords_big:
        lat, lon = city_coords_big[city]
        heat_data.append([lat, lon, value])

        folium.Marker(
            location=[lat, lon],
            popup=f"{city} AQI: {value:.2f}",
            icon=folium.Icon(color="red")
        ).add_to(india_map2)

HeatMap(heat_data).add_to(india_map2)

india_map2.save("outputs/advanced_pollution_map.html")

print("Advanced AQI map saved!\n")

# ---------------- COMPUTER VISION ---------------- #

print("Running Computer Vision...\n")

img = cv2.imread("outputs/pm10_analysis.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

cv2.imwrite("outputs/pm10_edges.png", edges)

print("CV processing done! Edge image saved.\n")

print(" PROJECT EXECUTED SUCCESSFULLY ")