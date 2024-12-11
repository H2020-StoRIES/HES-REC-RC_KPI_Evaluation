import os
import json
import logging
from Metric_Calculator import MetricCalculator
import sys
import xlsxwriter 
from pathlib import Path

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def write_to_excel(metrics, dir, run_id):
    file_path = Path(dir) / f'KPI_outputs_scenario_{run_id}.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for k, v in metrics.items():
        worksheet.write(row, col, k)
        worksheet.write(row, col + 1, float(v))
        row += 1
    workbook.close()

def calculate_metrics(data, run_id):
    metric_calculator = MetricCalculator(data)
    MC = metric_calculator
    MC.FF()
    MC.FF_base()
    MC.FF_W()
    MC.FF_SB()
    MC.FF_shift()
    MC.Eff()
    # print(MC.calculate())
    # for k, v in MC.calculate().items():
    #     print(f"{k}: {float(v)}")


    metrics = MC.calculate()
    write_to_excel(metrics, dir, run_id)

def main(file_name, dir, run_id):
    logging.info("Starting the metric calculation process")
    file_path1 = os.path.join( dir, f'{file_name}.json')
    data = read_json_file(file_path1)
    calculate_metrics(data, run_id)

if __name__ == "__main__":
    # file_name = 'OUT_20240926T142612_KPI.json'
    # dir = os.path.dirname(__file__)
    if len(sys.argv) != 4:
        print("Usage: python KPI_evaluation.py <file_name> <dir>")
        sys.exit(1)
    file_name = sys.argv[1]
    dir = sys.argv[2]
    run_id = sys.argv[3]
    print(f"file_name: {file_name}, dir: {dir}")
    main(file_name, dir, run_id)