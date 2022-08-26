#! /bin/bash

if [ "$1" = "vina" ]; then
    chmod a+x vina_script.sh
    source vina_script.sh
elif [ "$1" = "gnina" ]; then
    chmod a+x gnina_script.sh
    source gnina_script.sh
elif [ "$1" = ""]; then
    echo "No docking software specified!"
else
    echo "Docking software specified is not supported!"
fi