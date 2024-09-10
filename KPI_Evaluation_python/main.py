from metriccalculator import MetricCalculator
from Formulation import Flexibility, efficiency
from config import Config
import logging
from logging_util import setup_logging
setup_logging()
logging.info("Congiguration: \n T: %s, median: %s, FF_PC_ref: %s", Config.T, Config.median, Config.FF_PC_ref)

def main():
    logging.info("Starting the metric calculation process")
    metric_calculator = MetricCalculator()
    data_flex, data_eff = metric_calculator.calculate()
    # data_flex= data.data_flex
    flexibility = Flexibility(data_flex)
    flexibility.FF()
    flexibility.FF_base()
    flexibility.FF_W()
    flexibility.FF_SB()
    flexibility.FF_shift()
    metrics = flexibility.calculate()
    logging.info("Metrics: %s", metrics)
    print(metrics)
    Efficiency = efficiency(data_eff)
    Efficiency.Eff()
    metrics = Efficiency.calculate()
    logging.info("Metrics: %s", metrics)
if __name__ == "__main__":
    main()
