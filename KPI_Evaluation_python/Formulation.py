import numpy as np

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

        self.metrics = {}

    def FF_Pdelta(self):
        FF_Pdelta = (np.sum(self.sorted_Price_market[:12] * self.sorted_P_delta[:12]) - 
                     np.sum(self.sorted_Price_market[12:] * self.sorted_P_delta[12:])) / (
                    np.sum(self.sorted_Price_market[:12] * self.sorted_P_delta[:12]) + 
                    np.sum(self.sorted_Price_market[12:] * self.sorted_P_delta[12:]))
        self.metrics['FF_Pdelta'] = FF_Pdelta

    def FF_Pcons(self):
        FF_Pcons = (np.sum(self.sorted_Price_tarrif[:12] * self.sorted_P_cons[:12]) - 
                    np.sum(self.sorted_Price_tarrif[12:] * self.sorted_P_cons[12:])) / (
                   np.sum(self.sorted_Price_tarrif[:12] * self.sorted_P_cons[:12]) + 
                   np.sum(self.sorted_Price_tarrif[12:] * self.sorted_P_cons[12:]))
        self.metrics['FF_Pcons'] = FF_Pcons

    def FF_PC_Pcons(self):
        denominator = (np.sum(self.sorted_Price_tarrif[23] * self.sorted_P_cons) - 
                       np.sum(self.sorted_Price_tarrif[0] * self.sorted_P_cons))
        if denominator != 0:
            FF_PC_Pcons = ((np.sum(self.sorted_Price_tarrif[23] * self.sorted_P_cons) - 
                            np.sum(self.sorted_Price_tarrif * self.sorted_P_cons)) / denominator)
            self.metrics['FF_PC_Pcons'] = FF_PC_Pcons
            return FF_PC_Pcons
        else:
            print('Division by zero in FF_PC_Pcons')
            return None

    def FF_PC_Pdelta(self):
        denominator = (np.sum(self.sorted_Price_market[23] * self.sorted_P_delta) - 
                       np.sum(self.sorted_Price_market[0] * self.sorted_P_delta))
        if denominator != 0:
            FF_PC_Pdelta = ((np.sum(self.sorted_Price_market[23] * self.sorted_P_delta) - 
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