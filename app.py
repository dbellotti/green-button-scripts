from flask import Flask, render_template, request
import csv
from collections import defaultdict
from datetime import datetime
import yaml

from csv_uploader import CSVUploader
from holiday_date_identifier import HolidayDateIdentifier
from file_handler import FileHandler
from energy_data_processor import EnergyDataProcessor
from energy_data_printer import EnergyDataPrinter
from period_identifier import PeriodIdentifier
from solar_intensity_reader import SolarIntensityReader

app = Flask(__name__)

file_handler = FileHandler()
pricing_plans = file_handler.read_yaml("plans.yml")

@app.route("/")
def index():
    return render_template("index.html", enumerate=enumerate, pricing_plans=pricing_plans)

@app.route("/calculate", methods=["POST"])
def calculate():
    # Use the uploader to handle file upload
    gb_uploader = CSVUploader(app, 'green_button_csv_file', 'example.csv')
    gb_input_csv_file = gb_uploader.upload()
    gb_input_data = file_handler.read_csv(gb_input_csv_file)
    spe_uploader = CSVUploader(app, 'solar_estimation_csv_file')
    spe_input_csv_file = spe_uploader.upload()
    solar_intensity_data = SolarIntensityReader(spe_input_csv_file).read_solar_intensity()

    start_date_str = request.form.get("start_date") or None
    end_date_str = request.form.get("end_date") or None

    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None


    # Calculate totals
    energy_data_processor = EnergyDataProcessor(start_date_str, end_date_str)
    totals_by_month = energy_data_processor.calculate_totals_by_month(gb_input_data, solar_intensity_data)

    # Prompt the user to select a pricing plan
    selected_plan_index = int(request.form.get("pricing_plan")) - 1
    selected_plan = pricing_plans[selected_plan_index]

    net_production = 0
    net_consumption = 0
    for _, season_totals in totals_by_month.items():

        for season, time_totals in season_totals.items():
            season_plan = selected_plan[season.lower()]

        monthly_total = sum(sum(time_totals.values()) for time_totals in season_totals.values())

        if monthly_total < 0:
            net_production += monthly_total * -0.04
        else:
            combined_cost = (
                sum(time_totals['On Peak'] * season_plan['on_peak'] for time_totals in season_totals.values())
                + sum(time_totals['Off Peak'] * season_plan['off_peak'] for time_totals in season_totals.values())
                + sum(time_totals['Super Off Peak'] * season_plan['super_off_peak'] for time_totals in season_totals.values())
                + selected_plan['monthly_service_fee']
            )
            net_consumption += combined_cost

    return render_template(
        "results.html",
        totals_by_month=totals_by_month,
        selected_plan=selected_plan,
        net_production=net_production,
        net_consumption=net_consumption,
        total_true_up_cost=net_consumption - net_production
    )

if __name__ == "__main__":
    app.run()
