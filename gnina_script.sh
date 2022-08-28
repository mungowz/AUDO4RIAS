#! /bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOCKING_FOLDER="${SCRIPTPATH}/gnina/docking"

for p in proteins/pdbqt/protein_*.pdbqt; do
  tmp=${p#*_}
  receptor=${tmp%.*}
  mkdir -p "${DOCKING_FOLDER}/${receptor}"

  for f in ligands/sdf/*.sdf; do
    tmp=${f#*_}
    ligand=${tmp%.*}
    echo
    echo
    echo ANALISI
    echo Processing protein "$receptor"
    echo Processing ligand "$ligand"
    mkdir -p "${DOCKING_FOLDER}/${receptor}/${ligand}"
    gnina --receptor "$p" --ligand "$f" --autobox_ligand "$f" --out "${DOCKING_FOLDER}/${receptor}/${ligand}/out.sdf.gz" --scoring vina --cnn_scoring=rescore --pose_sort_order Energy --cnn_verbose 
  done
done