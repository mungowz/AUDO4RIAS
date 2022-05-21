#! /bin/bash

# find dir that contains "prepare_receptor4.py"
path=$(find /home -type d -name "Utilities24")

# move our "prepare_receptor4.py" to dirpath
mv "prepare_receptor4.py" "$path"

# set execution flag to "prepare_receptor4.py" 
file="${path}/prepare_receptor4.py"
chmod a+x "$file"
