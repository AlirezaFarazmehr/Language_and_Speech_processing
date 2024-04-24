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


# Ask for the audio file paths
audio_files = [input(f"Enter the path of audio file for 'a': "), input(f"Enter the path of audio file for 'i': ")]

# Plot the audio waveforms
plt.figure(figsize=(15, 5))

for i, audio_file in enumerate(audio_files):
    time, audio_array = plot_waveform(audio_file)
    plt.subplot(1, 2, i + 1)
    plt.plot(time, audio_array)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Waveform for "{chr(97 + i)}" sound')

plt.tight_layout()
plt.show()
