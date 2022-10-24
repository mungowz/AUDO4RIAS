from config import Config
import os
import pickle
import pandas as pd


if __name__ == "__main__":
        
    vina_folder, gnina_folder = Config.VINA_DOCKING_FOLDER, Config.GNINA_DOCKING_FOLDER
    
    vina_data, gnina_data = os.path.join(vina_folder, 'data.p'), os.path.join(gnina_folder, 'data.p')
    # retrieve scores and contact states
    with open(vina_data, 'rb') as fp1, open(gnina_data, 'rb') as fp2:
        vina_scores = pickle.load(fp1)
        gnina_scores = pickle.load(fp2)

    receptors = ["1fcu", "2h8v", "3fe9", "4e81", "5xz3_A", "6lqk_B"]
    
    data = []
    for receptor in receptors:
        record = {}
        record['vina_cc'] = int(pd.DataFrame(vina_scores[receptor]).sum(axis="columns")["close_contacts"])
        record['vina_hb'] = int(pd.DataFrame(vina_scores[receptor]).sum(axis="columns")["hydrogen_bonds"])
        record['vina_ratio'] = float(record['vina_hb']/(record['vina_cc']+record['vina_hb']))
        record['gnina_cc'] = int(pd.DataFrame(gnina_scores[receptor]).sum(axis="columns")["close_contacts"])
        record['gnina_hb'] = int(pd.DataFrame(gnina_scores[receptor]).sum(axis="columns")["hydrogen_bonds"])
        record['gnina_ratio'] = float(record['gnina_hb']/(record['gnina_cc']+record['gnina_hb']))
        data.append(record)
    df = pd.DataFrame(data, index=receptors)
    print(df)



    #vina_cc = [sum(vina_scores[receptor][res]["close_contacts"]) for receptor in receptors for res in vina_scores[receptor].keys() if 'close_contacts' in vina_scores[receptor][res].keys()]
    #vina_hb = [sum(vina_scores[receptor][res]['hydrogen_bonds']) for receptor in receptors for res in vina_scores[receptor].keys() if 'hydrogen_bonds' in vina_scores[receptor][res].keys()]

    #gnina_cc = [sum(gnina_scores[receptor][res]["close_contacts"]) for receptor in receptors for res in gnina_scores[receptor].keys() if 'close_contacts' in gnina_scores[receptor][res].keys()]
    #gnina_hb = [sum(gnina_scores[receptor][res]['hydrogen_bonds']) for receptor in receptors for res in gnina_scores[receptor].keys() if 'hydrogen_bonds' in gnina_scores[receptor][res].keys()]
    
    

    