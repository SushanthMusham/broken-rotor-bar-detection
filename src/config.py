# Motor & Acquisition Specifications
FS = 50000            # Sampling rate: 50 kHz
F_SUPPLY = 60.0        # Supply frequency: 60 Hz
T_ACQ_NOMINAL = 0.25   # Acquisition window: 0.25 s (15 electrical cycles)

# Operating Load Classes (Torque in Nm -> Expected Slip)
LOAD_PROFILES = {
    "0.5Nm": {"slip": 0.008, "t_acq": 1.0},    # Low load requires longer window (60 periods)
    "1.0Nm": {"slip": 0.012, "t_acq": 0.5},    # 30 periods
    "2.0Nm": {"slip": 0.021, "t_acq": 0.25},   # 15 periods
    "3.0Nm": {"slip": 0.029, "t_acq": 0.25},   # 15 periods
    "4.0Nm": {"slip": 0.038, "t_acq": 0.25},   # Nominal load (15 periods)
}