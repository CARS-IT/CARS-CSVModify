#!/usr/bin/env python
##############################################################################################
# Script Name: CARS-CSVModify.py
# Description: This script modifies the csv file that contains the data of the hosts for
#              each sector and adds the data of the hosts to a table for MariaDB.
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

import sys
from pathlib import Path

from cars_csvmodify import ModifyCSV, CSVToDB


def main(input_file: Path, output_file: Path, db_config_file: Path) -> None:
    """Runs the ModifyCSV and CSVToDB."""

    # Create an instance of the ModifyCSV class
    modify_csv = ModifyCSV(input_file=input_file, output_file=output_file)
    modify_csv.start()

    # Create an instance of the CSVToDB class
    csv_to_db = CSVToDB(csv_file=output_file, db_config_file=db_config_file, columns=modify_csv.columns)
    csv_to_db.convert_csv_to_db_table()


if __name__ == "__main__":

    # Provide example usage for the file in case if needed
    if len(sys.argv) != 4:
        print("Usage: python CARS-CSVModify.py <input_file> <output_file> <db_config_file>")
        sys.exit(1)

    # Check for proper input filename
    input_file = Path(sys.argv[1]).resolve()
    if not input_file.exists():
        print(f"Error: The input file {input_file} does not exist.")
        sys.exit(1)

    # Check for proper output filename
    output_file = Path(sys.argv[2]).resolve()
    if not output_file.parent.exists():
        print(f"Error: The output directory {output_file} does not exist.")
        sys.exit(1)

    # Check for proper database configuration filename
    db_config_file = Path(sys.argv[3]).resolve()
    if not db_config_file.exists():
        print(f"Error: The configuration file {db_config_file} does not exist.")
        sys.exit(1)

    main(input_file=input_file, output_file=output_file, db_config_file=db_config_file)
