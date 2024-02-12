
#import lumapi
import importlib.util
spec_win = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py')
lumapi = importlib.util.module_from_spec(spec_win) #windows
spec_win.loader.exec_module(lumapi)

import numpy as np
import os

class LatticeBuilder:
    def __init__(self, f0, ng, deltal,c):
        """
        Initialize the LatticeBuilder.

        Parameters:
        - f0: Central frequency.
        - ng: Group index.
        - deltal: Unit delay of the waveguide.
        - c: speed of light
        """
        self.f0 = f0
        self.ng = ng
        self.deltal = deltal
        self.c = c
        self.interconnect = None  # Will be initialized during lattice building

    def neff(self, phi):
        """
        Calculate the effective index of the waveguide.

        Parameters:
        - phi: Phase value.

        Returns:
        - Effective index of the waveguide.
        """
        return (phi * self.c) / (2 * np.pi * self.f0 * self.deltal) + self.ng

    def set_couplers(self, kappa_values):
        """
        Add couplers to the lattice filter based on kappa values.

        Parameters:
        - kappa_values: Array of kappa values for couplers.
        """
        for i, kappa in enumerate(kappa_values):
            self.interconnect.addelement("Waveguide Coupler")
            ele_name = f"C_{i}"
            self.interconnect.set("name", ele_name)
            self.interconnect.set("x position", i * 500)
            self.interconnect.set("Coupling Coefficient 1", np.sin(kappa * np.pi) ** 2)

    def set_waveguides(self, phi_values):
        """
        Add waveguides to the lattice filter.

        Parameters:
        - phi_values: Array of phase values for waveguides.
        """
        for i, phi in enumerate(phi_values):
            self.interconnect.addelement("Straight Waveguide")
            ele_name = f"WG_{i}"
            self.interconnect.set("name", ele_name)
            self.interconnect.set("x position", 250 + i * 500)
            self.interconnect.set("y position", -250)

            # Set unit delay of waveguide and twice that for the last one
            self.interconnect.set("length", 2 * self.deltal) if i + 1 != len(phi_values) else self.interconnect.set("length", self.deltal)

            # Set other properties of waveguide based on specs
            self.interconnect.set("frequency", self.f0)
            self.interconnect.set("group index 1", self.ng)
            self.interconnect.set("effective index 1", self.neff(phi))

    def set_analyzer(self):
        """
        Add Optical Analyser to the lattice filter.

        Parameters:
        - phi_values: Array of phase values for waveguides.
        """
        self.interconnect.addelement("Optical Network Analyzer")
        ele_name = "OPA"
        self.interconnect.set("name", ele_name)
        self.interconnect.set("y position", 250)
        self.interconnect.set("number of input ports", 2)

    def connect(self, kappa_values,phi_values):
        """
        Connect the placed couplers and waveguides correctly in a lattice configuration.

        Parameters:
        - kappa_values: Array of kappa values for couplers.
        - phi_values: Array of phase values for waveguides.
        """
        for i, kappa in enumerate(kappa_values):
            if i+1 < len(kappa_values):
                self.interconnect.connect(f"C_{i}","port 4",f"C_{i+1}","port 2")
        for i, phi in enumerate(phi_values):
            self.interconnect.connect(f"WG_{i}","port 1",f"C_{i}","port 3")
            self.interconnect.connect(f"WG_{i}","port 2",f"C_{i+1}","port 1")

        self.interconnect.connect("OPA","output","C_0","port 1")
        self.interconnect.connect("OPA","input 1",f"C_{len(kappa_values)-1}","port 3") #through port values
        self.interconnect.connect("OPA","input 2",f"C_{len(kappa_values)-1}","port 4") #cross port values

    def build_lattice(self, phi_values, kappa_values):
        """
        Build the lattice filter in INTERCONNECT and save as .icp file.

        Parameters:
        - phi_values: Array of phase values for waveguides.
        - kappa_values: Array of kappa values for couplers.
        """
        

        #define where to savefile
        script_directory = os.path.dirname(__file__)
        file_path = os.path.join(script_directory, "Lattice_Filter.icp")

        # Start the INTERCONNECT session
        with lumapi.INTERCONNECT(hide=True) as self.interconnect:
            self.set_couplers(kappa_values)
            self.set_waveguides(phi_values)
            self.set_analyzer()
            self.connect(kappa_values,phi_values)

            # Save the INTERCONNECT layout
            self.interconnect.save(file_path)

if __name__ == "__main__":
    # Example Specs
    F0 = 193.1e12
    NG = 8.05894
    FSR = 120e9
    c = 299792458
    DELTAL = c / FSR / NG
    # Example usage
    phi_values = [np.pi*1.0, 0.0, np.pi*1.0, 0.0]  # Replace with your desired value for phi
    kappa_values = [0.3498, 0.2448, 0.4186, 0.0797, 0.25]  # Replace with your desired values for kappas

    builder = LatticeBuilder(F0, NG, DELTAL,c)
    builder.build_lattice(phi_values, kappa_values)

