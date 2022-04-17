import pybel
import os

#def sdf_to_pdb():
input_folder = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligand_sdf\sdf"
output_folder = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligands_pdb\PDB"

for sdf_file in os.scandir(input_folder):
        # Extract the protein_code from path name, better than the option bellow
        # in this case because we have split proteins in monomers
    if sdf_file.is_file() and sdf_file.path.endswith('.sdf'):
        ligand_name = sdf_file.path.split('\\')[-1].split('.')[0]
        output_path = output_folder + '/' + ligand_name + '.pdb'
        for mol in pybel.readfile('sdf', sdf_file.path):
            mol.write('pdb', output_path, overwrite=True)
