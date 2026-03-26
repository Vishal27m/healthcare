# ==========================================
# EPI-Optim Synthetic Dataset Generator (FINAL)
# ==========================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

print("🔥 Script started...")

np.random.seed(42)

# -------------------------------
# CONFIG
# -------------------------------
NUM_ZONES = 10
NUM_HOSPITALS = 5
DAYS = 60

zones = [f"Zone_{i}" for i in range(1, NUM_ZONES + 1)]
hospitals = [f"Hospital_{i}" for i in range(1, NUM_HOSPITALS + 1)]

start_date = datetime(2026, 1, 1)

print("📁 Saving files to:", os.getcwd())

# -------------------------------
# 1. POPULATION DATA
# -------------------------------
print("Generating population data...")

population_data = []
for zone in zones:
    population_density = random.randint(1000, 10000)
    population_data.append([zone, population_density])

population_df = pd.DataFrame(population_data, columns=["zone", "population_density"])


# -------------------------------
# 2. WEATHER DATA
# -------------------------------
print("Generating weather data...")

weather_data = []
for day in range(DAYS):
    date = start_date + timedelta(days=day)
    for zone in zones:
        temp = random.uniform(25, 40)
        humidity = random.uniform(50, 95)
        rainfall = random.uniform(0, 20)

        weather_data.append([date, zone, temp, humidity, rainfall])

weather_df = pd.DataFrame(weather_data, columns=["date", "zone", "temperature", "humidity", "rainfall"])


# -------------------------------
# 3. DISEASE SPREAD DATA
# -------------------------------
print("Generating disease data...")

disease_data = []
zone_base_cases = {zone: random.randint(5, 30) for zone in zones}

for day in range(DAYS):
    date = start_date + timedelta(days=day)

    for zone in zones:
        base = zone_base_cases[zone]
        growth_factor = np.random.normal(1.05, 0.1)
        seasonal_effect = np.sin(day / 10) + 1

        cases = int(base * growth_factor * seasonal_effect)
        cases += random.randint(0, 10)
        cases = max(cases, 0)

        zone_base_cases[zone] = cases
        disease_data.append([date, zone, cases])

disease_df = pd.DataFrame(disease_data, columns=["date", "zone", "cases"])


# -------------------------------
# 4. HOSPITAL RESOURCE DATA
# -------------------------------
print("Generating hospital data...")

hospital_data = []
for hospital in hospitals:
    zone = random.choice(zones)
    beds = random.randint(50, 200)
    ventilators = random.randint(10, 50)
    available_beds = int(beds * random.uniform(0.3, 0.8))

    hospital_data.append([hospital, zone, beds, ventilators, available_beds])

hospital_df = pd.DataFrame(
    hospital_data,
    columns=["hospital", "zone", "total_beds", "ventilators", "available_beds"]
)


# -------------------------------
# 5. SAVE DATASETS (CSV + EXCEL)
# -------------------------------
print("Saving files...")

# CSV
population_df.to_csv("population_data.csv", index=False)
weather_df.to_csv("weather_data.csv", index=False)
disease_df.to_csv("disease_data.csv", index=False)
hospital_df.to_csv("hospital_data.csv", index=False)

# Excel (requires openpyxl)
try:
    population_df.to_excel("population_data.xlsx", index=False)
    weather_df.to_excel("weather_data.xlsx", index=False)
    disease_df.to_excel("disease_data.xlsx", index=False)
    hospital_df.to_excel("hospital_data.xlsx", index=False)
    print("📊 Excel files also created!")
except Exception as e:
    print("⚠️ Excel not created (install openpyxl):", e)

print("✅ All datasets generated successfully!")
print("🎯 Check this folder:", os.getcwd())