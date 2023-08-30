#!/bin/bash
##############################################################################################
# Script Name: run.sh 
# Description: This script is used to activate the anacoda environment and
#              run the main python script.
#
# License: MIT License
#
# CARS-CSVModify
#
# Copyright (c) 2023 Christofanis Skordas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################################

# Source the conda.sh file
source /opt/anaconda3/etc/profile.d/conda.sh

# Activate the anacoda environment
conda activate CSVModifyENV

# Function that runs the python scripts and has arguments for input file, output file and the
# db_config file
function run {
    input_file=$1
    output_file=$2
    db_config=$3

    python CARS-CSVModify.py $input_file $output_file $db_config
}

# Chek if the user provided the input file, output file and the db_config file
if [ $# -eq 3 ]; then
    run $1 $2 $3
else
    echo "Please provide the input file, output file and the db_config file"
    exit 1
fi
