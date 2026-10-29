import h5py

file_path = "data/raw/HR/struct_rs_R1.mat"

print("Opening file...")
with h5py.File(file_path, 'r') as f:
    rs_data = f['rs']
    
    # Look inside the first load level
    torque05_group = rs_data['torque05']
    print("\nVariables inside 'torque05':", list(torque05_group.keys()))
    
    # Let's dynamically check what's inside the first item of torque05
    first_inner_key = list(torque05_group.keys())[0]
    first_item = torque05_group[first_inner_key]
    
    if isinstance(first_item, h5py.Dataset):
        print(f"Shape of dataset '{first_inner_key}':", first_item.shape)
    elif isinstance(first_item, h5py.Group):
        print(f"'{first_inner_key}' is another Group containing:", list(first_item.keys()))