import numpy as np
from scipy.signal import remez,freqz
import matplotlib.pyplot as plt

class FIRFilter:
    def __init__(self, order:int,bands,desired,weights=None):

        """
        Parameters: Order: Order of the desired filter
                    Bands: List of band edges in the form (band1_start,band1_stop,band2_start,band2_stop, ...)
                    Desired: desired gain for each band: this should be half the size of bands
                    Weights: The weight represent how important is the band relative to the others.   
                             Usually, zero-gain bands are given higher weights to obtain the maximum possible attenuation.
        """

        self.order = order

        self.order = int(self.order)
        if self.order < 1:
            raise ValueError("Order must be >= 1")

        if self.order % 2 == 0:    # make odd (Type 1)
            self.order = self.order + 1

        self.bands = bands
        self.desired = desired
        if len(self.bands) != 2*len(self.desired):
            raise ValueError("Desired must be half the length of Bands array")
        self.weights = weights
        self.min = np.min(self.bands)
        self.range = np.max(self.bands)- np.min(self.bands)
        
        # Flag to check if coefficients have been computed
        self.computedCoeffs = False
        self.coeffs = None

    def Normalise(self,Bands):
        Band =[]
        for band in Bands:
            norm = ((band - self.min ) / (self.range)) *0.5
            Band.append(norm)
        Bands = Band
        return Bands
    
    def design_fir_filter(self, plot=False):
        """
        Function to design an FIR filter using Parks-McClellan algorithm (Remez method) based on user input.
        Returns:
            FIR filter coefficients.
        """
        if self.computedCoeffs:
            return self.coeffs

        self.bands = np.asarray(self.Normalise(self.bands)).flatten()
        self.desired = np.asarray(self.desired).flatten()
        
        if self.weights is not None:
            self.weights = np.asarray(self.weights).flatten()
   
        # Use scipy.signal.remez to design the filter
        coeffs = remez(numtaps=self.order, bands=self.bands, desired=self.desired, weight=self.weights,fs=1, grid_density=128)
        
        if plot:
            w, h = freqz(coeffs, [1], worN=2000, fs=1)
            w= 2*w*self.range + self.min
            self.plot_response(w, h, "Plot of FIR Transfer Function")
        
        return coeffs

    def plot_response(self,w, h, title): 
        "Utility function to plot response functions"
        fig, ax = plt.subplots()
        ax.plot(w, 20 * np.log10(np.abs(h)))
        ax.set_ylim(-40, 5)
        ax.grid(True)
        ax.set(xlabel='Frequency (Hz)', ylabel='Gain (dB)', title=title)
        plt.show()

    def SaveCoeffs(self, path):
        "Utility function to save coeffcients as csv file"
        if not self.computedCoeffs:
            self.Impulse()
        fileName = f"{path}/coefficients.csv"
        np.savetxt(fileName, self.coeffs, delimiter=',')


if __name__ == "__main__":
    Length = 50
    band_edges = [0, 500, 505, 720]
    desired_gain = [1, 0]
    Filter = FIRFilter(Length, band_edges, desired_gain)
    Filter.design_fir_filter(plot=True)
