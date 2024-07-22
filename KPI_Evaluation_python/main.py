from MetricCalculator import MetricCalculator
from Formulation import Flexibility
from config import Config
import logging
from logging_util import setup_logging
setup_logging()
logging.info("Congiguration: \n T: %s, median: %s, FF_PC_ref: %s", Config.T, Config.median, Config.FF_PC_ref)

def main():
    logging.info("Starting the metric calculation process")
    metric_calculator = MetricCalculator()
    data = metric_calculator.calculate()

    flexibility = Flexibility(data)
    FF_Pcons = flexibility.FF_Pcons()
    FF_PC_Pcons = flexibility.FF_PC_Pcons()
    FF_PC_Pdelta = flexibility.FF_PC_Pdelta()
    
    FF_PC_ref = Config.get_config().FF_PC_ref
    
    flexibility.FF_VS_Pdelta(FF_PC_ref, FF_PC_Pdelta)
    flexibility.FF_VS_Pcons(FF_PC_ref, FF_PC_Pcons)
    FF= flexibility.FF()
    flexibility.FF_W()
    FF_base= flexibility.FF_base()
    flexibility.FF_shift(FF, FF_base)
    flexibility.FF_SB()
    

    metrics = flexibility.calculate()
    logging.info("Metrics: %s", metrics)
    print(metrics)

if __name__ == "__main__":
    main()
