# main.py
from MetricCalculator import MetricCalculator
from Formulation import Flexibility

def main():
    metric_calculator = MetricCalculator()
    data, metric = metric_calculator.calculate()

    flexibility = Flexibility(data)
    flexibility.FF_Pcons()
    FF_PC_Pcons = flexibility.FF_PC_Pcons()
    FF_PC_Pdelta = flexibility.FF_PC_Pdelta()
    
    FF_PC_ref = 7.0
    
    flexibility.FF_VS_Pdelta(FF_PC_ref, FF_PC_Pdelta)
    flexibility.FF_VS_Pcons(FF_PC_ref, FF_PC_Pcons)

    metrics = flexibility.calculate()
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
