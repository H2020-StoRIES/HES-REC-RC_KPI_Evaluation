import os
import json
import logging
from Metric_Calculator import MetricCalculator
import sys

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_metrics(data):
    metric_calculator = MetricCalculator(data)
    MC = metric_calculator
    MC.FF()
    MC.FF_base()
    MC.FF_W()
    MC.FF_SB()
    MC.FF_shift()
    MC.Eff()
    print(MC.calculate())
    for k, v in MC.calculate().items():
        print(f"{k}: {float(v)}")

def main(file_name, dir):
    logging.info("Starting the metric calculation process")
    file_path1 = os.path.join( dir, file_name)
    data = read_json_file(file_path1)
    calculate_metrics(data)

if __name__ == "__main__":
    # file_name = 'OUT_20240926T142612_KPI.json'
    # dir = os.path.dirname(__file__)
    if len(sys.argv) != 3:
        print("Usage: python KPI_evaluation.py <file_name> <dir>")
        sys.exit(1)
    file_name = sys.argv[1]
    dir = sys.argv[2]
    print(f"file_name: {file_name}, dir: {dir}")
    main(file_name, dir)