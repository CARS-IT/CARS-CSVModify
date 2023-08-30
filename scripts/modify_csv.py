#!/usr/bin/env python
##############################################################################################
# Script Name: modify_csv.py
# Description: This script modifies the csv file that contains the data of the hosts for
#              each sector; can be modified to add or remove columns. The Hostname, MAC and
#              IP columns are required and added automatically by the script.               
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
import pandas as pd
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ModifyCSV:
    """
    This class modifies the csv file that contains the data of the hosts for
    each sector; can be modified to add or remove columns. The Hostname, MAC and
    IP columns are required and added automatically by the script.
    
    In order to use this class, you must provide the input file and output file
    as arguments to the class. The input file is the file that will be modified
    and the output file is the file that will be created with the modifications.
    
    The columns attribute is a list of columns that will be added to the output
    file. The columns are added in the order that they are provided in the list.
    The default columns are ["Make", "Model", "Status", "Location", "SerialNumber"].
    To provide a different list of columns, you can provide a list of strings
    to the columns attribute.
    """

    input_file: Path = field(compare=False)
    output_file: Path = field(compare=False)

    _columns: list = field(default_factory=lambda: ["Make", "Model", "Status", "Location", "SerialNumber"], compare=False)
    _directory: Path = field(init=False, compare=False, repr=False)
    _temp_file: Path = field(init=False, compare=False, repr=False)
    _is_backup: bool = field(init=False, default=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        # Get the directory of the input file
        self._directory = self.input_file.parent

    def _prepare_file(self) -> None:
        """
        Prepares the input file for modification by creating a temporary file
        if the input file is a .bak file.
        """
        # Create a temporary file if the input file is a .bak file
        if self.input_file.suffix == ".bak":
            self._is_backup = True
            # Create a temporary file with the same name as the input file
            # but with the .csv extension
            self._temp_file = self._directory.joinpath("temp.csv")
            with open(self.input_file, "r") as file:
                with open(self._temp_file, "w") as temp_file:
                    for line in file:
                        temp_file.write(line)

    def _prepare_columns(self) -> None:
        """
        Prepares the columns for the output file by adding the required columns
        to the beginning and to the end of the list of columns.
        """
        # Add the required columns to the beginning of the list of columns
        self._columns = ["Hostname"] + self._columns
        self._columns.append("MAC")
        self._columns.append("IP")

    def _modify(self) -> None:
        
        try:
            # Read the input file into a dataframe
            if self._is_backup:
                file = self._temp_file
            else:
                file = self.input_file
            df = pd.read_csv(file)
        except (pd.errors.ParserError, FileNotFoundError):
            print(f"Error: The input file {file} is not a valid csv file.")
            return
        
        # Set the columns for the output file
        df = df[self._columns]
    
        # Forward fill missing values for selected columns
        columns_to_fill = self._columns.copy()
        columns_to_fill.remove('IP')
        df[columns_to_fill] = df[columns_to_fill].fillna(method="ffill")

        # Format the MAC addresses
        df["MAC"] = df["MAC"].str.replace(":", "", regex=False).str.lower()

        # Format the Hostnames
        df["Hostname"] = df["Hostname"].str.replace(".cars.aps.anl.gov", "", regex=False)
    
        # Convert the IP column to string for grouping and sorting
        df["IP"] = df["IP"].astype(str)

        # Sort the dataframe by IP and Hostname
        df.sort_values(by=["IP", "Hostname"], ascending=[True, False], inplace=True)

        # Drop duplicate IP entries and keep the latest Hostname
        df.drop_duplicates(subset=["IP"], keep="first", inplace=True)

        # Drop NaN IP entries
        df = df.drop(df[df["IP"] == "nan"].index)

        # Write the dataframe to the csv file. If the file already exists,
        # it will be overwritten.
        df.to_csv(self.output_file, index=False)

    def _cleanup(self) -> None:
        """
        Cleans up the temporary file created by the script,
        otherwise it moves the output file into a backup file
        and removes any old backup files.
        """ 
        if self._is_backup:
            # Remove the temp file if it exists
            self._directory.joinpath("temp.csv").unlink()
        else:
            # Move the original file to a backup file with the .bak extension
            # and remove any old backup files
            backup_file = self._directory.joinpath(f"{self.input_file}.bak")
            if backup_file.exists():
                backup_file.unlink()
            self.input_file.rename(backup_file)

    def start(self) -> None:
        """
        Initiates all the required actions to prepare everything, modify the
        input file, create the output file and cleanup.
        """
        try:
            self._prepare_file()
            self._prepare_columns()
            self._modify()
        finally:
            self._cleanup()


if __name__ == "__main__":

    # Provide example usage for the file in case if needed
    if len(sys.argv) != 3:
        print("Usage: python modify_csv.py <input_file> <output_file>")
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

    # Create an instance of the ModifyCSV class
    modify_csv = ModifyCSV(input_file=input_file, output_file=output_file)
    modify_csv.start()
