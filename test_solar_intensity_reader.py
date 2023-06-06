import os
import csv
from datetime import datetime
from solar_intensity_reader import SolarIntensityReader

def test_read_solar_intensity_valid_file():
    # Write a temporary CSV file for testing
    with open("temp_solar_intensity.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "time", "solar_intensity"])
        writer.writerow(["01/01/2023", "12:00 PM", "1.23"])
    
    solar_reader = SolarIntensityReader("temp_solar_intensity.csv")
    solar_intensity_data = solar_reader.read_solar_intensity()

    assert len(solar_intensity_data) == 1
    assert solar_intensity_data[datetime.strptime("01/01/2023 12:00 PM", '%m/%d/%Y %I:%M %p')] == 1.23

    # Remove temporary file after use
    os.remove("temp_solar_intensity.csv")

def test_read_solar_intensity_invalid_file():
    solar_reader = SolarIntensityReader("nonexistent_file.csv")
    solar_intensity_data = solar_reader.read_solar_intensity()

    assert len(solar_intensity_data) == 0

def test_read_solar_intensity_no_file_provided():
    solar_reader = SolarIntensityReader()
    solar_intensity_data = solar_reader.read_solar_intensity()

    assert len(solar_intensity_data) == 0
