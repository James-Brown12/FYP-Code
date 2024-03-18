import numpy as np
from scipy.signal import remez,freqz
import matplotlib.pyplot as plt

class FIRFilter:
    def __init__(self, order:int,filter_type:str, t_width:float,center:float, range:float):

        """
        Parameters: order: Order of the desired filter
                    t_width: Transition width between pass and stopband Note: t_width ~ 1/order
                    endpoints: endpoints of Frequency of interest.
                    filter_type: string that indicates type of filter: ["Bandpass" ,"BandStop","Lowpass","Highpass"]
                                    
        Return: List of tuples representing band (normalized) frequency intervals
        """
        self.order = order
        self.t_width = t_width
        self.filter_type = filter_type
        self.center, self.range = center,range

    def normalized_frequency(self, f):
        return (f - (self.center - self.range/2)) / (2*(self.range))

    def design_fir_filter(self, band_center, band_width, cutoff_frequency=None, plot=False):
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
        bands = []
        desired = []
        
        if self.filter_type == "Lowpass" or self.filter_type == "Highpass":
            bands.extend([0.0, self.normalized_frequency(cutoff_frequency - self.t_width),self.normalized_frequency(cutoff_frequency + self.t_width), 0.5])
            if self.filter_type == "Lowpass":
                desired.extend([1.0, 0.0])
            else:
                desired.extend([0.0, 1.0])
        
        else:
            for frequency in band_center:
                f_low, f_up = frequency - band_width / 2.0, frequency + band_width / 2.0
                bands.extend(filter(lambda x: 0.0 < x < 0.5, [self.normalized_frequency(f_low - self.t_width), 
                                                              self.normalized_frequency(f_low), 
                                                              self.normalized_frequency(f_up), 
                                                              self.normalized_frequency(f_up + self.t_width)]))
               
                if self.normalized_frequency(f_up + self.t_width ) > 0.5:
                    desired.append(0.0 if self.filter_type == "Bandpass" else 1.0)

                elif self.normalized_frequency(f_low - self.t_width ) < 0.0:
                    desired.append(0.0 if self.filter_type == "Bandpass" else 1.0)

                else:
                    desired.extend([0.0, 1.0] if self.filter_type == "Bandpass" else [1.0, 0.0])
                
                
                
            bands = [0.0] + bands + [0.5]
            if self.filter_type == "Bandpass":
                    desired.extend([0.0])
            else:
                    desired.extend([1.0])
          
        
        coefs = remez(numtaps=self.order, bands=np.sort(bands), desired=desired)
        
        if plot:
            w, h = freqz(coefs, [1], worN=2000, fs=1)
            plot_response(w, h, "Plot of FIR Transfer Function")
        
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
    for filter_type in ['Bandstop','Bandpass','Highpass','Lowpass']:
        filter_instance = FIRFilter(order=61, t_width=2.5, filter_type=filter_type,center=190, range=50)
        
        
        band_center = np.array([200])   
        band_width = 5
        cutoff_frequency=190

        
        coefs= filter_instance.design_fir_filter(band_center, band_width, cutoff_frequency, plot=False)
        
        # Plot the frequency response
        w, h = freqz(coefs, [1], worN=2000,fs=1)
        plot_response(w,h,f"multiband_{filter_type}")
   
if __name__ == "__main__":
    example_usage()
