from solar_intensity_calculator import SolarIntensityCalculator


if __name__ == "__main__":
    # Example usage
    solar_intensity = SolarIntensityCalculator(input("Enter zip code: "), int(input("Enter year: ")), int(input("Enter month: ")), float(input("Enter total energy for the month in kWh: ")))
    solar_intensity.print_hourly_intensity()
    solar_intensity.to_csv("solar_intensity.csv")
