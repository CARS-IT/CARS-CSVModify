#!/usr/bin/env python
##############################################################################################
# Script Name: csv_to_db.py
# Description: This script converts the csv file that contains the data of the hosts for
#              each sector to a table for MariaDB.
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
import json
import mariadb
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CSVToDB:
    csv_file: Path = field(compare=False)
    db_config_file: Path = field(compare=False)
    columns: list = field(default_factory=list, compare=False)

    _table_name: str = field(init=False, compare=False)

    def convert_csv_to_db_table(self) -> None:
        # Try to read the configuration file
        try:
            with open(self.db_config_file, "r") as f:
                db_config = json.load(f)
        except Exception as e:
            print(
                f"Error: Could not read the configuration file {self.db_config_file}."
            )

        # Try to connect to the database
        try:
            connection = mariadb.connect(**db_config)
            print(f"Connected to MariaDB Platform as user {db_config['user']}")
        except mariadb.Error as e:
            print(f"Error: Could not connect to MariaDB Platform: {e}")
            sys.exit(1)
        else:
            # Create a cursor object
            cursor = connection.cursor()

            # Create the table name
            self._table_name = self.csv_file.stem

            # Drop the table if it exists
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {self._table_name}")
            except mariadb.Error as e:
                print(f"Error: Could not drop the table {self._table_name}: {e}")
                sys.exit(1)

            # Create the table and add varchar(255) to each column
            try:
                create_table_query = f"CREATE TABLE {self._table_name} ({', '.join([f'{col} VARCHAR(255)' for col in self.columns])})"
                cursor.execute(create_table_query)

                # Add the data from the csv file to the table
                query = f"""
                LOAD DATA INFILE '{self.csv_file}'
                INTO TABLE {self._table_name}
                FIELDS TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                """
                cursor.execute(query)

                # Commit the changes
                connection.commit()
            except mariadb.Error as e:
                print(f"Error: Could not create the table {self._table_name}: {e}")
                sys.exit(1)
            else:
                print(f"Created the table {self._table_name}")

        finally:
            # Close the connection to the database
            connection.close()
