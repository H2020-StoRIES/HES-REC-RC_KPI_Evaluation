import numpy as np
from config import Config
import logging
from logging_util import setup_logging
setup_logging()


median = Config.get_config().median
T = Config.get_config().T

class Flexibility:
    def __init__(self, data):
        self.sorted_indices_export = np.argsort(data['Price_export'])
        self.sorted_Price_export = data['Price_export'][self.sorted_indices_export]
        self.sorted_P_export= data['P_export'][self.sorted_indices_export]
        self.sorted_indices_import = np.argsort(data['Price_import'])   
        self.sorted_Price_import = data['Price_import'][self.sorted_indices_import]  
        self.sorted_P_import = data['P_import'][self.sorted_indices_import]   
        self.sorted_P_import_base = data['P_import_base'][self.sorted_indices_import]
        self.sorted_P_export_base = data['P_export_base'][self.sorted_indices_export]

        
        self.metrics = {}

    def FF (self):
        sum_export= sum(self.sorted_P_export)
        sum_import= sum (self.sorted_P_import)
        sum_import_lpt= np.sum(self.sorted_P_import[:median])
        sum_export_hpt= np.sum(self.sorted_P_export[median:])
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
        sum_import_lpt_base= np.sum(self.sorted_P_import_base[:median])
        sum_export_hpt_base= np.sum(self.sorted_P_export_base[median:])
        if sum_export_base + sum_import_base != 0:
            # FF_base = 0.5*(np.sum(self.import_P_delta_base[:median]) /np.sum(self.import_P_delta_base) + np.sum(self.export_P_delta_base[median:]) /np.sum(self.export_P_delta_base))
            FF_base = (sum_export_hpt_base+sum_import_lpt_base) /(sum_export_base + sum_import_base)
            self.metrics['FF_base'] = FF_base
        else:
            self.metrics['FF_base'] = None
            print('Division by zero in FF_base')
            logging.error('Division by zero in FF_base')

    def FF_W (self):
        cost_import = np.sum(self.sorted_P_import*self.sorted_Price_import)
        cost_export = np.sum(self.sorted_P_export * self.sorted_Price_export)
        cost_import_max= np.max(self.sorted_Price_import)*np.sum(self.sorted_P_import_base)
        cost_export_max= np.max(self.sorted_Price_export)*np.sum(self.sorted_P_export_base)
        cost_import_min= np.min(self.sorted_Price_import)*np.sum(self.sorted_P_import_base)
        cost_export_min= np.min(self.sorted_Price_export)*np.sum(self.sorted_P_export_base)
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
        import_cost_base = np.sum(self.sorted_P_import_base*self.sorted_Price_import)
        export_cost_base = np.sum(self.sorted_P_export_base * self.sorted_Price_export)
        import_cost = np.sum(self.sorted_P_import*self.sorted_Price_import)
        export_cost = np.sum(self.sorted_P_export * self.sorted_Price_export)
        if export_cost_base - import_cost_base != 0:
            FF_SB = ((export_cost -import_cost) - ( export_cost_base - import_cost_base))/ ( export_cost_base - import_cost_base)*100
            self.metrics['FF_SB'] = FF_SB
        else:
            self.metrics['FF_SB'] = None
            print('Division by zero in FF_SB')
            logging.error('Division by zero in FF_SB')

    def calculate(self):
        return self.metrics
    
