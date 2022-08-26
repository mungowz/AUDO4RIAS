#! /bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOCKING_FOLDER="${SCRIPTPATH}/vina/docking"

for p in proteins/pdbqt/protein_*.pdbqt; do
  tmp=${p#*_}
  receptor=${tmp%.*}
  mkdir -p "${DOCKING_FOLDER}/${receptor}"
  for g in proteins/gridbox_output/protein_*_grid.txt; do
    tmp=${g#*_}
    tmp=${tmp#*_}
    gridbox=${tmp%_*}
    if [ "$receptor" = "$gridbox" ]; then
      break
    fi
  done

  for f in ligands/pdbqt/ligand_*.pdbqt; do
    tmp=${f#*_}
    ligand=${tmp%.*}
    echo
    echo
    echo ANALISI
    echo Processing protein "$receptor"
    echo Processing ligand "$ligand"
    mkdir -p "${DOCKING_FOLDER}/${receptor}/${ligand}"
    touch "${DOCKING_FOLDER}/${receptor}/${ligand}/log.txt"
    vina --config "$g" --receptor "$p" --ligand "$f" --out "${DOCKING_FOLDER}/${receptor}/${ligand}/out.pdbqt" --log "${DOCKING_FOLDER}/${receptor}/${ligand}/log.txt"
  done
done