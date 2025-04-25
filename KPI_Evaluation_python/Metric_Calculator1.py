import random
import numpy as np
random.seed(5)

from config import Config
import logging
from logging_util import setup_logging
setup_logging()
# Open and read the JSON file



T= Config.T
median = Config.get_config().median
class MetricCalculator():
    def __init__(self, data1, data_base):
        
        self.Price_export = np.array(data1['EP_con']) # Generated values for the price export
        self.Price_import = np.array(data1['EP_gen']) # Generated values for the price import
        self.P_delta = np.array(data1['Pe_grid']) 
        self.P_import= -np.where(self.P_delta < 0, self.P_delta, 0)
        self.P_export= np.where(self.P_delta > 0, self.P_delta, 0)
        self.P_delta_base = np.array(data_base['Pe_grid'])
        self.P_import_base =- np.where(self.P_delta_base < 0, self.P_delta_base, 0)
        self.P_export_base = np.where(self.P_delta_base > 0, self.P_delta_base, 0)
        self.P_CT_rk= np.array(data1['P2rk']) #Power to Rankine Cycle
        self.Pt_grid= np.array(data1['Pt_grid'])
        self.Pt_import =- np.where(self.Pt_grid < 0, self.Pt_grid, 0)
        self.Pt_export = np.where(self.Pt_grid > 0, self.Pt_grid, 0)
        self.sorted_indices_export = np.argsort(self.Price_export)
        self.sorted_Price_export = self.Price_export[self.sorted_indices_export]
        self.sorted_P_export= self.P_export[self.sorted_indices_export]
        self.sorted_indices_import = np.argsort(self.Price_import)   
        self.sorted_Price_import = self.Price_import[self.sorted_indices_import]  
        self.sorted_P_import = self.P_import[self.sorted_indices_import]   
        self.sorted_P_import_base = self.P_import_base[self.sorted_indices_import]
        self.sorted_P_export_base = self.P_export_base[self.sorted_indices_export]
        self.Total_El_load = np.array(data1 ['Total_El_load'])
        self.Total_Th_load = np.array(data1 ['Total_Th_load'])
        self.Total_El_Gen = np.array(data1['Total_El_Gen'])
        self.Total_Th_Gen = np.array(data1['Total_Th_Gen'])  
        self.E_th_ext= sum(self.Pt_grid[:T])
        self.metrics = {}
        


    def FF (self):
        sum_export= sum(self.sorted_P_export)
        sum_import= sum (self.sorted_P_import)
        sum_import_lpt= sum(self.sorted_P_import[:median])
        sum_export_hpt= sum(self.sorted_P_export[median:])
        total_Exchange= (sum_export + sum_import)
        if total_Exchange != 0:
            FF = (sum_export_hpt+sum_import_lpt) /(sum_export + sum_import)
            self.metrics['FF'] = FF
        elif total_Exchange == 0:
            self.metrics['FF'] = None
            print('Division by zero in FF')
            logging.error('Division by zero in FF')
    def FF_base (self):
        sum_export_base= sum(self.sorted_P_export_base)
        sum_import_base= sum (self.sorted_P_import_base)
        sum_import_lpt_base= sum(self.sorted_P_import_base[:median])
        sum_export_hpt_base= sum(self.sorted_P_export_base[median:])
        if sum_export_base + sum_import_base != 0:
            # FF_base = 0.5*(sum(self.import_P_delta_base[:median]) /sum(self.import_P_delta_base) + sum(self.export_P_delta_base[median:]) /sum(self.export_P_delta_base))
            FF_base = (sum_export_hpt_base+sum_import_lpt_base) /(sum_export_base + sum_import_base)
            self.metrics['FF_base'] = FF_base
        else:
            self.metrics['FF_base'] = None
            print('Division by zero in FF_base')
            logging.error('Division by zero in FF_base')

    def FF_W (self):
        cost_import = sum(self.sorted_P_import*self.sorted_Price_import)
        cost_export = sum(self.sorted_P_export * self.sorted_Price_export)
        cost_import_max= max(self.sorted_Price_import)*sum(self.sorted_P_import_base)
        cost_export_max= max(self.sorted_Price_export)*sum(self.sorted_P_export_base)
        cost_import_min= min(self.sorted_Price_import)*sum(self.sorted_P_import_base)
        cost_export_min= min(self.sorted_Price_export)*sum(self.sorted_P_export_base)
        print(cost_import, cost_export)
        print(cost_import_max, cost_import_min, cost_export_max, cost_export_min)
        if (cost_import_max - cost_import_min) != 0 and (cost_export_max - cost_export_min) != 0:
            FF_W = 0.5* ((cost_import_max-cost_import)/(cost_import_max-cost_import_min) + (cost_export-cost_export_min)/(cost_export_max-cost_export_min))
            self.metrics['FF_W'] = FF_W
        elif (cost_import_max - cost_import_min) == 0:
            FF_W = 0.5*(cost_export-cost_export_min)/(cost_export_max-cost_export_min)
            self.metrics['FF_W'] = FF_W
        elif (cost_export_max - cost_export_min) == 0:
            FF_W = 0.5*(cost_import_max-cost_import)/(cost_import_max-cost_import_min)
            self.metrics['FF_W'] = FF_W
        else:
            self.metrics['FF_W'] = None
            print('Division by zero in FF_W')
            logging.error('Division by zero in FF_W')

    def FF_shift (self):
        FF= self.metrics['FF']
        FF_base= self.metrics['FF_base']
        if FF != 0 and FF_base != 0 and FF is not None and FF_base is not None:
            FF_shift = (FF - FF_base) / FF * 100
            self.metrics['FF_shift'] = FF_shift
        else:
            self.metrics['FF_shift'] = None
            print('Division by zero in FF_shift')
            logging.error('Division by zero in FF_shift')

    def FF_SB (self):
        import_cost_base = sum(self.sorted_P_import_base*self.sorted_Price_import)
        export_cost_base = sum(self.sorted_P_export_base * self.sorted_Price_export)
        import_cost = sum(self.sorted_P_import*self.sorted_Price_import)
        export_cost = sum(self.sorted_P_export * self.sorted_Price_export)
        if export_cost_base - import_cost_base != 0:
            FF_SB = ((export_cost -import_cost) - ( export_cost_base - import_cost_base))/ ( export_cost_base - import_cost_base)*100
            self.metrics['FF_SB'] = FF_SB
        else:
            self.metrics['FF_SB'] = None
            print('Division by zero in FF_SB')
            logging.error('Division by zero in FF_SB')
    
    def Eff (self):        
        # Eff= (abs(sum(self.Total_El_load))+abs(sum(self.P_export )))/(abs(sum(self.Total_El_Gen))+abs(sum(self.P_import))+abs(sum(self.P_CT_rk)))
        Eff = (
            abs(sum(self.Total_El_load)) + abs(sum(self.P_export))
        ) / (
            abs(sum(self.Total_El_Gen)) + abs(sum(self.P_import)) + 0.38 * abs(sum(self.P_CT_rk))
        )
        self.metrics['Eff'] = Eff   
    def Eff_th (self):
        # Eff_th= (abs(sum(self.Total_Th_load))+abs(sum(self.Pt_export))+abs(sum(self.P_CT_rk)))/(abs(sum(self.Total_Th_Gen))+abs(sum(self.Pt_import)))
        Eff_th = (
            abs(sum(self.Total_Th_load)) + abs(sum(self.Pt_export))
        ) / (
            abs(sum(self.Total_Th_Gen)) + abs(sum(self.Pt_import))
        )        
        self.metrics['Eff_th'] = Eff_th
    def LCOE (self):
        self.metrics['LCOE'] = 0
    def calculate(self):
        return self.metrics