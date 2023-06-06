import unittest
import pytest
from geopy.geocoders import Nominatim
from solar_intensity_calculator import SolarIntensityCalculator, calculate_daylight_intensity

class TestSolarIntensityCalculator(unittest.TestCase):

    def setUp(self):
        self.solar_intensity = SolarIntensityCalculator("90210", 2023, 5, 500)

    def test_get_location_info(self):
        city, country, latitude, longitude = self.solar_intensity.get_location_info()
        self.assertEqual(city, "Beverly Hills")
        self.assertEqual(country, "United States")
        self.assertAlmostEqual(latitude, 34.0696, places=1)
        self.assertAlmostEqual(longitude, -118.4053, places=1)

    def test_get_sunrise_sunset_times(self):
        sunrise, sunset, noon = self.solar_intensity.get_sunrise_sunset_times(1)
        self.assertTrue(5 <= sunrise.hour <= 8)
        self.assertTrue(17 <= sunset.hour <= 20)
        self.assertEqual(noon.hour, 12)

    def test_get_hourly_intensity(self):
        self.solar_intensity.get_hourly_intensity() # This should run without errors

    def test_generation_total(self):
        total_energy = self.solar_intensity.total_energy
        df = self.solar_intensity.get_hourly_intensity()
        generation_total = df["Generation"].sum()

        # Calculate the percentage difference
        percentage_difference = abs(generation_total - total_energy) / total_energy * 100.0

        self.assertAlmostEqual(percentage_difference, 1, places=0)

    #def test_calculate_daylight_intensity(self):
    #    energy_per_day = 100.0
    #    energy_per_hour = 1.0
    #    daylight_hours = 12.0
    #    intensity_list = calculate_daylight_intensity(energy_per_hour, daylight_hours)

    #    # Assert that the sum of intensity_list equals energy_per_day
    #    assert sum(intensity_list) == pytest.approx(energy_per_day)


if __name__ == '__main__':
    unittest.main()
