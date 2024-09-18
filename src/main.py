import wave
import numpy as np
from scipy.signal import resample
import librosa

def apply_distortion(input_file, output_file, gain=2.0, threshhold=0.6):
    with wave.open(input_file, 'rb') as wave_in:
        params, audio_signal, framerate = preprocess(wave_in)

        # Add gain
        audio_signal = audio_signal * gain

        # Apply distortion
        max_val = np.iinfo(np.int16).max
        min_val = np.iinfo(np.int16).min
        audio_signal = np.clip(audio_signal, threshhold * min_val, threshhold * max_val)

        # Convert back to intager
        distorted_signal = audio_signal.astype(np.int16)

        # Apply volume boost
        audio_signal = audio_signal * 3.0

        # Write to output wav file
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(distorted_signal.tobytes())

    print(f"Distorted file written to {output_file}")

def preprocess(wave_in):
    params = wave_in.getparams()
    n_channels, sampwidth, framerate, n_frames, comptype, compname = params
    print(f"Channels: {n_channels}, Sample Width: {sampwidth}, Frame Rate: {framerate}, Frames: {n_frames}")

        # Convert to numpy array
    frames = wave_in.readframes(n_frames)
    audio_signal = np.frombuffer(frames, dtype=np.int16)
    return params, audio_signal, framerate

def apply_delay(input_file, output_file, delay_time=0.5, feedback=0.5, mix=0.5):
    with wave.open(input_file, 'rb') as wav_in:
        params = wav_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        
        # Read the frames and convert to numpy array
        frames = wav_in.readframes(n_frames)
        audio_signal = np.frombuffer(frames, dtype=np.int16)
        
        # Calculate the number of samples for the delay
        delay_samples = int(delay_time * framerate)
        
        # Create an empty array for the output signal
        output_signal = np.zeros_like(audio_signal)
        
        # Apply delay effect
        for i in range(delay_samples, len(audio_signal)):
            delayed_sample = int(audio_signal[i - delay_samples] * feedback)
            output_signal[i] = audio_signal[i] + delayed_sample
            
        # Mix the original (dry) and delayed (wet) signals
        output_signal = (audio_signal * (1 - mix) + output_signal * mix).astype(np.int16)
        
        # Write the output signal to the output WAV file
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(output_signal.tobytes())
    
    print(f"Delay effect applied and written to {output_file}")

def apply_chorus(input_file, output_file, delay_time=0.005, feedback=0.2, mix=0.5):
    with wave.open(input_file, 'rb') as wav_in:
        params = wav_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        
        # Read the frames and convert to numpy array
        frames = wav_in.readframes(n_frames)
        audio_signal = np.frombuffer(frames, dtype=np.int16)
        
        # Calculate the number of samples for the delay
        delay_samples = int(delay_time * framerate)
        
        # Create an empty array for the output signal
        output_signal = np.zeros_like(audio_signal)
        
        # Apply delay effect
        for i in range(delay_samples, len(audio_signal)):
            delayed_sample = int(audio_signal[i - delay_samples] * feedback)
            output_signal[i] = audio_signal[i] + delayed_sample
            
        # Mix the original (dry) and delayed (wet) signals
        output_signal = (audio_signal * (1 - mix) + output_signal * mix).astype(np.int16)
        
        # Write the output signal to the output WAV file
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(output_signal.tobytes())
    
    print(f"Chorus effect applied and written to {output_file}")


def transpose_octave(input_file, output_file):
    with wave.open(input_file, 'rb') as wave_in:
        params, audio_signal, framerate = preprocess(wave_in)

        # If the audio is stereo, take the mean to convert it to mono
        if params.nchannels > 1:
            audio_signal = audio_signal.reshape(-1, params.nchannels)
            audio_signal = audio_signal.mean(axis=1).astype(np.int16)

        # Perform the Fourier Transform
        freq_data = np.fft.rfft(audio_signal)
        
        # Resample the frequency data to shift it up an octave
        num_samples = len(audio_signal)
        new_freq_data = resample(freq_data, num_samples // 2)
        
        # Perform the inverse Fourier Transform
        new_time_data = np.fft.irfft(new_freq_data, num_samples)
        
        # Ensure the new data has the correct length
        new_time_data = new_time_data[:num_samples]

        # Convert the new_time_data to floating point for librosa
        new_time_data = new_time_data.astype(np.float32)

        # Apply time stretching
        new_time_data = librosa.effects.time_stretch(new_time_data, rate=0.5)
        
        # Convert the stretched data back to int16 for writing to WAV file
        new_time_data = (new_time_data * np.iinfo(np.int16).max).astype(np.int16)

        # Write the output WAV file
        with wave.open(output_file, 'wb') as wave_out:
            wave_out.setparams(params)
            wave_out.writeframes(new_time_data.tobytes())

    print(f"Transposed file written to {output_file}")

input_file = 'clean_input.wav'
output_file_up = 'output_octave_up.wav'  # Path to the output WAV file for octave up
output_file_down = 'output_octave_down.wav'  # Path to the output WAV file for octave down
output_file = 'output.wav'
output_file1 = 'output1.wav'
output_file2 = 'output2.wav'
output_file3 = 'output3.wav'
transpose_octave(input_file, output_file2)
apply_delay(input_file, output_file, delay_time=0.8, feedback=0.2, mix=0.5)
apply_distortion(output_file, output_file1, threshhold=0.01, gain=0.4)
apply_chorus(input_file, output_file3)

def create_loop():
    if input == record:
        # Start recording
        while recording:
            if input == stop:
                break
    file.write(output_file)

def playback():
    file.read(selected_track)
    player.play(selected_track)