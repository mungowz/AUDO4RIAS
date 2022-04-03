import os
import pandas as pd
import openpyxl
import pubchempy as pcp
from pubchempy import get_compounds
import re
import xlsxwriter
import xlwt

#as_EU = r'C:\Users\cactus\Dropbox\Docking\ligands_PESTEU\ActiveSubstances.xlsx'
as_EU = '/media/sf_Dropbox/Docking/ligands_PESTEU/ActiveSubstances.xlsx'
sheet = 'approvedEU'
df_asEU = pd.read_excel(io=as_EU, sheet_name=sheet)
###################################################################
# This script extracts the substance 3D structures and chemical smiles from pubchem.
# I first though of using the smiles
# to create the 3D structures for substances with no 3D structure available. I have more scripts to later
# transform this to a pdb, but for some substances the 3D structure was not looking great.
# The reason why this substances
# don't have a 3D structure is because they are mixtures, salts, too long... so I decided to stick only
# to substances with 3D structure available to be on the save side.
# Still I kept the smiles line commented in case it is interestig to use them in the
# future but I didn't include it for the dataframe.

###################################################################
# create path to outputfolder and dictionaries
output_folder_pdb = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligand_sdf/sdf_1'
substance_dict = dict()
# sometimes the name of pubchem and EUdata set is not matching because there is an explanation in ()
# this dictionary will contain the cases for wich deleting the () was helpfull to retrieve the 3D structure
substance_noparent = dict()
# Not necesary anymore, as we will not use smiles. The susbtance from this category will move to substance_problem
#substance_onlysmiles = dict()
substance_problem = dict()
for substance in df_asEU['Substance']:
# check if 3D structure is available
    structure = get_compounds(substance, 'name', record_type='3d')
# if 3D structures available, download and to dictionary
    if structure != []:
        file_name = substance+".sdf"
        path = output_folder_pdb+"/"+file_name
        pcp.download('SDF', path, substance, 'name',record_type='3d', overwrite=True)
        substance_dict[substance] = {'Substance':substance} # if smiles are used then comment this line!!
########################################################
# This part is not needed as we won't use the smiles
        #for compound in get_compounds(substance, 'name'):
            #smiles = compound.isomeric_smiles
# if smiles is not empty then create dictionary for substance and smiles
            #substance_dict[smiles] = {'Substance':substance, 'SMILES':smiles}
#########################################################
# if 3d not available, try again without ()
    if structure == []:
        substance_no_parenthesis = re.sub('(\(.*\))', "", substance).lstrip('-')
        structure2 = get_compounds(substance_no_parenthesis, 'name', record_type='3d')
        if structure2 != []:
            file_name = substance_no_parenthesis+".sdf"
            path = output_folder_pdb+"/"+file_name
            pcp.download('SDF', path, substance_no_parenthesis, 'name',record_type='3d', overwrite=True)
            substance_noparent[substance] = {'Substance':substance, # if smiles are used then comment this line!!
                                                'Substance_no_parenthesis':substance_no_parenthesis}
################################################################
# This part is not needed as we won't use the smiles
            #for compound in get_compounds(substance_no_parenthesis, 'name'):
                #smiles = compound.isomeric_smiles
                #substance_noparent[smiles] = {'Substance':substance,
                                                #'Substance_no_parenthesis':substance_no_parenthesis, 'SMILES':smiles}
# if still not available extract smiles to different dic.
        #smiles = ""
        #for compound in get_compounds(substance, 'name'):
            #smiles = compound.isomeric_smiles
            #if smiles != "":
                #substance_onlysmiles[smiles] = {'Substance':substance, 'SMILES':smiles}
# if still issues extract substance name to issue diccionary and check why issue
        #if smiles == "":
            #for compound in get_compounds(substance_no_parenthesis, 'name'):
                #smiles = compound.isomeric_smiles
                #if smiles != "":
                    #substance_dict[smiles] = {'Substance':substance, 'SMILES':smiles}

            #if smiles == "":
                #substance_problem[substance] = {'Substance':substance, 'Substance_no_parenthesis':substance_no_parenthesis}
####################################################################
        if structure2 == []: # if smiles are used then comment this line!!
            substance_problem[substance] = {'Substance':substance, 'Substance_no_parenthesis':substance_no_parenthesis}
