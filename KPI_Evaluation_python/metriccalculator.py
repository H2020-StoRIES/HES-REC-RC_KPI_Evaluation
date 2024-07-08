import random
import numpy as np

random.seed(1)

class MetricCalculator():
    def __init__(self):
        self.Price_market = np.array([round(random.uniform(-20, 20), 2) for _ in range(24)])
        self.Price_tarrif = np.array([round(random.uniform(0, 20), 2) for _ in range(24)])
        self.P_el_in = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_el_out = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_cons = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_ESS = np.array([round(random.uniform(-500, 500), 2) for _ in range(24)])
        self.P_delta = self.P_el_in - self.P_el_out
        self.P_el_in_base = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_el_out_base = np.array([round(random.uniform(1000,1500), 2) for _ in range(24)])
        self.P_delta_base = self.P_el_in_base - self.P_el_out_base
        self.data = {}

    def calculate(self):
        self.data['Price_market'] = self.Price_market
        self.data['Price_tarrif'] = self.Price_tarrif
        self.data['P_el_in'] = self.P_el_in
        self.data['P_el_out'] = self.P_el_out
        self.data['P_cons'] = self.P_cons
        self.data['P_ESS'] = self.P_ESS
        self.data['P_delta'] = self.P_delta
        self.data['P_el_in_base'] = self.P_el_in_base
        self.data['P_el_out_base'] = self.P_el_out_base
        self.data['P_delta_base'] = self.P_delta_base
        return self.data

metric_calculator = MetricCalculator()

# Call the calculate method
data = metric_calculator.calculate()

