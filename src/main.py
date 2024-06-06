import wave
import numpy as np
from scipy.signal import resample

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

def apply_octaver(input_file, output_file, shift='up'):
    with wave.open(input_file, 'rb') as wav_in:
        params = wav_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        
        # Read the frames and convert to numpy array
        frames = wav_in.readframes(n_frames)
        audio_signal = np.frombuffer(frames, dtype=np.int16)
        
        # Handle stereo audio by splitting channels
        if n_channels == 2:
            audio_signal = audio_signal.reshape(-1, 2)
        
        # Define resampling factors
        if shift == 'up':
            factor = 0.5  # Octave up
        elif shift == 'down':
            factor = 2.0  # Octave down
        else:
            raise ValueError("shift parameter must be 'up' or 'down'")
        
        # Resample the audio signal
        if n_channels == 2:
            resampled_signal = np.array([resample(audio_signal[:, ch], int(len(audio_signal) * factor)) for ch in range(2)]).T
        else:
            resampled_signal = resample(audio_signal, int(len(audio_signal) * factor))
        
        # Interpolate to match the original length
        original_indices = np.arange(len(audio_signal))
        resampled_indices = np.linspace(0, len(audio_signal), num=len(resampled_signal))
        
        if n_channels == 2:
            shifted_signal = np.array([np.interp(original_indices, resampled_indices, resampled_signal[:, ch]) for ch in range(2)]).T
        else:
            shifted_signal = np.interp(original_indices, resampled_indices, resampled_signal)

        print(f"Resample done on {n_channels}")
        
        # Convert the signal back to int16
        shifted_signal = np.clip(shifted_signal, np.iinfo(np.int16).min, np.iinfo(np.int16).max).astype(np.int16)
        
        # Flatten the signal for stereo
        if n_channels == 2:
            shifted_signal = shifted_signal.reshape(-1)
        
        # Write the shifted signal to the output WAV file
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(shifted_signal.tobytes())
    
    print(f"Octaver effect applied ({shift} an octave) and written to {output_file}")



input_file = 'clean_input.wav'
output_file_up = 'output_octave_up.wav'  # Path to the output WAV file for octave up
output_file_down = 'output_octave_down.wav'  # Path to the output WAV file for octave down
output_file = 'output.wav'
output_file1 = 'output1.wav'
output_file2 = 'output2.wav'
output_file3 = 'output3.wav'
apply_octaver(input_file, output_file_up, shift='up')
apply_octaver(input_file, output_file_down, shift='down')
apply_delay(input_file, output_file, delay_time=0.8, feedback=0.2, mix=0.5)
apply_distortion(output_file, output_file1, threshhold=0.01, gain=0.4)