#!/bin/bash

# Sajid Nawaz Khan, released under the CC0 1.0 Universal license
# Last Updated: Sunday 25 April 2021
# For further information, visit https://github.com/ssnkhan/infrastructure-hunting/

read -r -p "Would you like to update the mihari database? This cannot be undone. [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	sqlite3	"mihari.db" '.read add_whois.sql'
	sqlite3	"mihari.db" '.read add_countries.sql'
	sqlite3 "mihari.db" '.read add_date.sql'
	sqlite3 "mihari.db" '.read add_pdns.sql'
	sqlite3 "mihari.db" '.read add_domains.sql'
	echo "Setup complete."
else
	echo "Setup aborted."
fi