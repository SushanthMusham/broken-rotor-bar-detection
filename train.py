import h5py
import numpy as np
import os
from src.model import BRBDiagnosticSystem
from src.config import FS

# 1. Update our single profile to match the MATLAB folder name ('torque40')
TARGET_LOAD = "4.0Nm"
PROFILE = {
    "matlab_key": "torque40", 
    "slip": 0.038, 
    "t_acq": 0.25
}

def load_real_mat_signals(file_path, matlab_load_key, t_acq, fs=FS):
    """
    Reads the 10 trials from the MATLAB v7.3 HDF5 file and extracts 
    the steady-state portion of Phase A ('Ia').
    """
    signals = []
    
    # Open the HDF5 file
    with h5py.File(file_path, 'r') as f:
        # Find the root struct name dynamically (e.g., 'rs', 'r1b', etc. ignoring '#refs#')
        root_key = [key for key in f.keys() if key != '#refs#'][0]
        
        # Navigate to: root -> torque40 -> Ia
        ia_references = f[root_key][matlab_load_key]['Ia']
        
        # Loop through the 10 trials
        for i in range(ia_references.shape[0]):
            # 1. Dereference the pointer to get the actual data array
            ref = ia_references[i, 0]
            raw_signal = np.array(f[ref]).flatten()
            
            # 2. Extract the last t_acq seconds (steady-state regime)
            samples_needed = int(fs * t_acq)
            steady_state_signal = raw_signal[-samples_needed:]
            
            signals.append(steady_state_signal)
            
    return signals

if __name__ == "__main__":
    system = BRBDiagnosticSystem()
    
    print(f"--- Training Model for Single Load: {TARGET_LOAD} with REAL DATA ---")
    
    matlab_key = PROFILE["matlab_key"]
    slip = PROFILE["slip"]
    t_acq = PROFILE["t_acq"]

    # 2. Map the classes to your exact downloaded file paths
    file_mapping = {
        'HR':   "data/raw/HR/struct_rs_R1.mat",
        '1BRB': "data/raw/1BRB/struct_r1b_R1.mat",
        '2BRB': "data/raw/2BRB/struct_r2b_R1.mat",
        '3BRB': "data/raw/3BRB/struct_r3b_R1.mat",
        '4BRB': "data/raw/4BRB/struct_r4b_R1.mat"
    }

    dataset = {}
    
    # 3. Load the data from the .mat files
    for cls_name, filepath in file_mapping.items():
        if not os.path.exists(filepath):
            print(f"Error: Could not find {filepath}. Make sure your folders are set up!")
            exit()
            
        print(f"Loading {cls_name} data from {filepath}...")
        dataset[cls_name] = load_real_mat_signals(filepath, matlab_key, t_acq)

    # 4. Train the thresholds using the real signal features
    print("\nCalculating decision thresholds based on real 3rd harmonic sidebands...")
    system.fit_load_condition(dataset, load_key=TARGET_LOAD, slip=slip)
    
    # Extract the values into a list first, then round them!
    threshold_values = list(system.thresholds[TARGET_LOAD].values())
    print(f"Calculated Thresholds [C1, C2, C3, C4]: {np.round(threshold_values, 4)}")
    
    # 5. Save the trained model
    system.save("data/thresholds.json")
    print("\nCalibration saved successfully to data/thresholds.json! You are ready for real-time inference.")