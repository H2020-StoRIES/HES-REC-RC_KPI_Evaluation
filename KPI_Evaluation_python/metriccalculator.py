import random
import numpy as np
random.seed(5)
import json
import os
from config import Config
# Open and read the JSON file

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Construct the full path to the JSON files
file_path1 = os.path.join(current_dir, 'OUT_20240827T134053_KPI.json')
file_path2 = os.path.join(current_dir, 'OUT_20240827T134053.json')

# Open and read the JSON files
with open(file_path1, 'r') as file:
    data2 = json.load(file)

with open(file_path2, 'r') as file1:
    data1 = json.load(file1)
T= Config.T
class MetricCalculator():
    def __init__(self):
        
        self.Price_export = np.array(data2['EP_con']) # Generated values for the price export
        self.Price_import = np.array(data2['EP_gen'] )# Generated values for the price import
        self.P_delta = np.array(data2['Pe_grid'])        
        self.P_import= -np.where(self.P_delta < 0, self.P_delta, 0)
        self.P_export= np.where(self.P_delta > 0, self.P_delta, 0)
        rand_var= max(max(self.P_import),  max(self.P_export))
        self.P_import_base =- np.array([round(random.uniform(-rand_var, 0), 2) for _ in range(T)])
        self.P_export_base = np.array([round(random.uniform(0, rand_var), 2) for _ in range(T)])
        self.P_CT_WD= data1['P_CT_WD'] # Hourly power of wind turbine
        self.P_CT_PV= data1['P_CT_PV'] # Hourly power of PV
        self.P_c_Cbu= data1['P_c_Cbu'] #   Hourly consumption of the building
        self.P_c_CEV=  data1['P_c_CEV'] # Hourly consumption of the EV
        self.P_c_CPl= data1['P_c_CPl'] # Hourly consumption of the pelletizer?!
        self.P_ess_BAT= data1['P_ess_BAT'] # Hourly power charged by the battery
        self.P_ess_SC= data1['P_ess_SC'] # Hourly power charged by the supercapacitor
        self.P_ess_HP= data1['P_ess_HP'] # Hourly power charged by the heat pump
        self.P_CT_rk= data1['P_CT_rk'] #??
        self.P_gri= data1['e_gri'] # Hourly grid exchange
        self.SOC_BAT= data1['SOC_BAT'] # Hourly state of charge of the battery
        self.SOC_SC= data1['SOC_SC'] # Hourly state of charge of the supercapacitor
        self.SOC_HP= data1['SOC_HP'] # Hourly state of charge of the heat pump
        self.E_CT_WD= sum (self.P_CT_WD[:T]) # Energy of the wind turbine
        self.E_CT_PV= sum (self.P_CT_PV[:T]) # Energy of the PV
        self.E_c_Cbu= sum (self.P_c_Cbu[:T]) # Energy of the building
        self.E_c_CEV= sum (self.P_c_CEV[:T])
        self.E_c_CPl= sum (self.P_c_CPl[:T])
        self.E_ess_BAT= sum (self.P_ess_BAT[:T])
        self.E_ess_SC= sum (self.P_ess_SC[:T])
        self.E_ess_HP= sum (self.P_ess_HP[:T])
        self.E_CT_rk= sum (self.P_CT_rk[:T])
        self.E_gri= sum (self.P_gri[:T])

# Eff1= 
#         self.data = {}

    def calculate(self):
        keys= [ 'Price_export', 'Price_import', 'P_delta', 'P_import', 'P_export', 
               'P_import_base', 'P_export_base']
        values= [ self.Price_export, self.Price_import, self.P_delta, self.P_import, self.P_export, 
                 self.P_import_base, self.P_export_base]
        self.data_flex = dict(zip(keys, values))
        keys1= ['P_CT_WD', 'P_CT_PV', 'P_c_Cbu', 'P_c_CEV', 'P_c_CPl', 'P_ess_BAT', 'P_ess_SC',
                 'P_ess_HP', 'P_CT_rk', 'P_gri', 'SOC_BAT', 'SOC_SC', 'SOC_HP']
        
        values1= [self.P_CT_WD, self.P_CT_PV, self.P_c_Cbu, self.P_c_CEV, self.P_c_CPl, self.P_ess_BAT, self.P_ess_SC,
                    self.P_ess_HP, self.P_CT_rk, self.P_gri, self.SOC_BAT, self.SOC_SC, self.SOC_HP]
        
        self.data_eff = dict(zip(keys1, values1))

        return self.data_flex , self.data_eff

metric_calculator = MetricCalculator()
data_flex, data_eff = metric_calculator.calculate()
# Call the calculate method

