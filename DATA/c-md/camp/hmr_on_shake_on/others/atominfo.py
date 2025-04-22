import parmed

# Load the prmtop or parm7 file
prmtop = parmed.load_file('ti.prmtop')  # Replace with your file name

# Specify the residue ID for which you want to get the atomic masses
target_resid = 1  # Replace with your desired residue ID

# Filter atoms by residue ID and extract their names and masses
atom_data = [
    (atom.name, atom.mass) for atom in prmtop.atoms if atom.residue.number == target_resid
]

# File name to save
output_file = f'atom_{target_resid}_info.dat'

# Write the data to the file
with open(output_file, 'w') as f:
    f.write(f"# Atom Name\tMass (amu) for Residue {target_resid}\n")
    for atom_name, mass in atom_data:
        f.write(f"{atom_name}\t{mass:.3f}\n")

print(f"Atom name and mass information for residue {target_resid} saved to {output_file}")

