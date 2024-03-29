#! /bin/bash

# repository cannot be located as ADFRsuite subdir 
PR4_PATH=$(find "$(pwd)"  -type f -name "prepare_receptor4.py")


if [ "$1" = "-v" ]; then
    VERBOSE=true
elif [ "$1" = "-h" ]; then
    echo "./replacePrepareReceptor4.sh [-v|-h]
            [-v]    verbose
            [-h]    help"
    exit 1

fi

if [ "$VERBOSE" = true ]; then
    echo "############ replacePrepareReceptor4.sh #############"
fi

# find dir that contains "prepare_receptor4.py"
# ADFRsuite must be located as Desktop subdir
if [ "$VERBOSE" = true ]; then
    echo "Searching for ADFRsuite Utilities24 directory..."
fi
ADFR_FOLDER=$(find "$HOME" -type d -name "ADFRsuite-1.0")
ADFR_PR4=$(find "$ADFR_FOLDER" -type d -name "Utilities24")

if [ "$VERBOSE" = true ]; then
    echo "FOUND: "$ADFR_PR4""
fi

# move our "prepare_receptor4.py" to dirpath
if [ "$VERBOSE" = true ]; then
    echo "Copying files..."
fi
cp "$PR4_PATH" "$ADFR_PR4"

if [ "$VERBOSE" = true ]; then
    echo "Copied "$PR4_PATH" into "$ADFR_PR4""
fi

# set binaries to PATH, now can use prepare_receptor and prepare_ligand
# export PATH="${ADFR}/bin:$PATH"
# source $HOME/.bashrc

# set execution flag to "prepare_receptor4.py" 
if [ "$VERBOSE" = true ]; then
    echo "Setting execution flag..."
fi
FINAL_PATH="${ADFR_PR4}/prepare_receptor4.py"
chmod a+x "$FINAL_PATH"

if [ "$VERBOSE" = true ]; then
    echo "Set execution flag to "$FINAL_PATH""
fi
echo "###############   DONE   #################"
