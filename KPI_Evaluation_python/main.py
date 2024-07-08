from MetricCalculator import MetricCalculator
from Formulation import Flexibility

def main():
    metric_calculator = MetricCalculator()
    data = metric_calculator.calculate()

    flexibility = Flexibility(data)
    FF_Pcons = flexibility.FF_Pcons()
    FF_PC_Pcons = flexibility.FF_PC_Pcons()
    FF_PC_Pdelta = flexibility.FF_PC_Pdelta()
    
    FF_PC_ref = 7.0
    
    flexibility.FF_VS_Pdelta(FF_PC_ref, FF_PC_Pdelta)
    flexibility.FF_VS_Pcons(FF_PC_ref, FF_PC_Pcons)
    FF= flexibility.FF()
    flexibility.FF_W()
    FF_base= flexibility.FF_base()
    flexibility.FF_shift(FF, FF_base)
    flexibility.FF_SB()
    

    metrics = flexibility.calculate()
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
