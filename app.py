from flask import Flask, render_template, request
import csv
from collections import defaultdict
from datetime import datetime
import yaml

from holiday_date_identifier import HolidayDateIdentifier
from main_script import load_plans, calculate_totals
from period_identifier import PeriodIdentifier

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", enumerate=enumerate, pricing_plans=load_plans())

@app.route("/calculate", methods=["POST"])
def calculate():
    input_csv_file = "elec-5.22-5.23.csv"
    start_date_str = request.form.get("start_date") or None
    end_date_str = request.form.get("end_date") or None

    totals = calculate_totals(input_csv_file, start_date_str, end_date_str)
    pricing_plans = load_plans()

    # Prompt the user to select a pricing plan
    selected_plan_index = int(request.form.get("pricing_plan")) - 1
    selected_plan = pricing_plans[selected_plan_index]

    for _, season_totals in totals.items():
        for season, time_totals in season_totals.items():
            season_plan = selected_plan[season.lower()]
            combined_total = sum(sum(time_totals.values()) for time_totals in season_totals.values())
            combined_cost = (
                time_totals['On Peak'] * season_plan['on_peak']
                + time_totals['Off Peak'] * season_plan['off_peak']
                + time_totals['Super Off Peak'] * season_plan['super_off_peak']
                + selected_plan['service_fee']
            )

    return render_template("results.html", totals=totals, selected_plan=selected_plan, combined_total=combined_total, combined_cost=combined_cost)

if __name__ == "__main__":
    app.run()
