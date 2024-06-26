# formulation.py
from config import Price_market, Price_tarrif, P_el_in, P_el_out, P_cons, P_ESS, P_delta
import random
import numpy as np

# Price_market: negative to positive
sorted_indices = np.argsort(Price_market)
sorted_Price_market = Price_market[sorted_indices]
sorted_P_el_in = P_el_in[sorted_indices]
sorted_P_el_out = P_el_out[sorted_indices]
sorted_P_delta = P_delta[sorted_indices]

# Price_tarrif: positive
sorted_indices1 = np.argsort(Price_tarrif)
sorted_Price_tarrif = Price_tarrif [sorted_indices1]
sorted_P_cons = P_cons[sorted_indices1]
sorted_P_ESS = P_ESS[sorted_indices1]


# Print the sorted vectors

# print("Sorted Price:", sorted_Price_market)
# print("Sorted indices:", sorted_indices)
# print("Sorted P_el_in:", sorted_P_el_in)
# print("Sorted P_el_out:", sorted_P_el_out)
# print("Sorted P_cons:", sorted_P_cons)
# print("Sorted P_ESS:", sorted_P_ESS)
# print("Sorted Price_retailors:", sorted_Price_tarrif)



def FF_Pdelta():
    # Price: negative to positive,  P_delta= P_el_in-P_el_out
    FF_Pdelta= (sum(sorted_Price_market[:12]*sorted_P_delta[:12])-sum(sorted_Price_market[12:]*sorted_P_delta[12:]))/(sum(sorted_Price_market[:12]*sorted_P_delta[:12])+sum(sorted_Price_market[12:]*sorted_P_delta[12:]))
    print('FF_Pdelta',FF_Pdelta)

def FF_Pcons():
    # Price: positive
    FF_Pcons= (sum(sorted_Price_tarrif[:12]*sorted_P_cons[:12])-sum(sorted_Price_tarrif[12:]*sorted_P_cons[12:]))/(sum(sorted_Price_tarrif[:12]*sorted_P_cons[:12])+sum(sorted_Price_tarrif[12:]*sorted_P_cons[12:]))
    print('FF_Pcons',FF_Pcons)

def FF_PC_Pcons():
    # Price: positive
    FF_PC_Pcons= ((sum(sorted_Price_tarrif[23]*sorted_P_cons)-sum(sorted_Price_tarrif*sorted_P_cons))/(sum(sorted_Price_tarrif[23]*sorted_P_cons)-sum(sorted_Price_tarrif[0]*sorted_P_cons)))
    print( 'FF_PC_Pcons:',FF_PC_Pcons)
    return FF_PC_Pcons

def FF_PC_Pdelta():
    # Price: positive
    FF_PC_Pdelta= ((sum(sorted_Price_market[23]*sorted_P_delta)-sum(sorted_Price_market*sorted_P_delta))/(sum(sorted_Price_market[23]*sorted_P_delta)-sum(sorted_Price_market[0]*sorted_P_delta)))
    print( 'FF_PC_Pdelta:',FF_PC_Pdelta)
    return FF_PC_Pdelta

def FF_VS_Pdelta(FF_PC_ref, FF_PC_Pdelta):
    FF_VS_Pdelta= (FF_PC_Pdelta- FF_PC_ref)/FF_PC_Pdelta
    print('FF_VS_Pdelta:', FF_VS_Pdelta)

def FF_VS_Pcons(FF_PC_ref, FF_PC_Pcons):
    FF_VS_Pcons= (FF_PC_Pcons- FF_PC_ref)/FF_PC_Pcons
    print('FF_VS_Pcons:', FF_VS_Pcons)