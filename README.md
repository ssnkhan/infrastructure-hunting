# Zero to Hero: Proactive Infrastructure Hunting
by Sajid Nawaz Khan, _Cyber Threat Intelligence Analyst_.

This README is designed to support the above workshop which took place in May 2021. A copy of the presentation is available to defenders working within the financial sector. 

---

## System Requirements
Please ensure you have installed [VirtualBox](https://www.virtualbox.org) with the [Extension Pack](https://www.virtualbox.org/wiki/Downloads), followed by a virtual machine running x64 [Ubuntu 20.04 LTS](https://wiki.ubuntu.com/Releases). Ideally, the machine should be configured with at least 2GB of RAM.


## Installation
Detailed installation instructions are available on the [Mihari Wiki](https://github.com/ninoseki/mihari/wiki/Requirements-&-Installation). The code below is provided for convenience to help support the workshop, and is correct for version 2.3.0.


### Installing Dependencies
``` bash
# Core
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential gcc make perl dkms
sudo apt-get install git
sudo apt-get install sqlite3 libsqlite3-dev
sudo apt-get install ruby-full
sudo apt-get install python3-pip


# Artefact Enrichment
# Update PATH as necessary in /etc/environment
pip3 install requests
pip3 install tldextract


# For Data Analysis
pip3 install jupyter numpy pandas matplotlib seaborn
pip3 install tabulate
pip3 install datasette


# VS Code Plugins (Install VS Code via the Ubuntu Software app)
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension alexcvzz.vscode-sqlite
```

On a minimal install of Ubuntu, you may also need to install cURL and whois: `sudo apt-get install curl whois`. 

Additionally, you may also wish to clone a copy of this repository:  
`git clone https://github.com/ssnkhan/infrastructure-hunting.git`


### Installing Mihari
``` bash
# Can take around 5 minutes, please be patient
sudo gem install mihari
```

Post-installation, please configure API keys as detailed within the [Mihari Wiki](https://github.com/ninoseki/mihari/wiki/Configuration). 

In addition to supporting API key configuration via a YAML file, Mihari also supports configuration via environmental variables, e.g.,  `export SHODAN_API_KEY=YOUR_API_KEY` within your `queries.sh` file,  or by updating `.profile` or `/etc/environment`.


## Extending Mihari
### Updating `mihari.db`
Once a local `mihari.db` sqlite database has been instantiated, copy or move it to the `setup/` directory and run the `./setup.sh` script to update its database schema. This is necessary to use the enrichment scripts detailed below.


### Enriching Artefacts
These scripts are designed to enrich artefacts collected by Mihari with basic whois and passive DNS data.

| File | Description |
| --- | --- |
| `update_whois.py` | Implements the Team Cymru whois API to capture a host's ASN, ASN name, BGP prefix, registrar and country. Note that location data is self attested by the ASN, and may not be accurate. |
| `update_whois_dns.py` | Additionally implements the PassiveTotal API for passive DNS lookups associated with a host within the past ten days (API key required). |
| `update_domains.py` | Uses the `tldextract` library to distil a FQDN to its components (subdomain, domain and TLD). |


### Analysis
| File | Description |
| --- | --- |
| `Mihari.ipnb` | Jupyter notebook which allows SQL queries to be executed and loaded into a Pandas dataframe. |
| `Seaborn.ipnb` | Jupyter notebook which allows SQL queries to be executed and graphed as a Seaborn bar chart. |
| `Queries.md` | SQL queries to support analysis. Use the Jupyter notebooks above, or with Datasette. |


#### Datasette
Datasette offers a simple yet powerful way of reviewing and querying the Mihari database through your browser. Start the Datasette server with `datasette serve mihari.db -o`. Add basic chart generation with `pip3 install datasette-vega`.

---


### Backups
Run `backup.sh` manually or via a cronjob to backup the `mihari.db` sqlite database to the `backups` folder. Update your paths as necessary.


---


I'd love to hear your thoughts and feedback. Feel free to say hello on Twitter [@snkhan](https://twitter.com/snkhan?lang=en) or via [LinkedIn](https://uk.linkedin.com/in/sajidnawazkhan).


---

#cti #threatintelligence #blueteam #threathunting #shodan #censys
