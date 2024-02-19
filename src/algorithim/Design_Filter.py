import numpy as np
from scipy.signal import remez,freqz
import matplotlib.pyplot as plt

class FIRFilter:
    def __init__(self, order, t_width, filter_type,endpoints):
        self.order = order
        self.t_width = t_width
        self.filter_type = filter_type
        self.fstart, self.fend = endpoints[0], endpoints[1]

    def normalized_frequency(self, f):
        return (f - self.fstart) / (2 * (self.fend - self.fstart))

    def obtain_bands(self, center_frequencies, band_width):
        """
        Function to obtain the bands(pass or stop), in units of normalized frequency, from
        the center Frequencies (in nm)
    
        Parameters: center_frequencies: ndarray of center Frequencies, longest Frequency/
                                    lowest frequency is in position 0 of array
                    band_width: desired width of pass (or stop) band, in nm
                        endpoints: endpoints of Frequency of interest.
                            typef: string that indicates type of filter, this parameter is
                                    either "Pass" or "Stop"
                                    
        Return: List of tuples representing band (normalized) frequency intervals
        """
        bands = []
        for frequency in center_frequencies:
            f_low = frequency - band_width/2.0
            f_up = frequency + band_width/2.0
            omega_lower = self.normalized_frequency(f_low)
            omega_upper = self.normalized_frequency(f_up)
            if self.filter_type == "Pass":
                bands.append((omega_lower, omega_upper, 1.0))
            else:
                bands.append((omega_lower, omega_upper, 0.0))
        return bands

    def fir_filter_parks_mcclellan(self, bands):
        freq = []  # Frequency points
        gain = []  # Gain of filter for bands in freq, size of this list should be exactly half the size of freq

        # Build lists freq and gain
        for band in bands:
            start_freq, end_freq, band_gain = band
            t_width = self.normalized_frequency(self.t_width)

            # Insert point just before the start frequency
            if start_freq - t_width > 0.0:
                freq.extend([start_freq - t_width])
                
            # Add points for the passband
            freq.extend([start_freq, end_freq])
            gain.extend([band_gain])

            # Insert point just after the end frequency with gain 0.0 or 1.0 based on filter type
            if end_freq + t_width < 0.5:
                freq.extend([end_freq + t_width])
                gain.extend([0.0] if self.filter_type == 'Pass' else [1.0])

        # Ensure that 0.0 and 0.5 are in the frequency list
        if 0.0 not in freq:
            freq.insert(0, 0.0)
            #ensures gain element for between zero and first band frequency
            gain.insert(0,0.0 if self.filter_type == 'Pass' else 1.0)

        if 0.5 not in freq:
            freq.extend([0.5])

        # Design the filter
        coefs = remez( numtaps = self.order + 1, bands=freq, desired=gain)
        
        return coefs



def plot_response(w, h, title):
    "Utility function to plot response functions"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(w, 20*np.log10(np.abs(h)))
    ax.set_ylim(-40, 5)
    ax.grid(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.set_title(title)
    plt.show()

def example_usage():
    filter_instance = FIRFilter(order=100, t_width=10, filter_type='Pass',endpoints = (0, 500))
    center_frequencies = np.array([100, 300])   
    band_width = 100

    bands = filter_instance.obtain_bands(center_frequencies, band_width)
    coefs= filter_instance.fir_filter_parks_mcclellan(bands)
    
    # Plot the frequency response
    w, h = freqz(coefs, [1], worN=2000,fs=1)
    plot_response(w,h,"multiband")
   
if __name__ == "__main__":
    example_usage()
