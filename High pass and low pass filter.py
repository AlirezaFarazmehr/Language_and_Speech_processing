import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import os

# Set the Matplotlib backend to 'Agg'
plt.switch_backend('Agg')

# Ask user for the input file path
input_file = input("Enter the path to the audio file: ")

# Default output paths
low_pass_output_file = "low_pass_filtered.wav"
high_pass_output_file = "high_pass_filtered.wav"

# Read the audio file
rate, data = wavfile.read(input_file)
# Convert to mono if stereo
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Function to apply filter
def butter_filter(data, cutoff, fs, order=5, btype='low'):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    y = lfilter(b, a, data)
    return y

# Low-pass filter to remove glass sound
low_cutoff = 500  # Adjust as needed
low_filtered_data = butter_filter(data, low_cutoff, rate, order=6, btype='low')

# High-pass filter to remove voice sound
high_cutoff = 1000  # Adjust as needed
high_filtered_data = butter_filter(data, high_cutoff, rate, order=6, btype='high')

# Save the filtered audio files
wavfile.write(low_pass_output_file, rate, low_filtered_data.astype(np.int16))
print(f"Low-pass filtered audio saved as '{low_pass_output_file}' - This should have minimized the glass sound.")

wavfile.write(high_pass_output_file, rate, high_filtered_data.astype(np.int16))
print(f"High-pass filtered audio saved as '{high_pass_output_file}' - This should have minimized the voice sound.")

# Plot the frequency responses and the original and filtered signals
plt.figure(figsize=(15, 8))

# Original signal
plt.subplot(3, 1, 1)
plt.plot(data)
plt.title('Original Signal')

# Low-pass filtered signal
plt.subplot(3, 1, 2)
plt.plot(low_filtered_data)
plt.title('Low-pass Filtered Signal (Glass Sound Removed)')

# High-pass filtered signal
plt.subplot(3, 1, 3)
plt.plot(high_filtered_data)
plt.title('High-pass Filtered Signal (Voice Removed)')

plt.tight_layout()
plt.savefig('filtered_signals.png')
plt.close()

# Plot the frequency responses of the filters
plt.figure(figsize=(12, 6))
for cutoff, btype in zip([low_cutoff, high_cutoff], ['low', 'high']):
    b, a = butter(6, cutoff / (0.5 * rate), btype=btype, analog=False)
    w, h = freqz(b, a, worN=8000)
    plt.plot(0.5 * rate * w / np.pi, np.abs(h), label=f'{btype.capitalize()}-pass Filter (cutoff={cutoff} Hz)')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')
plt.title('Frequency Response of Filters')
plt.savefig('frequency_response.png')
plt.close()

# Report results
print("Filtering completed. Results:")
print(f"Low-pass filtered audio saved as '{low_pass_output_file}' - This should have minimized the glass sound.")
print(f"High-pass filtered audio saved as '{high_pass_output_file}' - This should have minimized the voice sound.")
print("Plots saved as 'filtered_signals.png' and 'frequency_response.png'.")
