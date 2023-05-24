# SDGE Bill Calculator

This repository contains a Python utility for San Diego Gas & Electric (SDGE) customers to calculate the cost of their electricity bills based on past usage and different Time of Use (TOU) pricing plans.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

You will need Python 3.7 or later to run this utility.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SDGEBillCalculator.git
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```


## Usage

The utility reads a "Green Button" CSV file containing your past usage data, and it calculates costs for various TOU pricing plans.

To use it:

1. Prepare a "Green Button" CSV file with your past usage data.
2. Update the `plans.yml` file with your TOU pricing plans.
3. Run the main script and follow the prompts to input the start and end dates and select a pricing plan:
```bash
python3 main_script.py
```
The utility will output the total kilowatt-hours and cost for each period (On Peak, Off Peak, Super Off Peak) and season (Winter, Summer), as well as the combined total and cost.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
