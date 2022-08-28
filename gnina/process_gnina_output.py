from operator import contains
from openbabel import pybel
import pandas as pd
import os
from config import Config

gnina_folder = Config.GNINA_DOCKING_FOLDER
for root, dirs, files in os.walk(gnina_folder):
    for file in files:
        if file == "out.sdf.gz":
            filepath = os.path.join(root, file)
            # filepath = f"/home/gomax22/Desktop/Computational-Docking/gnina/docking/1fcq/1-(4-Chlorophenyl)-5-(2-methoxyethoxy)-4-oxo-1,4-dihydrocinnoline-3-carboxylic_acid/out.sdf.gz"
            scores = []
            for mol in pybel.readfile('sdf', filepath):
                # keys: minimizedAffinity, CNNscore, CNNaffinity, CNN_VS, CNNaffinity_variance
                scores.append({'title': mol.title, 
                'CNNscore': float(mol.data['CNNscore']),
                'CNNaffinity': float(mol.data['CNNaffinity']),
                'Vinardo': float(mol.data['minimizedAffinity'])})

            scores = pd.DataFrame(scores)
            scores['label'] = scores.title.str.contains('active')
            print(scores)