df_3d= pd.DataFrame.from_dict(substance_dict).transpose()
df_3dnoparent= pd.DataFrame.from_dict(substance_noparent).transpose()
#df_onlysmiles=pd.DataFrame.from_dict(substance_onlysmiles).transpose() # Only if smiles are used
df_issues= pd.DataFrame.from_dict(substance_problem).transpose()
# This part is only needed when smiles are used
##################################################################
# The same substance can have more than 1 smiles. So now in the dataframe we have repeated names
# We create fuction to rename duplicates for substances with >1 smiles.
# Nevertheless the 3D structure was only downloaded 1 time regardless of how many smiles the subtance had
#def rename_duplicates(df):
# create a dictionary to imput the substance names
    #duplicates = dict()
    #for i,row in df.iterrows():
        #substance_name = row["Substance"]
        #if substance_name not in duplicates:
# if substance is not repeated, the value is 1
            #duplicates[substance_name]=1
# if substance is repeated the value is = to how many times it is repeated
        #else:
            #duplicates[substance_name]+=1
            #df.at[i,"Substance"]=substance_name+"_"+str(duplicates[substance_name])
# This part is only needed when smiles are used
#######################################################
# rename_duplicates
#rename_duplicates(df_3d)
#rename_duplicates(df_3dnoparent)
#rename_duplicates(df_onlysmiles)
#rename_duplicates(df_issues)
#path = r'C:\Users\cactus\Dropbox\Docking\ligands_PESTEU'
#path = r'/media/sf_Dropbox/Docking/ligands_PESTEU'
writer = pd.ExcelWriter(path+'/'+'ligands_pubchem.xlsx', engine='xlsxwriter')

# write each DataFrame to a specific sheet
df_3d.to_excel(writer, sheet_name='3D',index = False)
df_3dnoparent.to_excel(writer, sheet_name='3Dnoparent',index = False)
#df_onlysmiles.to_excel(writer, sheet_name='onlysmiles',index = False) # Only if smiles are used
df_issues.to_excel(writer, sheet_name='issues',index = False)

#close the Pandas Excel writer and output the Excel file
writer.save()
#################### CHECK ISSUES MANUALLY##################################
# same process was repeated after checking the issue. A new sheet was created called issues_check.
# The 3D structure search was performed for the column pubchem_name
# Note: for a few structures it was noted that the structure was available with the same name in pubchem
# as in the EUdatabase but still the 3D structure was not downloaded with the script. I don't know
# what was the proble, but as there were only a few I extracted them manually. Exaple 'Ziram'
#################################################################################################
#file = r'C:\Users\cactus\Dropbox\Docking\ligands_PESTEU\ligandspubchem.xlsx'
file = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligands_pubchem.xlsx'
sheet = 'issues_check'
df_issues = pd.read_excel(io=file, sheet_name=sheet)
df_pubchem = df_issues['pubchem_name'].dropna()

#I put the 3D structures in a different folder just in case
output_folder_pdb = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligand_sdf/sdf_2'
substance_dict = dict()
# sometimes the name of pubchem and EUdata set is not matching because there is an explanation in ()
# this dictionary will contain the cases for wich deleting the () was helpfull to retrieve the 3D structure
substance_problem = dict()
for substance in df_pubchem:
# check if 3D structure is available
    structure = get_compounds(substance, 'name', record_type='3d')
# if 3D structures available, download and to dictionary
    if structure != []:
        file_name = substance+".sdf"
        path = output_folder_pdb+"/"+file_name
        pcp.download('SDF', path, substance, 'name',record_type='3d', overwrite=True)
        substance_dict[substance] = {'Substance':substance}
# if 3d not available, try again without ()
    if structure == []:
        substance_problem[substance] = {'Substance':substance}

df_3d_2 = pd.DataFrame.from_dict(substance_dict).transpose()
df_issues_2 = pd.DataFrame.from_dict(substance_problem).transpose()
#file_name = r'C:\Users\cactus\Dropbox\Docking\ligands_PESTEU\ligands_pubchem.xlsx'
file_name = '/media/sf_Dropbox/Docking/ligands_PESTEU/ligands_pubchem.xlsx'

# -to add call to a function delete_duplicate_ligands()

excel_book = openpyxl.load_workbook(file_name)

with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    writer.book = excel_book
    writer.sheets = {
        worksheet.title: worksheet
        for worksheet in excel_book.worksheets
    }
    df_3d_2.to_excel(writer, '3D_2', index = False)
    df_issues_2.to_excel(writer, 'issues_2',index = False)
    writer.save()
