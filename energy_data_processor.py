from collections import defaultdict
from datetime import datetime

from holiday_date_identifier import HolidayDateIdentifier
from period_identifier import PeriodIdentifier


class EnergyDataProcessor:
    def __init__(self, start_date_str=None, end_date_str=None):
        self.start_date_str = start_date_str
        self.end_date_str = end_date_str

    def calculate_cost(time_totals, season_plan):
        return time_totals * season_plan

    def calculate_totals(self, input_data, solar_intensity_data=None):
        # Create nested defaultdicts to store the totals by date range, on peak/off peak/super off peak, and total value
        totals_by_range = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        # Skip the header row
        input_data = input_data[1:]

        # Determine the start and end dates based on the CSV data
        dates = [datetime.strptime(row[1], "%m/%d/%Y") for row in input_data]
        start_datetime = min(dates) if self.start_date_str is None else datetime.strptime(self.start_date_str, "%m/%d/%Y")
        end_datetime = max(dates) if self.end_date_str is None else datetime.strptime(self.end_date_str, "%m/%d/%Y")

        # Define a list of holidays (in datetime format)
        holidays = HolidayDateIdentifier().get_holidays_in_date_range(start_datetime, end_datetime)

        # Create an instance of the PeriodIdentifier class
        period_identifier = PeriodIdentifier(holidays)

        # Iterate through each row in the CSV
        for row in input_data:
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

                if solar_intensity_data:
                    # Deduct the solar intensity from the net value
                    net_value -= solar_intensity_data.get(date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0), 0)

                # Accumulate the net value by date range, season, and period
                totals_by_range[(start_datetime, end_datetime)][season][period] += net_value

        # Return the totals by date range, season, period, and total value
        print("totals_by_range", totals_by_range)
        return totals_by_range

    def calculate_totals_by_month(self, input_data, solar_intensity_data=None):
        # Create nested defaultdicts to store the totals by month, season, period, and total value
        totals_by_month = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        # Skip the header row
        input_data = input_data[1:]

        # Determine the start and end dates based on the CSV data
        dates = [datetime.strptime(row[1], "%m/%d/%Y") for row in input_data]
        start_datetime = min(dates) if self.start_date_str is None else datetime.strptime(self.start_date_str, "%m/%d/%Y")
        end_datetime = max(dates) if self.end_date_str is None else datetime.strptime(self.end_date_str, "%m/%d/%Y")

        # Define a list of holidays (in datetime format)
        holidays = HolidayDateIdentifier().get_holidays_in_date_range(start_datetime, end_datetime)

        # Create an instance of the PeriodIdentifier class
        period_identifier = PeriodIdentifier(holidays)

        # Iterate through each row in the CSV
        for row in input_data:
            # Extract the date, start time, and net value from the row
            date = datetime.strptime(row[1], "%m/%d/%Y")
            month = date.month
            month_str = date.strftime("%B %Y")
            start_time = datetime.strptime(row[2], "%I:%M %p").time()
            net_value = float(row[6])

            # Check if the date is within the specified range
            if start_datetime <= date < end_datetime:
                # Identify the period
                period_identifier.identify_period(date, start_time)
                period = period_identifier.get_period()

                # Identify the season based on the month
                season = "Winter" if month >= 11 or month <= 5 else "Summer"

                if solar_intensity_data:
                    # Deduct the solar intensity from the net value
                    net_value -= solar_intensity_data.get(
                        date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0), 0
                    )

                # Accumulate the net value by month, season, period, and total value
                totals_by_month[month_str][season][period] += net_value

        # Convert the defaultdict objects to regular dictionaries for ease of use
        totals_by_month = dict(totals_by_month)
        for month, month_data in totals_by_month.items():
            totals_by_month[month] = dict(month_data)
            for season, season_data in month_data.items():
                totals_by_month[month][season] = dict(season_data)

        # Return the totals by month, season, period, and total value
        return totals_by_month
