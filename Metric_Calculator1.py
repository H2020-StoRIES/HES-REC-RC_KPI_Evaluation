import random
import numpy as np
random.seed(5)

T = 24
median = int(T/2)
class MetricCalculator():
    def __init__(self, data, data_simulink, data_opt,  data_base):
        
        self.Price_export = np.array(data['EP_con']) # Generated values for the price export
        self.Price_import = np.array(data['EP_gen']) # Generated values for the price import
        self.P_delta = np.array(data['Pe_grid']) /1000 # Power exchange with the grid in kW
        self.P_import= -np.where(self.P_delta < 0, self.P_delta, 0)
        self.P_export= np.where(self.P_delta > 0, self.P_delta, 0)
        self.P_delta_base = np.array(data_base['Pe_grid'])/1000 # Power exchange with the grid in kW
        self.P_import_base =- np.where(self.P_delta_base < 0, self.P_delta_base, 0)
        self.P_export_base = np.where(self.P_delta_base > 0, self.P_delta_base, 0)
        self.P_CT_rk= np.array(data['P2rk'])/1000 #Power to Rankine Cycle
        self.Pt_grid= np.array(data['Pt_grid'])/1000
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
        self.Total_El_load = sum(np.array(data ['Total_El_load']))/1000
        self.Total_Th_load = sum(np.array(data ['Total_Th_load']))/1000
        # self.Total_El_Gen = np.array(data['Total_El_Gen'])
        # self.Total_Th_Gen = np.array(data['Total_Th_Gen'])  
        self.cost_obj = np.array(data['cost_obj'])
        self.Cost_operation_ESS = np.array(data['Cost_operation_ESS'])
        self.Price_operational_PV= data_opt['Generation']['PV']['Cost_operational']
        self.Price_operational_WT= data_opt['Generation']['WT']['Cost_operational']
        self.Price_operational_TPS= data_opt['Generation']['TPS']['Cost_operational']
        self.Price_operational_CSP= data_opt['Generation']['CSP']['Cost_operational']
        self.Price_investment_PV= data_opt['Generation']['PV']['Capital_cost_per_module']
        self.Price_investment_WT= data_opt['Generation']['WT']['Capital_cost_per_module']
        self.Price_investment_TPS= data_opt['Generation']['TPS']['Capital_cost_per_module']
        self.Price_investment_CSP= data_opt['Generation']['CSP']['Capital_cost_per_module']
        self.Price_investment_Bat= data_opt['Electrcial_Storage_Units'][0][list(data_opt['Electrcial_Storage_Units'][0].keys())[0]]["Capital_cost_per_module"]
        self.Price_investment_sc= data_opt['Electrcial_Storage_Units'][1][list(data_opt['Electrcial_Storage_Units'][1].keys())[0]]["Capital_cost_per_module"]
        self.Price_investment_HP= data_opt['Electrcial_Storage_Units'][2][list(data_opt['Electrcial_Storage_Units'][2].keys())[0]]["Capital_cost_per_module"]
        self.Price_investment_PCM= data_opt['Thermal_Storage_Units'][0][list(data_opt['Thermal_Storage_Units'][0].keys())[0]]["Capital_cost_per_module"]
        self.Price_investment_RC= data_opt['Thermal_to_Electrical_Converters'][0][list(data_opt['Thermal_to_Electrical_Converters'][0].keys())[0]]["Capital_cost_per_module"]
        self.Ness_Bat= data_simulink['BAT_ESSm']["Ness"]
        self.Ness_sc= data_simulink['SC_ESSm']["Ness"]
        self.Ness_HP= data_simulink['HP_ESSm']["Ness"]
        self.Ness_PCM= data_simulink['PCM_ESS']["Ness"]
        self.Total_PV= sum(np.array(data["P_CT_PV"]))/1000
        self.Total_WT= sum(np.array(data["P_CT_WD"]))/  1000
        self.Total_TPS= sum(np.array(data["P_tsp"]))/1000
        self.Total_CSP= sum(np.array(data["P_csp"]))/1000
        self.Total_P2rk= sum(np.array(data["P2rk"]))/1000
        self.life_time= data_opt['General']['lifeTime']
        self.discount_rate= data_opt['General']['discountRate']
        self.CI_el= data_opt['General']['CI_el']
        self.CI_th= data_opt['General']['CI_th']
        self.Total_El_Gen= sum(np.array(data["P_CT_PV"]))/1000 + sum(np.array(data["P_CT_WD"])) /1000
        self.Total_Th_Gen= sum(np.array(data["P_tsp"]))/1000 + sum(np.array(data["P_csp"]))/1000
        self.Eta_RC= data_opt['Thermal_to_Electrical_Converters'][0][list(data_opt['Thermal_to_Electrical_Converters'][0].keys())[0]]["Eta_RC"] # Efficiency of the Rankine Cycle

        
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
            # logging.error('Division by zero in FF')
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
            # logging.error('Division by zero in FF_base')

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
            # logging.error('Division by zero in FF_W')

    def FF_shift (self):
        FF= self.metrics['FF']
        FF_base= self.metrics['FF_base']
        if FF != 0 and FF_base != 0 and FF is not None and FF_base is not None:
            FF_shift = (FF - FF_base) / FF * 100
            self.metrics['FF_shift'] = FF_shift
        else:
            self.metrics['FF_shift'] = None
            print('Division by zero in FF_shift')
            # logging.error('Division by zero in FF_shift')

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
            # logging.error('Division by zero in FF_SB')
    
    def Eff_el (self):        
        Eff_el = (
            abs(self.Total_El_load) + abs(sum(self.P_export))
        ) / (
            abs(self.Total_El_Gen) + abs(sum(self.P_import)) + self.Eta_RC * abs(sum(self.P_CT_rk))
        )
        self.metrics['Eff_el'] = Eff_el  
    def Eff_th (self):
        denominator = abs(self.Total_Th_Gen) + abs(sum(self.Pt_import))
        if denominator != 0:
            Eff_th = (
                abs(self.Total_Th_load) + abs(sum(self.Pt_export))
                + abs(sum(self.P_CT_rk))
            ) / denominator
            self.metrics['Eff_th'] = Eff_th
        else:
            self.metrics['Eff_th'] = None
            print('Division by zero in Eff_th calculation')
            # logging.error('Division by zero in Eff_th calculation')
    def Eff (self):
        Eff = (
            abs(self.Total_El_load) + abs(sum(self.P_export))
            + abs(self.Total_Th_load) + abs(sum(self.Pt_export)) + abs(sum(self.P_CT_rk))
        ) / (
            abs(self.Total_El_Gen) + abs(sum(self.P_import)) + self.Eta_RC * abs(sum(self.P_CT_rk))
            + abs(self.Total_Th_Gen) + abs(sum(self.Pt_import))
        )
        self.metrics['Eff'] = Eff
    def Cost_investment_ESS (self):
        Cost_investment_ESS = (self.Price_investment_Bat * self.Ness_Bat + self.Price_investment_sc * self.Ness_sc + self.Price_investment_HP * self.Ness_HP) + self.Price_investment_PCM * self.Ness_PCM
        return Cost_investment_ESS
    def Cost_investment_Generation (self):
        Cost_investment_Generation = self.Price_investment_PV + self.Price_investment_WT  + self.Price_investment_TPS + self.Price_investment_CSP + self.Price_investment_RC
        return Cost_investment_Generation
    def Cost_operation_Generation (self):
        Cost_operation_Generation = self.Price_operational_PV*self.Total_PV + self.Price_operational_WT*self.Total_WT + self.Price_operational_TPS*self.Total_TPS + self.Price_operational_CSP*self.Total_CSP
        return Cost_operation_Generation

    def LCOE (self):
        LCOE_numinator = 0
        LCOE_denominator = 0
        for t in range(int(self.life_time)+1):
            self.Cost_investment_Generation1 = self.Cost_investment_Generation()/25 * (1 + self.discount_rate) ** (-t)
            self.Cost_investment_ESS1 = self.Cost_investment_ESS()/25 * (1 + self.discount_rate) ** (-t)
            self.Cost_operation_Generation1 =  365 * self.Cost_operation_Generation() * (1 + self.discount_rate) ** (-t)
            self.Cost_operation_ESS1 = 365 * self.Cost_operation_ESS * (1 + self.discount_rate) ** (-t)
            self.Total_PV1 = 365 * self.Total_PV * (1 + self.discount_rate) ** (-t)
            self.Total_WT1 = 365 * self.Total_WT * (1 + self.discount_rate) ** (-t)
            self.Total_TPS1 = 365 * self.Total_TPS * (1 + self.discount_rate) ** (-t)
            self.Total_CSP1 = 365 * self.Total_CSP * (1 + self.discount_rate) ** (-t)
            self.Total_P2rk1 = 365 * self.Total_P2rk * (1 + self.discount_rate) ** (-t)
            self.Total_El_load1 = 365 * self.Total_El_load * (1 + self.discount_rate) ** (-t)
            LCOE_numinator += (self.Cost_investment_Generation1 + self.Cost_investment_ESS1 + self.Cost_operation_Generation1+ self.Cost_operation_ESS1)
            LCOE_denominator += (self.Total_P2rk1 + self.Total_PV1 + self.Total_WT1 + self.Total_TPS1 + self.Total_CSP1) 
            # LCOE_denominator += self.Total_El_load1 
        if LCOE_denominator != 0:
            self.metrics['LCOE'] = LCOE_numinator / LCOE_denominator
        else:
            self.metrics['LCOE'] = None
            print('Division by zero in LCOE calculation')
            # logging.error('Division by zero in LCOE calculation')
    def Capex (self):
        Capex = (self.Cost_investment_Generation() + self.Cost_investment_ESS())
        self.metrics['Capex'] = Capex
    def Annual_Opex (self):
        Opex = (self.Cost_operation_Generation() + self.Cost_operation_ESS)*365
        self.metrics['Annual_Opex'] = Opex
    def Opex_Per_kWh (self):
        Opex = (self.Cost_operation_Generation() + self.Cost_operation_ESS)/(self.Total_El_load)
        self.metrics['Opex_Per_kWh'] = Opex
    def Co2_emission (self):
        Baseline_Co2_emission = (self.CI_el * self.Total_El_load + self.CI_th * self.Total_Th_load)
        Co2_emission = ((self.CI_el * sum(self.P_import) + self.CI_th * sum(self.Pt_import))-Baseline_Co2_emission)/Baseline_Co2_emission
        self.metrics['Co2_emission'] = Co2_emission
    def calculate(self):
        return self.metrics