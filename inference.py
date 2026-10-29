import h5py
import numpy as np
import time
from src.model import BRBDiagnosticSystem
from src.config import FS

# Configuration parameters
TARGET_LOAD = "4.0Nm"
MATLAB_KEY = "torque40"
SLIP = 0.038
T_ACQ = 0.25

def load_all_trials(filepath, matlab_key, t_acq=T_ACQ, fs=FS):
    """Loads all 10 real test trials from a MATLAB v7.3 file."""
    signals = []
    with h5py.File(filepath, 'r') as f:
        root_key = [k for k in f.keys() if k != '#refs#'][0]
        ia_references = f[root_key][matlab_key]['Ia']
        
        for i in range(ia_references.shape[0]):
            ref = ia_references[i, 0]
            raw_signal = np.array(f[ref]).flatten()
            # Extract steady-state portion (last 0.25s)
            samples_needed = int(fs * t_acq)
            signals.append(raw_signal[-samples_needed:])
            
    return signals

if __name__ == "__main__":
    # 1. Load our trained model boundaries (C1, C2, C3, C4)
    system = BRBDiagnosticSystem()
    system.load("data/thresholds.json")
    print("Model loaded successfully. Starting batch evaluation...\n")

    # Mapping each class label to its real .mat file path
    file_mapping = {
        'HR':   "data/raw/HR/struct_rs_R1.mat",
        '1BRB': "data/raw/1BRB/struct_r1b_R1.mat",
        '2BRB': "data/raw/2BRB/struct_r2b_R1.mat",
        '3BRB': "data/raw/3BRB/struct_r3b_R1.mat",
        '4BRB': "data/raw/4BRB/struct_r4b_R1.mat"
    }

    total_tests = 0
    correct_predictions = 0

    print(f"--- Real Dataset Accuracy Evaluation ({TARGET_LOAD}) ---")

    # 2. Loop through every class and its 10 real trials
    for true_label, filepath in file_mapping.items():
        trials = load_all_trials(filepath, MATLAB_KEY)
        class_correct = 0
        
        for signal in trials:
            total_tests += 1
            
            # Run inference on the real signal
            prediction, amp = system.predict(signal, load_key=TARGET_LOAD, slip=SLIP)
            
            # Check if the model's prediction string matches the true label
            if true_label in prediction:
                correct_predictions += 1
                class_correct += 1
                
        print(f"Condition [{true_label:4s}] -> Correct: {class_correct}/{len(trials)} trials")

    # 3. Calculate and display final accuracy
    accuracy = (correct_predictions / total_tests) * 100
    
    print("\n========================================")
    print(f"Total Trials Tested    : {total_tests}")
    print(f"Correct Diagnoses      : {correct_predictions}")
    print(f"Overall Model Accuracy : {accuracy:.2f}%")
    print("========================================")