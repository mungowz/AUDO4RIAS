import pybel
import openpyxl
import os

input_folder = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligand_sdf/sdf_2'
output_folder = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligands_pdb/From_sfd_2'


for sdf_file in os.scandir(input_folder):
    # Extract the protein_code from path name, better than the option bellow
    # in this case because we have split proteins in monomers
    if sdf_file.is_file():
        ligand_path = sdf_file.path
        if ligand_path.endswith('.sdf'):
            ligand_name = ligand_path.split('\\')[-1].split('.')[0]
            output_path = output_folder + '/' + ligand_name + '.pdb'
            for mol in pybel.readfile('sdf', ligand_path):
                mol.write('pdb', output_path, overwrite=True)
