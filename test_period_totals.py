import pytest
from main_script import calculate_totals

# Define the test function
def test_super_off_peak_total():
    # Define the input variables
    input_csv_file = "elec-5.22-5.23.csv"
    start_date_str = "05/01/2022"
    end_date_str = "05/02/2022"

    # Run the main script to calculate the totals
    totals = calculate_totals(input_csv_file, start_date_str, end_date_str)

    for date_range, season_totals in totals.items():
        # Assert the "super off peak" total is 3.87 for May 1 in the Winter season
        assert season_totals["Winter"]["Super Off Peak"] == 3.87
        # Assert the "on peak" total is 8.865 for May 1 in the Winter season
        assert season_totals["Winter"]["On Peak"] == 8.865
        # Assert the "off peak" total is 4.225 for May 1 in the Winter season
        assert season_totals["Winter"]["Off Peak"] == 4.225

# Run the tests
pytest.main()
