import Algorithim.Design_Filter as df
import Algorithim.FIR_Algorithim as fir
#import Lumerical.Build_Lattice_Filter as Lum
import numpy as np


######################## USER PARAMTERS ########################################
Order = 20
band_edges = [1400, 1500,1510,1590,1600,1700] #The start a sndtop wavelengths for band must occur in pairs, the central freuqncy and FSR are taken from this also.
desired_gain = [0,1, 0] # The gain in each band given in Desired_bands
#Find Length
n_g = 4.40063 #group index
###################################################################################

def FindOpticalParameters():

    Filter = df.FIRFilter(Order, band_edges, desired_gain)
    A = Filter.design_fir_filter(plot=True)
    #Find the correct optical parameters for the found transfer fuction A implemented in FIR_Algorithim.py
    kappa,phi = fir.FindCoefficents(A=A)
    center_frequncy = (np.max(band_edges) + np.min(band_edges)) / 2
    range = np.max(band_edges) - np.min(band_edges)
    DeltaL = ((center_frequncy)**2 /(n_g*range) ) *1E-3 # Delta L in microns

    return DeltaL,kappa

if __name__ == "__main__":
    DeltaL, kappa = FindOpticalParameters()
    print(DeltaL,kappa)

