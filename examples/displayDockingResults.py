from numpy import True_
from InteractionsAnalysis.resultsProcessing import processGninaResults, processVinaResults
from config import Config
import pandas as pd

if __name__ == "__main__":

    gnina_folder, vina_folder = Config.GNINA_DOCKING_FOLDER, Config.VINA_DOCKING_FOLDER
    df_gnina = processGninaResults(gnina_folder) 
    df_vina = processVinaResults(vina_folder)
    print("Average values for GNINA docking results:")
    print(df_gnina)


    print("\n\nAverage values for Vina docking results:")
    print(df_vina)

    print("\n\nMerged DataFrames...")
    merged_df = pd.merge(df_gnina, df_vina, on='code', sort=True).set_index('code')
    print(merged_df)

