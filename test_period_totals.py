import pytest
from datetime import datetime
from file_handler import FileHandler
from solar_intensity_reader import SolarIntensityReader
from energy_data_processor import EnergyDataProcessor

# Define the test function
def test_super_off_peak_total():
    # Define the input variables
    input_csv_file = "elec-5.22-5.23.csv"
    start_date_str = "05/01/2022"
    end_date_str = "05/02/2022"
    solar_intensity_file = "ssolar_intensity.csv"

    file_handler = FileHandler()
    input_data = file_handler.read_csv(input_csv_file)
    solar_intensity_data = SolarIntensityReader(solar_intensity_file).read_solar_intensity()

    # Run the main script to calculate the totals
    processor = EnergyDataProcessor(start_date_str, end_date_str)
    totals = processor.calculate_totals(input_data, solar_intensity_data)

    for date_range, season_totals in totals.items():
        # Assert the "super off peak" total is 3.87 for May 1 in the Winter season
        assert season_totals["Winter"]["Super Off Peak"] == 3.87
        # Assert the "on peak" total is 8.865 for May 1 in the Winter season
        assert season_totals["Winter"]["On Peak"] == 8.865
        # Assert the "off peak" total is 4.225 for May 1 in the Winter season
        assert season_totals["Winter"]["Off Peak"] == 4.225

# Run the tests
pytest.main()
