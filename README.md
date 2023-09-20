# CARS-CSVModify

[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE) ![Python](https://img.shields.io/badge/python-v3.11-blue.svg?logo=python) ![MariaDB](https://img.shields.io/badge/MariaDB-v3:10.5.16--2-brown.svg?logo=mariadb)

CARS-CSVModify is used to modify existing .csv files with host information from CARS and set up the modifications as tables in MariaDB.

------------
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

------------
## Installation

Make sure all you install all the requirements for the project.

#### System Requirements

- MariaDB v3:10.5.16-2
- mariadb-connector-c-devel
- make

#### Python Requirements

- Python >= 3.10
- mariadb == 1.1.4
- pandas >= 2.1.0

#### Source

Download the GitHub repository and modify the Makefile in order to change the filepath for the input, the output and the db_config files.

```bash
git clone -b main https://github.com/skordaschristofanis/CARS-CSVModify.git
```

You can change the columns for the output file, but the MAC, IP and Hostname, host_id and Data columns are required. In order to modify the columns open the modify_csv.py file in the cars_csvmodify package and add or remove columns from the default_factory option of the columns variable.

#### Systemd Services

There is a timer (set to run every 5 minutes) and an associated service with this project. In order to use these you need to first copy the contents of the systemd folder to /etc/systemd/system and then enable both the service and the timer. 

Navigate to the project directory and run the following commands:

```bash
sudo cp systemd/* /etc/systemd/system/
sudo systemctl enable --now csv-modify.service
sudo systemctl enable --now csv-modify.timer
```

------------
## Usage

This repository contains a copy of the CARS-CSVModify directory, excluding any database configuration files. The database used is a MariaDB previously configured by LibreNMS. Both the LibreNMS and the CSV files contain information about the devices connected to the CARS network.

Besides the automated way of converting the CSV files (systemd) you can manually convert files. Navigate to the directory of the project and run the following commands.:

```bash
# The make default target will make the files for all sectors
make

# the make s13, s14, s15 for each sector
make s13
make s14
make s15
```

Make sure to take in account any modifications you made to the make file.

------------
## Contributing

All contributions to CARS-CSVModify are welcome! Here are some ways you can help:
- Report a bug by opening an [issue](https://github.com/skordaschristofanis/CARS-CSVModify/issues).
- Add new features, fix bugs or improve documentation by submitting a [pull request](https://github.com/skordaschristofanis/CARS-CSVModify/pulls).

Please adhere to the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) model when making your contributions! This means creating a new branch for each feature or bug fix, and submitting your changes as a pull request against the main branch. If you're not sure how to contribute, please open an issue and we'll be happy to help you out.

By contributing to CARS-CSVModify, you agree that your contributions will be licensed under the MIT License.

[back to top](#table-of-contents)

------------
## License

CARS-CSVModify is distributed under the MIT license. You should have received a [copy](LICENSE) of the MIT License along with this program. If not, see https://mit-license.org/ for additional details.

------------
#### [Christofanis Skordas](mailto:skordasc@uchicago.edu) - Last updated: 20-Sep-2023