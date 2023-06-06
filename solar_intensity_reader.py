import csv
import os
from collections import defaultdict
from datetime import datetime

class SolarIntensityReader:
    def __init__(self, solar_intensity_csv=None):
        self.solar_intensity_csv = solar_intensity_csv

    def read_solar_intensity(self):
        solar_intensity_data = defaultdict(float)
        if self.solar_intensity_csv and os.path.isfile(self.solar_intensity_csv):
            with open(self.solar_intensity_csv, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    date_time_str = row[0] + " " + row[1]
                    date_time = datetime.strptime(date_time_str, '%m/%d/%Y %I:%M %p')
                    solar_intensity_data[date_time] = float(row[2])
        else:
            print("No solar intensity data found. Continuing without it.")
        return solar_intensity_data