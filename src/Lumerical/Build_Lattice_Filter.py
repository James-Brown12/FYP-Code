import importlib.util
#default path for current release 
spec_win = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py')
#Functions that perform the actual loading
lumapi = importlib.util.module_from_spec(spec_win) #windows
spec_win.loader.exec_module(lumapi)



def Build_Lattice(phis, kappas):

     # Start the INTERCONNECT session
    with lumapi.INTERCONNECT(hide=True) as interconnect:
        

        # Add resonators to the lattice filter based on kappas
        for kappa in kappas:
            interconnect.addelement("Waveguide Coupler")
            eleName = f"coupler_{kappa}"
            interconnect.set("name", eleName)
            interconnect.set("coupling coefficient 1", kappa)
    
        # Save the INTERCONNECT layout (optional)
        interconnect.save("Lattice_Filter.icp")
    


    

if __name__ == "__main__":
    # Example usage
    phi_values = [0.5,0.3]  # Replace with your desired value for phi
    kappas_values = [0.1, 0.2, 0.3]  # Replace with your desired values for kappas

    Build_Lattice(phi_values, kappas_values)
