import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


def plot_waveform(audio_file):
    # Open the audio file
    with wave.open(audio_file, 'rb') as wf:
        # Extract audio file parameters
        channels = wf.getnchannels()
        framerate = wf.getframerate()
        frames = wf.getnframes()
        width = wf.getsampwidth()

        # Read audio data
        audio_data = wf.readframes(frames)

        # Convert binary data to numpy array
        if width == 1:
            dtype = np.uint8  # 8-bit unsigned integer
        elif width == 2:
            dtype = np.int16  # 16-bit signed integer
        else:
            raise ValueError("Unsupported sample width")

        audio_array = np.frombuffer(audio_data, dtype=dtype)

        # Convert array to 2D if the file is stereo
        if channels == 2:
            audio_array = audio_array.reshape(-1, 2)
        else:
            audio_array = audio_array.reshape(-1, 1)

        # Calculate time corresponding to each audio sample
        time = np.linspace(0, len(audio_array) / framerate, num=len(audio_array))

        return time, audio_array


# Function to compare waveforms
def compare_waveforms(audio_files):
    data = []
    for audio_file in audio_files:
        time, audio_array = plot_waveform(audio_file)
        data.append((time, audio_array))

    # Find the shortest audio file length
    min_len = min([len(data[i][1]) for i in range(len(data))])

    # Truncate audio data to the length of the shortest file
    for i in range(len(data)):
        data[i] = (data[i][0][:min_len], data[i][1][:min_len])

    # Calculate differences
    differences = {}
    for i in range(1, len(data)):
        time_diff = np.mean(data[i][0] - data[0][0])
        amplitude_diff = np.mean(data[i][1] - data[0][1])
        differences[f"Time difference between file {i + 1} and file 1"] = time_diff
        differences[f"Amplitude difference between file {i + 1} and file 1"] = amplitude_diff

    return differences


# Ask for the audio file paths
audio_files = []
for i in range(5):
    audio_files.append(input(f"Enter the path of audio file {i + 1}: "))

# Compare waveforms
differences = compare_waveforms(audio_files)

# Print differences
print("\nDifferences between waveforms:")
for key, value in differences.items():
    print(f"{key}: {value}")
