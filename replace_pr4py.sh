#! /bin/bash
path=$(find /home -type d -name "Utilities24")
mv "prepare_receptor4.py" "$path"
file="${path}/prepare_receptor4.py"
chmod a+x "$file"
