#! /bin/bash

# repository cannot be located as ADFRsuite subdir 
PR4_PATH=$(find "$(cd ..; pwd)"  -type f -name "prepare_receptor4.py")


if [ "$1" = "-v" ]; then
    VERBOSE=true
elif [ "$1" = "-h" ]; then
    echo "./replace_pr4.py [-v|-h]
            [-v]    verbose
            [-h]    help"
fi

if [ "$VERBOSE" = true ]; then
    echo "############ replace_pr4py.sh #############"
fi

# find dir that contains "prepare_receptor4.py"
# ADFRsuite must be located as Desktop subdir
if [ "$VERBOSE" = true ]; then
    echo "Searching for ADFRsuite Utilities24 directory..."
fi
ADFR_PR4=$(find "$HOME" -type d -name "Utilities24")

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
# set execution flag to "prepare_receptor4.py" 
if [ "$VERBOSE" = true ]; then
    echo "Setting execution flag..."
fi
FINAL_PATH="${ADFR_PR4}/prepare_receptor4.py"
chmod a+x "$FINAL_PATH"

if [ "$VERBOSE" = true ]; then
    echo "Set execution flag to "$FINAL_PATH""
    echo "###############   DONE   #################"
fi