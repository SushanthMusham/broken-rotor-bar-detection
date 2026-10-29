import json
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

class BRBDiagnosticSystem:
    def __init__(self, fs=50000, f_supply=60.0):
        self.fs = fs             # Sampling frequency (50 kHz)
        self.f_supply = f_supply # Fundamental frequency (60 Hz)
        self.thresholds = {}     # Stores our cut-off boundaries (C1, C2, C3, C4)

    def compute_fft(self, signal):
        """Converts raw time-domain current signal into a frequency spectrum."""
        N = len(signal)
        freqs = rfftfreq(N, d=1.0 / self.fs)
        amplitudes = np.abs(rfft(signal)) * (2.0 / N)
        return freqs, amplitudes

    def extract_sideband_peak(self, freqs, amplitudes, slip):
        """
        Locates the 1st Left Sideband of the 3rd Harmonic:
        Formula: f_BRB = (3 - 2 * slip) * f_supply
        """
        target_freq = (3 - 2 * slip) * self.f_supply

        # Look in a tight window around the theoretical frequency (±1.5 Hz)
        band_mask = (freqs >= target_freq - 1.5) & (freqs <= target_freq + 1.5)
        band_amps = amplitudes[band_mask]

        if len(band_amps) == 0:
            return 0.0

        # Find local maximum peak height
        peaks, _ = find_peaks(band_amps)
        if len(peaks) > 0:
            return float(np.max(band_amps[peaks]))
        return float(np.max(band_amps))

    def fit_load_condition(self, training_data, load_key, slip):
        """
        OFFLINE TRAINING: 
        1. Takes 10 trials for each of the 5 classes (HR to 4BRB).
        2. Measures average sideband height for each class.
        3. Sets midpoint cut-off thresholds (C1, C2, C3, C4) between them.
        """
        classes = ['HR', '1BRB', '2BRB', '3BRB', '4BRB']
        means = {}

        for cls in classes:
            amps = []
            for sig in training_data[cls]:
                freqs, spectral_amps = self.compute_fft(sig)
                amp = self.extract_sideband_peak(freqs, spectral_amps, slip)
                amps.append(amp)
            means[cls] = float(np.mean(amps))

        # Calculate midpoint fences between adjacent severity classes
        self.thresholds[load_key] = {
            "C1": (means['HR']   + means['1BRB']) / 2.0,
            "C2": (means['1BRB'] + means['2BRB']) / 2.0,
            "C3": (means['2BRB'] + means['3BRB']) / 2.0,
            "C4": (means['3BRB'] + means['4BRB']) / 2.0
        }

    def predict(self, signal, load_key, slip):
        """
        ONLINE INFERENCE:
        Takes a new signal, measures its sideband peak, and drops it 
        into the threshold buckets to diagnose the fault.
        """
        if load_key not in self.thresholds:
            raise KeyError(f"Load '{load_key}' is not calibrated in thresholds.")

        th = self.thresholds[load_key]
        freqs, amps = self.compute_fft(signal)
        a_star = self.extract_sideband_peak(freqs, amps, slip)

        if a_star < th["C1"]:
            label = "Healthy Rotor (HR)"
        elif th["C1"] <= a_star < th["C2"]:
            label = "1 Broken Rotor Bar (1BRB)"
        elif th["C2"] <= a_star < th["C3"]:
            label = "2 Broken Rotor Bars (2BRB)"
        elif th["C3"] <= a_star < th["C4"]:
            label = "3 Broken Rotor Bars (3BRB)"
        else:
            label = "4 Broken Rotor Bars (4BRB)"

        return label, a_star

    def save(self, filepath="data/thresholds.json"):
        with open(filepath, "w") as f:
            json.dump(self.thresholds, f, indent=4)

    def load(self, filepath="data/thresholds.json"):
        with open(filepath, "r") as f:
            self.thresholds = json.load(f)