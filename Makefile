##############################################################################################
# Makefile for configuring the sector 13, 14 and 15 hosts.csv files, and for
# updating the tables on MariaDB.
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

# Set the default target
.DEFAULT_GOAL := all

# Target for sector 13
s13:
	-bash run.sh "/cars5/users/CARS-IT/Grafana/IHW/S13/hosts.csv" "/cars5/users/CARS-IT/Grafana/IHW/S13/13ihw.csv" "/cars5/users/CARS-IT/Grafana/db_config.json"

# Target for sector 14
s14:
	-bash run.sh "/cars5/users/CARS-IT/Grafana/IHW/S14/hosts.csv" "/cars5/users/CARS-IT/Grafana/IHW/S14/14ihw.csv" "/cars5/users/CARS-IT/Grafana/db_config.json"

# Target for sector 15
s15:
	-bash run.sh "/cars5/users/CARS-IT/Grafana/IHW/S15/hosts.csv" "/cars5/users/CARS-IT/Grafana/IHW/S15/15ihw.csv" "/cars5/users/CARS-IT/Grafana/db_config.json"

# Default target for all sectors
all: s13 s14 s15
	@echo "All sectors configured successfully"

# Usage information for the available targets
help:
	@echo "Usage: make [help]"
	@echo " help    - Show this help message"
	@echo " all     - Configure all sectors"
	@echo " s13     - Configure sector 13"
	@echo " s14     - Configure sector 14"
	@echo " s15     - Configure sector 15"
