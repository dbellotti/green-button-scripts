import csv
from collections import defaultdict
from datetime import datetime
import yaml

from holiday_date_identifier import HolidayDateIdentifier
from period_identifier import PeriodIdentifier


def load_plans():
    with open("plans.yml", "r") as file:
        plans = yaml.safe_load(file)
    return plans


def calculate_totals(input_csv_file, start_date_str=None, end_date_str=None):
    # Define the indices of columns to remove (0-based index)
    columns_to_remove = [0, 3, 4, 5]

    # Create nested defaultdicts to store the totals by date range, on peak/off peak/super off peak, and total value
    totals_by_range = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    with open(input_csv_file, "r") as file:
        reader = csv.reader(file)

        # Skip the header row
        next(reader)

        # Determine the start and end dates based on the CSV data
        dates = [datetime.strptime(row[1], "%m/%d/%Y") for row in reader]
        start_datetime = min(dates) if start_date_str is None else datetime.strptime(start_date_str, "%m/%d/%Y")
        end_datetime = max(dates) if end_date_str is None else datetime.strptime(end_date_str, "%m/%d/%Y")

        # Reset the file pointer to the beginning
        file.seek(0)
        next(reader)  # Skip the header row

        # Define a list of holidays (in datetime format)
        holidays = HolidayDateIdentifier().get_holidays_in_date_range(start_datetime, end_datetime)

        # Create an instance of the PeriodIdentifier class
        period_identifier = PeriodIdentifier(holidays)

        # Iterate through each row in the CSV
        for row in reader:
            # Extract the date, start time, and net value from the row
            date = datetime.strptime(row[1], "%m/%d/%Y")
            month = date.month
            start_time = datetime.strptime(row[2], "%I:%M %p").time()
            net_value = float(row[6])

            # Check if the date is within the specified range
            if start_datetime <= date < end_datetime:
                # Identify the period
                period_identifier.identify_period(date, start_time)
                period = period_identifier.get_period()

                # Identify the season based on the start date
                season = "Winter" if month >= 11 or month <= 5 else "Summer"

                # Accumulate the net value by date range, season, and period
                totals_by_range[(start_datetime, end_datetime)][season][period] += net_value

    # Return the totals by date range, season, period, and total value
    return totals_by_range


if __name__ == "__main__":
    # Get user input for the start and end dates
    input_csv_file = "elec-5.22-5.23.csv"
    start_date_str = input("Enter the start date (MM/DD/YYYY), or press Enter for default: ").strip() or None
    end_date_str = input("Enter the end date (MM/DD/YYYY), or press Enter for default: ").strip() or None

    totals = calculate_totals(input_csv_file, start_date_str, end_date_str)

    # Load the pricing plans from the YAML file
    pricing_plans = load_plans()

    # Prompt the user to select a pricing plan
    print("Available Pricing Plans:")
    for i, plan in enumerate(pricing_plans, 1):
        print(f"{i}. {plan['name']}")

    selected_plan_index = int(input("Select a pricing plan (enter the number): ")) - 1
    selected_plan = pricing_plans[selected_plan_index]

    # Print the totals by date range, season, period, and total value
    for date_range, season_totals in totals.items():
        start_date, end_date = date_range
        print(f"\nDate Range: {start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}")

        for season, time_totals in season_totals.items():
            season_plan = selected_plan[season.lower()]
            print()
            print(season)
            print(f"On Peak: \t{time_totals['On Peak']:.3f} kWh \t(Cost: ${time_totals['On Peak'] * season_plan['on_peak']:.2f})")
            print(f"Off Peak: \t{time_totals['Off Peak']:.3f} kWh \t(Cost: ${time_totals['Off Peak'] * season_plan['off_peak']:.2f})")
            print(f"Super Off Peak: {time_totals['Super Off Peak']:.3f} kWh \t(Cost: ${time_totals['Super Off Peak'] * season_plan['super_off_peak']:.2f})")

        combined_total = sum(sum(time_totals.values()) for time_totals in season_totals.values())
        combined_cost = (
            time_totals['On Peak'] * season_plan['on_peak']
            + time_totals['Off Peak'] * season_plan['off_peak']
            + time_totals['Super Off Peak'] * season_plan['super_off_peak']
            + selected_plan['service_fee']
        )
        print(f"\nCombined Total: {combined_total:.3f} kWh (Cost: ${combined_cost:.2f})")
