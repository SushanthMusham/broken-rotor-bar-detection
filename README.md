# Broken Rotor Bar Detection in Induction Motors

A Python-based project for detecting and estimating the number of broken rotor bars in induction motors using Motor Current Signature Analysis (MCSA) and FFT-based signal processing.

## Overview

This project analyzes stator current signals to detect broken rotor bar faults without dismantling the motor. It extracts fault-related frequency components and uses calibrated decision thresholds to classify the rotor condition.

## Methodology

1. **Data Loading:** Load experimental current signals from MATLAB v7.3 files using `h5py`.
2. **Signal Processing:** Extract Phase A current and apply Fast Fourier Transform (FFT).
3. **Feature Extraction:** Measure the peak amplitude around the selected fault frequency of `175.44 Hz`.
4. **Threshold Calibration:** Calculate four decision thresholds using the mean amplitudes of five rotor health conditions.
5. **Fault Classification:** Classify the rotor condition based on the extracted amplitude and calibrated thresholds.

## Operating Conditions

- **Shaft Torque:** 4.0 Nm
- **Supply Frequency:** 60 Hz
- **Motor Slip:** 0.038
- **Acquisition Window:** 0.25 seconds
- **Selected Fault Frequency:** 175.44 Hz

## Results

The system was evaluated using 50 real experimental signals, with 10 signals for each rotor condition.

| Rotor Condition | Accuracy |
|---|---:|
| Healthy Rotor | 100% |
| 1 Broken Rotor Bar | 100% |
| 2 Broken Rotor Bars | 80% |
| 3 Broken Rotor Bars | 70% |
| 4 Broken Rotor Bars | 90% |
| **Overall Accuracy** | **88%** |

## Technologies Used

- Python
- NumPy
- SciPy
- h5py
- FFT-based Signal Processing

## Rotor Health Classes

The system classifies the motor into five categories:

1. Healthy Rotor (HR)
2. One Broken Rotor Bar (1BRB)
3. Two Broken Rotor Bars (2BRB)
4. Three Broken Rotor Bars (3BRB)
5. Four Broken Rotor Bars (4BRB)

## References

1. Maciejewski et al., *Decision Support System for Diagnosing Broken Rotor Bar Severity in Induction Motors*, IEEE Access, 2026. [DOI](https://doi.org/10.1109/ACCESS.2026.3657711)
2. Treml et al., *Experimental Database for Detecting and Diagnosing Rotor Broken Bar in a Three-Phase Induction Motor*, IEEE DataPort, 2020. [Dataset](https://ieee-dataport.org/open-access/experimental-database-detecting-and-diagnosing-rotor-broken-bar-three-phase-induction)

---
