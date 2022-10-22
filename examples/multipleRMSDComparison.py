from InteractionsAnalysis.resultsProcessing import RMSDComparison
from config import Config
from statistics import fmean
import pandas as pd
if __name__ == "__main__":
    # initialize environment
    ligands_folder = Config.LIGANDS_SDF_FOLDER
    docking_folders = [Config.VINA_DOCKING_FOLDER, Config.GNINA_DOCKING_FOLDER]
    receptors = ["1fcu", "2h8v", "3fe9", "4e81", "5xz3_A", "6lqk_B"]

    
    data = []

    for receptor in receptors:
        record = {}
        result = RMSDComparison(receptor, ligands_folder, docking_folders, verbose=False)
        magnitude = "{:.1e}".format(abs(result[0][0] - result[0][1]))
        record['Vina'], record['GNINA'], record['Magnitude'] = result[0][0], result[0][1], magnitude
        data.append(record)

    df = pd.DataFrame(data, index=receptors, columns=['Vina', 'GNINA', 'Magnitude'])
    
    print(df)

    vina_mean, gnina_mean = fmean(df['Vina']), fmean(df['GNINA'])
    magnitude = "{:.1e}".format(abs(vina_mean - gnina_mean))
    print(f"\nVina RMSDs mean: {vina_mean}\nGNINA RMSDs mean: {gnina_mean}\nMagnitude: {magnitude}")