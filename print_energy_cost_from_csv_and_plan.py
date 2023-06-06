from file_handler import FileHandler
from solar_intensity_reader import SolarIntensityReader
from energy_data_processor import EnergyDataProcessor
from user_input_handler import UserInputHandler
from energy_data_printer import EnergyDataPrinter

if __name__ == "__main__":
    # Get user input for the start and end dates
    user_input_handler = UserInputHandler()
    start_date_str, end_date_str = user_input_handler.get_date_input()

    file_handler = FileHandler()
    input_data = file_handler.read_csv("elec-5.22-5.23.csv")
    pricing_plans = file_handler.read_yaml("plans.yml")
    solar_intensity_data = SolarIntensityReader("solar_intensity.csv").read_solar_intensity()

    # Get selected pricing plan
    selected_plan = user_input_handler.get_plan_input(pricing_plans)

    # Calculate totals
    energy_data_processor = EnergyDataProcessor(start_date_str, end_date_str)

    # Print totals and costs
    energy_data_printer = EnergyDataPrinter()
    #energy_data_printer.print_totals_and_cost(energy_data_processor.calculate_totals(input_data, solar_intensity_data) , selected_plan)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    energy_data_printer.print_totals_and_cost_by_month(energy_data_processor.calculate_totals_by_month(input_data, solar_intensity_data) , selected_plan)
