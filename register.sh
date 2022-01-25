#!/bin/bash

for ROOM in "01" "02" "03"
do
    sudo prosodyctl register windows${ROOM} localhost password  
    sudo prosodyctl register blinds${ROOM} localhost password  
    sudo prosodyctl register floor_heating${ROOM} localhost password  
done

sudo prosodyctl register repo localhost password  
sudo prosodyctl register sensors localhost password
