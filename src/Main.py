import Algorithim.Design_Filter as df
import Algorithim.FIR_Algorithim as fir
#import Lumerical.Build_Lattice_Filter as Lum
import numpy as np


######################## USER PARAMTERS ########################################
Order = 15
band_edges = [0, 0.1,0.15,0.35,0.4,0.5] #Normailsed between [0-0.5] must occur in pairs
desired_gain = [0,1, 0]
n_g= 8.05894 #group index
center_frequncy = 1550
FSR = 20
# Note code will take the range of Band_enges as FSR and Median as the central wavelength
#################################################################################

def FindOpticalParameters():
    Filter = df.FIRFilter(Order, band_edges, desired_gain)
    A = Filter.design_fir_filter(plot=True)
    #Find the correct optical parameters for the found transfer fuction A implemented in FIR_Algorithim.py
    kappa,phi = fir.FindCoefficents(A=A)

    DeltaL = (np.median(band_edges)**2 / n_g*np.ptp(band_edges)) * 1E-9 #put into meters
    return DeltaL,kappa, phi

if __name__ == "__main__":
    DeltaL, kappa, phi = FindOpticalParameters()
    print(DeltaL,kappa,phi)
