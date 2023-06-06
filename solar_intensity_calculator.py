import os.path
from geopy.geocoders import Nominatim
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime, timedelta
import pytz
import math
import pandas as pd

def calculate_daylight_intensity(energy_per_day, daylight_hours):
    energy_per_hour = energy_per_day / daylight_hours
    return [energy_per_day / (2 * daylight_hours / math.pi) * math.sin(math.pi * hour / daylight_hours) for hour in range(int(daylight_hours))]

class SolarIntensityCalculator:
    def __init__(self, zip_code, year, month, total_energy):
        self.zip_code = zip_code
        self.year = year
        self.month = month
        self.total_energy = total_energy
        self.geolocator = Nominatim(user_agent="22cb-experiment")
        self.city, self.country, self.latitude, self.longitude = self.get_location_info()

    def get_location_info(self):
        location = self.geolocator.geocode(self.zip_code)
        city = location.address.split(',')[0]
        country = location.address.split(',')[-1]
        latitude = location.latitude
        longitude = location.longitude
        return city, country.strip(), latitude, longitude

    def get_sunrise_sunset_times(self, day):
        date = datetime(self.year, self.month, day)
        location = LocationInfo(self.city, self.country, timezone="US/Pacific", latitude=self.latitude, longitude=self.longitude)
        sun_times = sun(location.observer, date=date, tzinfo=pytz.timezone(location.timezone))
        return sun_times['sunrise'], sun_times['sunset'], sun_times['noon']

    def get_hourly_intensity(self):
        rows_list = []
        current_date = datetime(self.year, self.month, 1)
        end_date = datetime(self.year, self.month, self.num_days_in_month(self.year, self.month))

        while current_date <= end_date:
            sunrise_time, sunset_time, _ = self.get_sunrise_sunset_times(current_date.day)
            daylight_hours = (sunset_time - sunrise_time).seconds / 3600

            energy_per_day = self.total_energy / self.num_days_in_month(current_date.year, current_date.month)
            energy_per_hour = energy_per_day / daylight_hours

            daylight_intensity = calculate_daylight_intensity(energy_per_day, daylight_hours)

            for hour in range(24):
                if sunrise_time.hour <= hour < sunset_time.hour:
                    energy = daylight_intensity[hour - sunrise_time.hour] if hour - sunrise_time.hour < len(daylight_intensity) else 0
                else:
                    energy = 0

                date = current_date.strftime('%m/%d/%Y')
                start_time = datetime(current_date.year, current_date.month, current_date.day, hour).strftime('%I:%M %p')
                rows_list.append({"Date": date, "Start Time": start_time, "Generation": energy})

            current_date += timedelta(days=1)

        df = pd.DataFrame(rows_list)
        return df

    def num_days_in_month(self, year, month):
        if month == 12:
            return (datetime(year + 1, 1, 1) - datetime(year, month, 1)).days
        else:
            return (datetime(year, month + 1, 1) - datetime(year, month, 1)).days

    def to_csv(self, filename):
        if os.path.isfile(filename):
            existing_data = pd.read_csv(filename)
            df = pd.concat([existing_data, self.get_hourly_intensity()], ignore_index=True).drop_duplicates()
        else:
            df = self.get_hourly_intensity()

        df.to_csv(filename, index=False)


    def print_hourly_intensity(self):
        df = self.get_hourly_intensity()
        print(df)

# Example usage
# solar_intensity = SolarIntensity("90210", 2022, 5, 1000)
# solar_intensity.print_hourly_intensity()
