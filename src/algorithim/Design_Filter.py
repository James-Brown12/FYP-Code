import numpy as np
from scipy.signal import remez,freqz
import matplotlib.pyplot as plt

class FIRFilter:
    def __init__(self, order, t_width, filter_type,endpoints):

        """
        Function to obtain the bands(pass or stop), in units of normalized frequency, from
        the center Frequencies (in nm)
    
        Parameters: order: Order of the desired filter
                    t_width: Transition width between pass and stopband Note: t_width ~ 1/order
                    endpoints: endpoints of Frequency of interest.
                    filter_type: string that indicates type of filter: ["Bandpass" ,"BandStop","Lowpass","Highpass"]
                                    
        Return: List of tuples representing band (normalized) frequency intervals
        """
        self.order = order
        self.t_width = t_width
        self.filter_type = filter_type
        self.fstart, self.fend = endpoints[0], endpoints[1]

    def normalized_frequency(self, f):
        return (f - self.fstart) / (2 * (self.fend - self.fstart))

    def obtain_bands(self, center_frequencies, band_width,cutoff_frequency=None):
        """
        Function to obtain the bands(pass or stop), in units of normalized frequency, from
        the center Frequencies (in nm)
    
        Parameters: center_frequencies: ndarray of center Frequencies, lowest frequency is in position 0 of array
                    band_width: desired width of pass (or stop) band, in Hz
                    endpoints: endpoints of Frequency of interest.
                    filter_type: string that indicates type of filter: ["Bandpass" ,"BandStop","Lowpass","Highpass"]
                                    
        Return: List of tuples representing band (normalized) frequency intervals
        """
        
        bands = []

        if self.filter_type == "Lowpass":
            bands.append((0.0, self.normalized_frequency(cutoff_frequency), 1.0))
        elif self.filter_type == "Highpass":
            bands.append((self.normalized_frequency(cutoff_frequency), 0.5, 1.0))
        else:
            for frequency in center_frequencies:
                f_low, f_up = frequency - band_width / 2.0, frequency + band_width / 2.0
                bands.append((self.normalized_frequency(f_low), self.normalized_frequency(f_up), 1.0 if self.filter_type == "Bandpass" else 0.0))
                
        return bands

    def fir_filter_parks_mcclellan(self, bands):
        freq, gain = [], []

        for band in bands:
            start_freq, end_freq, band_gain = band
            t_width = self.normalized_frequency(self.t_width)

            freq.extend(filter(lambda x: 0.0 < x < 0.5, [start_freq - t_width, start_freq, end_freq, end_freq + t_width]))
            gain.extend([band_gain])
            if self.filter_type !="Highpass":
                gain.extend([0.0 if self.filter_type in {"Bandpass", "Lowpass"} else 1.0])


        freq = [0.0] + freq + [0.5]
        if self.filter_type !="Lowpass":
            gain = [0.0 if self.filter_type in {"Bandpass", "Highpass"} else 1.0] + gain

        print(freq,gain)
        coefs = remez(numtaps=self.order + 1, bands=freq, desired=gain)
        return coefs



def plot_response(w, h, title):
    "Utility function to plot response functions"
    fig, ax = plt.subplots()
    ax.plot(w, 20 * np.log10(np.abs(h)))
    ax.set_ylim(-40, 5)
    ax.grid(True)
    ax.set(xlabel='Frequency (Hz)', ylabel='Gain (dB)', title=title)
    plt.show()

def example_usage():
    filter_instance = FIRFilter(order=100, t_width=10, filter_type='Bandstop',endpoints = (0, 500))
    center_frequencies = np.array([100, 300])   
    band_width = 100
    cutoff_frequency=100

    bands = filter_instance.obtain_bands(center_frequencies, band_width,cutoff_frequency)
    coefs= filter_instance.fir_filter_parks_mcclellan(bands)
    
    # Plot the frequency response
    w, h = freqz(coefs, [1], worN=2000,fs=1)
    plot_response(w,h,"multiband")
   
if __name__ == "__main__":
    example_usage()
