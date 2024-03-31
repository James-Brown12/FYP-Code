import numpy as np
from scipy.signal import remez,freqz
import matplotlib.pyplot as plt

class FIRFilter:
    def __init__(self, order:int,bands,desired,weights=None):

        """
        Parameters: Order: Order of the desired filter
                    Bands: Transition width between pass and stopband Note: t_width ~ 1/order
                    Desired: endpoints of Frequency of interest.
                    Weights: 
        """

        self.order = order

        self.order = int(self.order)
        if self.order < 1:
            raise ValueError("Order must be >= 1")

        if self.order % 2 == 0:    # make odd (Type 1)
            self.order = self.order + 1

        self.bands = bands
        self.desired = desired
        self.weights = weights
        self.fs = 2*np.max(bands)
        
        # Flag to check if coefficients have been computed
        self.computedCoeffs = False
        self.coeffs = None

    def design_fir_filter(self, plot=False):
        """
        Function to design an FIR filter using Parks-McClellan algorithm (Remez method) based on user input.

        Parameters:
            center_freq: Center frequency or array of center frequencies.
            band_width: Desired width of pass (or stop) band, in Hz.
            cutoff_frequency: Cutoff frequency for high and low pass filter.
            plot: Boolean indicating whether to plot the frequency response.

        Returns:
            FIR filter coefficients.
        """
        if self.computedCoeffs:
            return self.coeffs

        self.bands = np.asarray(self.bands).flatten()
        
        self.desired = np.asarray(self.desired).flatten()
        
        if self.weights is None:
            self.weights = np.ones(len(self.desired))
        self.weights = np.asarray(self.weights).flatten()

        # Use scipy.signal.remez to design the filter
        coeffs = remez(numtaps=self.order, bands=self.bands, desired=self.desired, weight=self.weights,fs=self.fs)
        
        if plot:
            w, h = freqz(coeffs, [1], worN=2000, fs=1)
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
        if not self.computedCoeffs:
            self.Impulse()
        fileName = f"{path}/coefficients.csv"
        np.savetxt(fileName, self.coeffs, delimiter=',')


if __name__ == "__main__":
    Fs = 1440
    Length = 50
    band_edges = [0, 500, 505, 720]
    desired_gain = [1, 0]
    Filter = FIRFilter(Length, band_edges, desired_gain)
    Filter.design_fir_filter(plot=True)
