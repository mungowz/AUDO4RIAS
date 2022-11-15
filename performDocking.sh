#! /bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOCKING_FOLDER="${SCRIPTPATH}/output/docking"
DATA_FOLDER="${SCRIPTPATH}/data"

showHelp() {
cat << EOF
Usage: ./performDocking -s <software> [-h]
Perform docking using a specific software

-h              Display help
-s              Choose a specific docking software in [Vina, GNINA]
    
EOF
}
DOCKING_SOFTWARE=""

while getopts "hs:" arg; do
    case "${arg}" in
        s)
            DOCKING_SOFTWARE=${OPTARG,,}
            ;;
        h|*)
            showHelp
            exit 0
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "$DOCKING_SOFTWARE" ]; then
    showHelp
    exit 0
fi
if [ "$DOCKING_SOFTWARE" != "vina" ] && [ "$DOCKING_SOFTWARE" != "gnina" ]; then
    echo "ERROR: Docking software specified is not supported!"
    exit 2
fi

for p in  ${DATA_FOLDER}/proteins/pdbqt/protein_*.pdbqt; do
    tmp=${p#*_}
    receptor=${tmp%.*}
    # mkdir -p "${DOCKING_FOLDER}/${receptor}"
    if [ "$DOCKING_SOFTWARE" = "vina" ]; then
        for g in  ${DATA_FOLDER}/proteins/gridbox/protein_*_grid.txt; do
            tmp=${g#*_}
            tmp=${tmp#*_}
            gridbox=${tmp%_*}
            if [ "$receptor" = "$gridbox" ]; then
            break
            fi
        done
    fi  

    for f in ${DATA_FOLDER}/ligands/pdbqt/ligand_*.pdbqt; do
        tmp=${f#*_}
        ligand=${tmp%.*}
        echo
        echo
        echo ANALISI
        echo Processing protein "$receptor"
        echo Processing ligand "$ligand"
        mkdir -p "${DOCKING_FOLDER}/${DOCKING_SOFTWARE}/${receptor}/${ligand}"
        if [ "$DOCKING_SOFTWARE" = "vina" ]; then
            touch "${DOCKING_FOLDER}/${DOCKING_SOFTWARE}/${receptor}/${ligand}/log.txt"
            vina --config "$g" --receptor "$p" --ligand "$f" --out "${DOCKING_FOLDER}/${DOCKING_SOFTWARE}/${receptor}/${ligand}/out.pdbqt" --log "${DOCKING_FOLDER}/${DOCKING_SOFTWARE}/${receptor}/${ligand}/log.txt"
        else
            gnina --receptor "$p" --ligand "$f" --autobox_ligand "$p" --out "${DOCKING_FOLDER}/${DOCKING_SOFTWARE}/${receptor}/${ligand}/out.pdbqt" --cnn_verbose 
        fi
    done
done
