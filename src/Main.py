import Algorithim.Design_Filter as df
import Algorithim.FIR_Algorithim as fir
#import Lumerical.Build_Lattice_Filter as Lum
import numpy as np
import json
import os


"CONSTANTS"
C = 299792458

# def UserInput(filename):
#     """
#     Function to receive the necessary parameters from an input file in JSON format to design the filter

#     Parameters:
#     - filename: Name of input file

#     Return:
#     - params: Dictionary containing filter parameters
#     """
#     try:
#         # Open the file and load the JSON data
#         with open(filename, "r") as file:
#             data = json.load(file)

#         # Define default values and types for each key
#         defaults = {
#             "Optical paramters":{
#             "n_g": 0.0,                 # Group refractive index
#             "FSR": 0.0,                 # Free Spectral Range
#             },

#             "Initialise Digital filter":{
#             "filter_order": 7,          # Max order of the FIR filter 
#             "filter_type": "Bandpass",  # "Lowpass","Highpass","Bandpass", "Bandstop"
#             "t_width":40,               # Transition width between stop and pass band Hz
#             "endpoints": [187,200],     # The frequency range of interest
            
#             },

#             "Frequency parameters":{
#             "center_frequencies": [100.0],   # list of center frequncies for bamds
#             "band_width": 100.0,          # Band width of the bands
#             "cutoff_frequncy": None,    # cutoff frequncy for high and lowpass filters
#             }
#         }

#         """params ={}
#         # Iterate through function defaults and update params
#         for function_name, default_params in defaults.items():
#             params[function_name] = {}
#             for key, default_value in default_params.items():
#                 params[function_name][key] = data[function_name].get(key, default_value)"""

#         return defaults


#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON in the input file: {e}")
#         exit()

#     except FileNotFoundError:
#         print(f"Error! File {filename} not found.")
#         exit()

def FindOpticalParameters():

    params = {
            
            "Initialise Digital filter":{
            "filter_order": 15,         # Max order of the FIR filter/ number of couplers optical filter
            "filter_type": "Bandpass",  # "Lowpass","Highpass","Bandpass", "Bandstop"
            "t_width":5.0,                # Transition width between stop and pass band (THz)
            "center_frequency": 193.5,  # Center Frequency for range (THz)  
            "range": 50,                # The frequency range of interest (THz)
            },

            "Frequency parameters":{
            "band_centers": [193.5],  # list of center frequncies for bands(THz)
            "band_width": 15,          # Band width of the bands (THz)
            "cutoff_frequency": None,  # cutoff frequncy for high and lowpass filters
            }
        }

    
    filter = params.get("Initialise Digital filter", {})
    frequency= params.get("Frequency parameters", {})
    
    #Design Fir filter using park McClellan method for parameters above implemented in Design_filter.py
    filter_instance = df.FIRFilter(order = filter.get("filter_order"), filter_type = filter.get("filter_type"), t_width = filter.get("t_width"), center = filter.get("center_frequency"), range = filter.get("range"))
    A = filter_instance.design_fir_filter(band_center = frequency.get("band_centers"), band_width = frequency.get("band_width") , cutoff_frequency= frequency.get("cutoff_frequency"), plot=True)
  
    #Find the correct optical parameters for the found transfer fuction A implemented in FIR_Algorithim.py
    kappa,phi,theta = fir.FindCoefficents(A=A)
    
    return kappa, phi,theta

if __name__ == "__main__":
    kappa, phi,theta = FindOpticalParameters()
    print(kappa,phi)