class efficiency:
    def __init__(self, data):
        self.metrics = {}
        self.E_CT_WD= sum (data['P_CT_WD'][:T]) # Energy of the wind turbine
        self.E_CT_PV= sum (data['P_CT_PV'][:T]) # Energy of the PV
        self.E_c_Cbu= sum (data['P_c_Cbu'][:T]) # Energy of the building
        self.E_c_CEV= sum (data['P_c_CEV'][:T])
        self.E_c_CPl= sum (data['P_c_CPl'][:T])
        self.E_ess_BAT= sum (data['P_ess_BAT'][:T])
        P_ess_BAT_array = np.array(data['P_ess_BAT'][:T])
        self.E_ess_BAT_ch = np.sum(P_ess_BAT_array[P_ess_BAT_array < 0])
        self.E_ess_BAT_dis = np.sum(P_ess_BAT_array[P_ess_BAT_array > 0])
        self.P_ess_SC = data['P_ess_SC']  # Add this line to define self.P_ess_SC
        self.P_ess_HP = data['P_ess_HP']  # Add this line to define self.P_ess_HP
        self.P_CT_rk = data['P_CT_rk']  # Add this line to define self.P_CT_rk
        self.P_delta = data['P_delta']  # Add this line to define self.P_gri
        self.E_delta= sum(data['P_delta'][:T]) # Energy exchanged with the external grid
        self.E_ess_SC= sum (data['P_ess_SC'][:T])
        P_ess_SC_array = np.array(data['P_ess_SC'][:T])
        self.E_ess_SC_ch = np.sum(P_ess_SC_array[P_ess_SC_array < 0])
        self.E_ess_SC_dis = np.sum(P_ess_SC_array[P_ess_SC_array > 0])
        self.E_ess_HP= sum (data['P_ess_HP'][:T])
        self.E_CT_rk= sum (data['P_CT_rk'][:T])
        self.P_c_tbu= data['P_c_Ctbu']# Thermal consumption of the building
        self.E_c_tbu= sum(data['P_c_Ctbu'][:T]) # Energy of the building
        self.P_PCM= np.array(data['P_ess_PCM'][:T]) # Power of PCM Phase-change material
        self.E_PCM_ch= np.sum(P_ess_SC_array[P_ess_SC_array < 0] )# Energy charged by PCM Phase-change material
        self.E_PCM_dis= np.sum(P_ess_SC_array[P_ess_SC_array > 0])# Energy discharged by PCM Phase-change material
        self.P_csp= data['P_csp'] # Concentrated solar power
        self.E_csp= sum(data['P_csp'][:T]) # Energy of the concentrated solar power
        self.E_STP= sum(data['P_tsp'][:T]) # Solar thermal power
        self.E_th_ext= sum(data['Pt_grid'][:T]) # Thermal energy exchanged with the external grid
        self.data = data
    def Eff (self):
        E_El_consumption= self.E_c_Cbu+ self.E_c_CEV+ self.E_c_CPl #Electrical consumption
        E_th_consumption= self.E_c_tbu #Thermal consumption
        E_El_ESS_ch= self.E_ess_BAT_ch+self.E_ess_SC_ch #ESS Electrical energy charged
        E_th_ESS_ch= E_El_ESS_ch +self.E_PCM_ch #ESS Thermal energy charged
        E_El_ext= self.E_delta #​Electrical energy exchanged with the external grid
        E_th_ext= self.E_th_ext #Thermal energy exchanged with the external grid
        E_El_gen= self.E_CT_WD + self.E_CT_PV  #Electrical energy generated
        E_th_gen= self.E_csp+self.E_STP + self.E_CT_rk #Thermal energy generated
        E_ESS_El_dis= self.E_ess_BAT_dis+self.E_ess_SC_dis #ESS Electrical energy discharged
        E_ESS_th_dis= self.E_PCM_dis #ESS Thermal energy discharged
        Eff= (E_El_consumption + E_th_consumption + E_th_ESS_ch)/(E_El_ext +E_th_ext+
                E_El_gen+ E_th_gen+ E_ESS_El_dis+E_ESS_th_dis)
        
        self.metrics['Eff'] = Eff
    def calculate(self):
        return self.metrics
    


class CO2:
    def __init__(self, data):
        self.data = data
    def CO2 (self):
        self.metrics['CO2'] = 10

    def calculate(self):
        return self.metrics
    

class Operation:
    def __init__(self, data):
        self.data = data
    def Operation (self):
        self.metrics['Operation'] = 10

    def calculate(self):
        return self.metrics