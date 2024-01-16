import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, butter, lfilter, filtfilt

def design_filter(filter_type, num_taps_or_order, cutoff_freq):
    if filter_type.lower() == 'fir':
        # Designing an FIR filter
        coefficients = firwin(num_taps_or_order, cutoff_freq, window='hamming')
    elif filter_type.lower() == 'iir':
        # Designing an IIR filter
        coefficients = butter(num_taps_or_order, cutoff_freq, btype='low', analog=False, output='ba')
    else:
        raise ValueError("Invalid filter type. Choose 'fir' or 'iir'.")

    return coefficients

def apply_filter(signal, coefficients, filter_type):
    if filter_type.lower() == 'fir':
        # Apply FIR filter
        filtered_signal = lfilter(coefficients, 1.0, signal)
    elif filter_type.lower() == 'iir':
        # Apply IIR filter using filtfilt to avoid phase distortion
        filtered_signal = filtfilt(coefficients[0], coefficients[1], signal)
    else:
        raise ValueError("Invalid filter type. Choose 'fir' or 'iir'.")

    return filtered_signal

# User input
filter_type = input("Enter filter type (FIR or IIR): ")
num_taps_or_order = int(input("Enter number of taps (for FIR) or order (for IIR): "))
cutoff_freq = float(input("Enter cutoff frequency: "))

# Design the filter
coefficients = design_filter(filter_type, num_taps_or_order, cutoff_freq)

# Generate a test signal
t = np.linspace(0, 1, 1000, endpoint=False)
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.normal(size=len(t))

# Apply the filter to the signal
filtered_signal = apply_filter(signal, coefficients, filter_type)

# Plot the original and filtered signals
plt.plot(t, signal, label='Original Signal')
plt.plot(t, filtered_signal, label=f'Filtered Signal ({filter_type.upper()})')
plt.legend()
plt.show()
