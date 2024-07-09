import numpy as np
from config import Config
midian = Config.get_config().midian
T = Config.get_config().T

class Flexibility:
    def __init__(self, data):
        self.data = data

        # Sort the data
        self.sorted_indices = np.argsort(data['Price_market'])
        self.sorted_Price_market = data['Price_market'][self.sorted_indices]
        self.sorted_P_el_in = data['P_el_in'][self.sorted_indices]
        self.sorted_P_el_out = data['P_el_out'][self.sorted_indices]
        self.sorted_P_delta = data['P_delta'][self.sorted_indices]

        self.sorted_indices1 = np.argsort(data['Price_tarrif'])
        self.sorted_Price_tarrif = data['Price_tarrif'][self.sorted_indices1]
        self.sorted_P_cons = data['P_cons'][self.sorted_indices1]
        self.sorted_P_ESS = data['P_ESS'][self.sorted_indices1]
        self.sorted_P_delta_base = data['P_delta_base'][self.sorted_indices1]
        self.sorted_P_el_in_base = data['P_el_in_base'][self.sorted_indices1]
        self.sorted_P_el_out_base = data['P_el_out_base'][self.sorted_indices1]
        self.export_P_delta_base = np.where(self.sorted_P_delta_base < 0, self.sorted_P_delta_base, 0)
        self.import_P_delta_base = np.where(self.sorted_P_delta_base > 0, self.sorted_P_delta_base, 0)   
        self.export_P_delta = np.where(self.sorted_P_delta < 0, self.sorted_P_delta, 0) 
        self.import_P_delta = np.where(self.sorted_P_delta > 0, self.sorted_P_delta, 0)
        
        self.metrics = {}

    def FF_Pdelta(self):
        FF_Pdelta = (np.sum(self.sorted_Price_market[:midian] * self.sorted_P_delta[:midian]) - 
                     np.sum(self.sorted_Price_market[midian:] * self.sorted_P_delta[midian:])) / (
                    np.sum(self.sorted_Price_market[:midian] * self.sorted_P_delta[:midian]) + 
                    np.sum(self.sorted_Price_market[midian:] * self.sorted_P_delta[midian:]))
        self.metrics['FF_Pdelta'] = FF_Pdelta

    def FF_Pcons(self):
        FF_Pcons = (np.sum(self.sorted_Price_tarrif[:midian] * self.sorted_P_cons[:midian]) - 
                    np.sum(self.sorted_Price_tarrif[midian:] * self.sorted_P_cons[midian:])) / (
                   np.sum(self.sorted_Price_tarrif[:midian] * self.sorted_P_cons[:midian]) + 
                   np.sum(self.sorted_Price_tarrif[midian:] * self.sorted_P_cons[midian:]))
        self.metrics['FF_Pcons'] = FF_Pcons

    def FF_PC_Pcons(self):
        denominator = (np.sum(self.sorted_Price_tarrif[T-1] * self.sorted_P_cons) - 
                       np.sum(self.sorted_Price_tarrif[0] * self.sorted_P_cons))
        if denominator != 0:
            FF_PC_Pcons = ((np.sum(self.sorted_Price_tarrif[T-1] * self.sorted_P_cons) - 
                            np.sum(self.sorted_Price_tarrif * self.sorted_P_cons)) / denominator)
            self.metrics['FF_PC_Pcons'] = FF_PC_Pcons
            return FF_PC_Pcons
        else:
            print('Division by zero in FF_PC_Pcons')
            return None

    def FF_PC_Pdelta(self):
        denominator = (np.sum(self.sorted_Price_market[T-1] * self.sorted_P_delta) - 
                       np.sum(self.sorted_Price_market[0] * self.sorted_P_delta))
        if denominator != 0:
            FF_PC_Pdelta = ((np.sum(self.sorted_Price_market[T-1] * self.sorted_P_delta) - 
                             np.sum(self.sorted_Price_market * self.sorted_P_delta)) / denominator)
            self.metrics['FF_PC_Pdelta'] = FF_PC_Pdelta
            return FF_PC_Pdelta
        else:
            print('Division by zero in FF_PC_Pdelta')
            return None

    def FF_VS_Pdelta(self, FF_PC_ref, FF_PC_Pdelta):
        if FF_PC_Pdelta != 0:
            FF_VS_Pdelta = (FF_PC_Pdelta - FF_PC_ref) / FF_PC_Pdelta
            self.metrics['FF_VS_Pdelta'] = FF_VS_Pdelta
        else:
            print('Division by zero in FF_VS_Pdelta')

    def FF_VS_Pcons(self, FF_PC_ref, FF_PC_Pcons):
        if FF_PC_Pcons != 0:
            FF_VS_Pcons = (FF_PC_Pcons - FF_PC_ref) / FF_PC_Pcons
            self.metrics['FF_VS_Pcons'] = FF_VS_Pcons
        else:
            print('Division by zero in FF_VS_Pcons')
    def FF (self):
        if sum(self.export_P_delta) != 0 or sum(self.import_P_delta) != 0:
            # FF = 0.5*(np.sum(self.import_P_delta[:midian]) /np.sum(self.import_P_delta) + np.sum(self.export_P_delta[midian:]) /np.sum(self.export_P_delta))
            FF = (np.sum(self.import_P_delta[:midian])+np.sum(self.export_P_delta[midian:])) /(np.sum(self.import_P_delta) + np.sum(self.export_P_delta))

            self.metrics['FF'] = FF
        else:
            print('Division by zero in FF')
    def FF_base (self):
        if sum(self.export_P_delta_base) != 0 or sum (self.import_P_delta_base) != 0:
            # FF_base = 0.5*(np.sum(self.import_P_delta_base[:midian]) /np.sum(self.import_P_delta_base) + np.sum(self.export_P_delta_base[midian:]) /np.sum(self.export_P_delta_base))
            FF_base = (np.sum(self.import_P_delta_base[:midian])+np.sum(self.export_P_delta_base[midian:])) /(np.sum(self.import_P_delta_base) + np.sum(self.export_P_delta_base))
            self.metrics['FF_base'] = FF_base
        else:
            print('Division by zero in FF_base')

    def FF_W (self):
        if sum (self.export_P_delta) != 0 or sum(self.import_P_delta) != 0:
            lpt_Avg = np.average(self.sorted_Price_market[:midian])
            hpt_Avg = np.average(self.sorted_Price_market[midian:])
            # FF_W = 0.5*(np.sum(self.import_P_delta[:midian])*lpt_Avg /np.sum(self.import_P_delta) + np.sum(self.export_P_delta[midian:])*hpt_Avg /np.sum(self.export_P_delta))/(lpt_Avg+hpt_Avg)
            FF_W =(np.sum(self.import_P_delta[:midian])*lpt_Avg +np.sum(self.export_P_delta[midian:])*hpt_Avg) /(np.sum(self.import_P_delta)*lpt_Avg  + np.sum(self.export_P_delta)*hpt_Avg)
            
            self.metrics['FF_W'] = FF_W
        else:
            print('Division by zero in FF')

    def FF_shift (self, FF, FF_base): 
        print(FF, FF_base)
        if FF != 0 and FF_base != 0 and FF is not None and FF_base is not None:
            FF_shift = (FF - FF_base) / FF * 100
            self.metrics['FF_shift'] = FF_shift

    def FF_SB (self):
        if sum(self.sorted_Price_market * self.sorted_P_delta_base) != 0:
            FF_SB = (sum(self.sorted_Price_market * self.sorted_P_delta) - sum(self.sorted_Price_market * self.sorted_P_delta_base)) / sum(self.sorted_Price_market * self.sorted_P_delta_base)*100
        
            self.metrics['FF_SB'] = FF_SB
        else:
            print('Division by zero in FF_SB')

    def calculate(self):
        return self.metrics



class efficiency:
    def __init__(self, data):
        self.data = data
    def Eff_1 (self):
        self.metrics['Eff'] = 10

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