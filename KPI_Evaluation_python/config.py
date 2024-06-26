# config.py
import random
import numpy as np


random.seed(0)


Price_market = np.array([round(random.uniform(-20,20), 2) for _ in range(24)]);
Price_tarrif = np.array([round(random.uniform(0,20), 2) for _ in range(24)]);


P_el_in = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)]);
P_el_out = np.array([round(random.uniform(1000,1500), 2) for _ in range(24)]);
P_cons = np.array([round(random.uniform(1000, 1500), 2) for _ in range(24)]);
P_ESS = np.array([round(random.uniform(-500,500), 2) for _ in range(24)]);

P_delta= P_el_in - P_el_out
