# main.py
from Flexibility import FF_Pdelta, FF_Pcons, FF_PC_Pcons, FF_PC_Pdelta, FF_VS_Pdelta, FF_VS_Pcons
FF_PC_ref=0.7

def main():
    FF_Pdelta()
    FF_Pcons()
    FF_PC_Pcons()
    FF_PC_Pdelta()
    FF_VS_Pdelta(FF_PC_ref, FF_PC_Pdelta())
    FF_VS_Pcons(FF_PC_ref, FF_PC_Pcons())
    


if __name__ == "__main__":
    main()
