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

        # Plot the audio waveform
        plt.figure(figsize=(10, 4))
        if channels == 2:
            plt.plot(time, audio_array[:, 0], label='Channel 1')
            plt.plot(time, audio_array[:, 1], label='Channel 2')
        else:
            plt.plot(time, audio_array[:, 0])
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.legend()
        plt.grid(True)
        plt.show()


# Ask for the audio file path
audio_file = input("Enter the audio file path: ")

# Plot the audio waveform
plot_waveform(audio_file)
