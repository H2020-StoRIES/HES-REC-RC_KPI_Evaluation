clc
clear
folderPath = 'C:\Users\szata\OneDrive - Danmarks Tekniske Universitet\Dokumenter\StoRIES\Code\t32-ref-case-dev';
addpath(folderPath);
A= open('dataIn_CEDER.mat');
B= open('dataIn_CEDER_preDesign.mat');

Price_elec= A.elePrizes_spain;
Data= A.cederPDgc.date;
Gen_total= A.cederPDgc.P_g_tot;
Load_total= A.cederPDgc.P_c_tot;
BT_data= B.PessTT_BT;
SC_data= B.PessTT_SC;
HP_data= B.PessTT_HP;
