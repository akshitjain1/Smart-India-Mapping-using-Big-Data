import pandas as pd
import matplotlib.pyplot as plt
import folium
import cv2

# load dataset
file_path = "data/city_data.csv"
df = pd.read_csv(file_path)

print("Dataset loaded successfully!\n")

# ---------------- CLEANING ---------------- #

df.replace("*", pd.NA, inplace=True)

for col in df.columns:
    if col not in ["Cities", "Month"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(df.mean(numeric_only=True), inplace=True)

print("Data cleaned successfully!\n")

# ---------------- ANALYSIS ---------------- #

avg_pm10 = df.groupby("Cities")[["2013-14 - PM10", "2014-15 - PM10", "2015-16 - PM10"]].mean()

print("Average PM10 levels:\n")
print(avg_pm10)

# ---------------- GRAPH ---------------- #

avg_pm10.plot(kind='bar', figsize=(10,5))
plt.title("Average PM10 Levels Across Cities")
plt.ylabel("PM10")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("outputs/pm10_analysis.png")

print("\nGraph saved!")

# ---------------- MAP ---------------- #

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

print("Map saved!")

# ---------------- COMPUTER VISION ---------------- #

print("\nRunning Computer Vision on graph image...")

img = cv2.imread("outputs/pm10_analysis.png")

# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# edge detection
edges = cv2.Canny(gray, 100, 200)

# save output
cv2.imwrite("outputs/pm10_edges.png", edges)

print("CV processing done! Edge image saved.")