import os
import json
import logging
from Metric_Calculator1 import MetricCalculator
import sys
import xlsxwriter 
from pathlib import Path
import yaml

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def write_to_excel(metrics, dir, run_id):
    file_path = Path(dir) / f'KPI_outputs_{run_id}.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for k, v in metrics.items():
        worksheet.write(row, col, k)
        worksheet.write(row, col + 1, float(v))
        row += 1
    workbook.close()
def write_to_json(metrics, dir, run_id):
    file_path = Path(dir) / f'KPI_outputs_{run_id}.json'
    with open(file_path, 'w') as json_file:
        json.dump(metrics, json_file, indent=4)

def calculate_metrics(data, data_simulink, data_opt, data_base, dir, run_id):
    metric_calculator = MetricCalculator(data, data_simulink, data_opt,data_base)
    MC = metric_calculator
    MC.FF()
    MC.FF_base()
    MC.FF_W()
    MC.FF_SB()
    MC.FF_shift()
    MC.Eff_el()
    MC.Eff_th()
    MC.Eff()
    MC.LCOE()
    MC.Capex()
    MC.Annual_Opex()
    MC.Opex_Per_kWh()
    MC.Co2_emission()
    # print(MC.calculate())
    # for k, v in MC.calculate().items():
    #     print(f"{k}: {float(v)}")


    metrics = MC.calculate()
    print(metrics)
    write_to_excel(metrics, dir, run_id)
    write_to_json(metrics, dir, run_id)

def main(file_name, dir):
    logging.info("Starting the metric calculation process")
    file_path1 = os.path.join( dir, f'{file_name}_KPI.json')
    data = read_json_file(file_path1)
    file_path2 = os.path.join( dir, f'config_{file_name}.yaml')
    file_path3 = os.path.join( dir, f'{file_name}.yaml')
    with open(file_path2, 'r') as file:
        data_opt = yaml.safe_load(file)
    with open(file_path3, 'r') as file:
        data_simulink = yaml.safe_load(file)
    file_path_base= os.path.join( dir, f'Base_case_KPI.json')
    data_base= read_json_file(file_path_base)
    calculate_metrics(data, data_simulink, data_opt, data_base, dir, run_id)

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
    main(file_name, dir)