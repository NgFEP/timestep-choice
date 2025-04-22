from rdkit import Chem
from rdkit.Chem import AllChem, rdFMCS

# Load ethane and ethanol from PDB files
ethane = Chem.MolFromPDBFile("ethane.pdb")
ethanol = Chem.MolFromPDBFile("ethanol.pdb")

# Add hydrogens and generate 3D conformations if needed
AllChem.EmbedMolecule(ethane)
AllChem.EmbedMolecule(ethanol)

# Find the Maximum Common Substructure (MCS)
mcs = rdFMCS.FindMCS([ethane, ethanol])
mcs_smarts = mcs.smartsString
mcs_mol = Chem.MolFromSmarts(mcs_smarts)

# Get the atom mapping for alignment
ethane_match = ethane.GetSubstructMatch(mcs_mol)
ethanol_match = ethanol.GetSubstructMatch(mcs_mol)

# Align ethanol to ethane based on MCS
AllChem.AlignMol(ethanol, ethane, atomMap=list(zip(ethanol_match, ethane_match)))

# Optional: Save aligned ethanol to a new PDB file
Chem.MolToPDBFile(ethanol, "aligned_ethanol.pdb")

print("Alignment complete. Aligned ethanol saved as aligned_ethanol.pdb")

