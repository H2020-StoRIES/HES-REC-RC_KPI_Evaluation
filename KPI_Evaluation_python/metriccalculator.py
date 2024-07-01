import random
import numpy as np

random.seed(0)

class MetricCalculator():
    def __init__(self):
        self.Price_market = np.array([round(random.uniform(-20, 20), 2) for _ in range(24)])
        self.Price_tarrif = np.array([round(random.uniform(0, 20), 2) for _ in range(24)])
        self.P_el_in = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_el_out = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_cons = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)])
        self.P_ESS = np.array([round(random.uniform(-500, 500), 2) for _ in range(24)])
        self.P_delta = self.P_el_in - self.P_el_out
        self.data = {}
        self.Metric = {}

    def calculate(self):
        self.data['Price_market'] = self.Price_market
        self.data['Price_tarrif'] = self.Price_tarrif
        self.data['P_el_in'] = self.P_el_in
        self.data['P_el_out'] = self.P_el_out
        self.data['P_cons'] = self.P_cons
        self.data['P_ESS'] = self.P_ESS
        self.data['P_delta'] = self.P_delta

        # Example metric calculations
        self.Metric['Average_Price_market'] = np.mean(self.Price_market)
        self.Metric['Average_Price_tarrif'] = np.mean(self.Price_tarrif)
        self.Metric['Total_P_el_in'] = np.sum(self.P_el_in)
        self.Metric['Total_P_el_out'] = np.sum(self.P_el_out)
        self.Metric['Total_P_cons'] = np.sum(self.P_cons)
        self.Metric['Total_P_ESS'] = np.sum(self.P_ESS)
        self.Metric['Total_P_delta'] = np.sum(self.P_delta)

        return self.data, self.Metric

metric_calculator = MetricCalculator()

# Call the calculate method
data, metric = metric_calculator.calculate()

