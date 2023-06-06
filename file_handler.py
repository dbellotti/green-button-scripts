import csv
import os
from collections import defaultdict
from datetime import datetime
import yaml


class FileHandler:
    def __init__(self):
        pass

    def read_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            return [row for row in reader]
    
    def read_yaml(self, yaml_file):
        with open(yaml_file, "r") as file:
            return yaml.safe_load(file)
