#!/usr/bin/env python
##############################################################################################
# Script Name: modify_csv.py
# Description: This script modifies the csv file that contains the data of the hosts for
#              each sector; can be modified to add or remove columns. The Hostname(Data), MAC
#              and IP columns are required and added automatically by the script.
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

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ModifyCSV:
    """
    This class modifies the csv file that contains the data of the hosts for
    each sector; can be modified to add or remove columns. The Hostname, Data, MAC
    IP and host_id columns are required and added automatically by the script.

    In order to use this class, you must provide the input file and output file
    as arguments to the class. The input file is the file that will be modified
    and the output file is the file that will be created with the modifications.

    The columns attribute is a list of columns that will be added to the output
    file. The columns are added in the order that they are provided in the list.
    The default columns are ["SerialNumber", "Make", "Model", "Status", "Location"].
    To provide a different list of columns, you can provide a list of strings
    to the columns attribute.
    """

    input_file: Path = field(compare=False)
    output_file: Path = field(compare=False)

    columns: list = field(
        init=False,
        default_factory=lambda: ["SerialNumber", "Make", "Model", "Status", "Location"], 
        compare=False,
    )

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
        to the beginning of the list of columns.
        """
        # Add the required columns to the beginning of the list of columns
        self.columns = ["Hostname", "Data", "host_id", "MAC", "IP"] + self.columns

    def _modify(self) -> None:
        try:
            # Read the input file into a dataframe
            if self._is_backup:
                file = self._temp_file
            else:
                file = self.input_file
            hosts_df = pd.read_csv(file)
        except (pd.errors.ParserError, FileNotFoundError):
            print(f"Error: The input file {file} is not a valid csv file.")
            return

        # Set the columns for the output file
        hosts_df = hosts_df[self.columns]

        # Set some variables to keep track of the current hostname and the device
        current_hostname = None
        is_new_device = True

        # Create variables for each column that will be used to fill in empty values dynamically
        for column in self.columns:
            if column not in ["Hostname", "Data", "host_id", "MAC", "IP"]:
                object.__setattr__(self, "current_" + column.lower(), None)

        # Iterate through the rows of the dataframe
        for i, row in hosts_df.iterrows():
            
            # Get the hostname from the row
            hostname = row["Hostname"]

            if pd.isna(hostname):
                # If the hostname is empty, use the current hostname
                hostname = current_hostname
                
                # Set the is_new_device variable to False since the hostname is empty
                is_new_device = False

                # Fill in the empty hostname
                hosts_df.at[i, "Hostname"] = hostname
            else:
                # If the hostname changes, update the current hostname and set the is_new_device variable to True
                current_hostname = hostname
                is_new_device = True

            # Iterate through the columns of the row for each column that will be used to fill in empty values dynamically
            for column in self.columns:
                
                if column not in ["Hostname", "Data", "host_id", "MAC", "IP"]:
                    
                    # Get the value of the row for each column
                    column_value = row[column]

                    if pd.isna(column_value) and not is_new_device:
                        # If the value is empty, use the current value
                        column_value = object.__getattribute__(self, "current_" + column.lower())
                        
                        # Fill in the empty value
                        hosts_df.at[i, column] = column_value
                    else:
                        if is_new_device:
                            # If the value changes, update the current value
                            object.__setattr__(self, "current_" + column.lower(), column_value) 

        # Shift the "MAC" and "host_id" columns down by one row before dropping the duplicate IP entries
        hosts_df["MAC"] = hosts_df["MAC"].shift(1)
        hosts_df["host_id"] = hosts_df["host_id"].shift(1)
        
        # Shift the Data row up by one row before dropping the duplicate IP entries
        hosts_df["Data"] = hosts_df["Data"].shift(-1)

        # Drop the rows with duplicate IP entries, keeping the first entry
        hosts_df.drop_duplicates(subset=["IP"], keep="first", inplace=True)

        # Drop rows with empty IP entries
        hosts_df.dropna(subset=["IP"], inplace=True)

        # Format the Data and the Hostname columns
        hosts_df[["Data", "Hostname"]] = hosts_df[["Data", "Hostname"]].apply(lambda x: x.str.replace(".cars.aps.anl.gov", "", regex=False))
        hosts_df[["Data", "Hostname"]] = hosts_df[["Data", "Hostname"]].apply(lambda x: x.str.replace(".xray.aps.anl.gov", "", regex=False))

        # Format the host_id column
        hosts_df["host_id"] = hosts_df["host_id"].astype(str)
        hosts_df["host_id"] = hosts_df["host_id"].str.replace(".0", "") 

        # Format the MAC addresses
        hosts_df["MAC"] = hosts_df["MAC"].str.replace(":", "", regex=False).str.lower()

        # Write the dataframe to the csv file. If the file already exists,
        # it will be overwritten.
        hosts_df.to_csv(self.output_file, index=False)

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
