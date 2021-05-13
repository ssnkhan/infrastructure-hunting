#!/usr/bin/python3
# Sajid Nawaz Khan, released under the CC0 1.0 Universal license
# Last Updated: Tuesday 23 March 2021
# For further information, visit https://github.com/ssnkhan/infrastructure-hunting/

import sqlite3
import subprocess
import requests
import time
import datetime


# PassiveTotal Configuration
username = ''
key = ''
auth = (username, key)
base_url = 'https://api.passivetotal.org'


def passivetotal_get(path, query):
    # Constrain pDNS resolutions to the previous 10 days
    start = datetime.date.fromordinal(datetime.date.today().toordinal()-10).strftime("%F")
    
    url = base_url + path
    data = {'query': query, 'start': start}
    
    response = requests.get(url, auth=auth, json=data)
    response = response.json()

    pdns = []
    if len(response['results']) > 0:
        for resolution in response['results']:
            pdns.append(resolution['resolve'])
        
        return pdns
    else:
        return ""


connect = sqlite3.connect('mihari.db')
mihari = connect.cursor()

results = mihari.execute('''
SELECT
    id,
    data
FROM artifacts
WHERE data_type = 'ip'
  AND asn IS NULL
ORDER BY
    id ASC;
''')

results = results.fetchall()

for row in results:
    key = row[0]
    ip = row[1]

    print (f"Querying {ip}.")
    
    # Perform the whois using the Team Cymru service
    getwhois = "whois -h whois.cymru.com ' -v " + str(ip) + "' | tail -1"
    whois = subprocess.Popen(getwhois, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
    
    # Populate a tuple with the results of the query
    whois = [x.strip() for x in whois.split('|')]

    tc_asn = whois[0]
    tc_asn_name = whois[6]
    tc_bgp_prefix = whois[2]
    tc_registry = whois[4]
    tc_country_code = whois[3]
    
    
    # Get pDNS
    resolutions = passivetotal_get('/v2/dns/passive', ip)
    
    # Update the table
    mihari.execute(f'''
        UPDATE artifacts
        SET asn = "{tc_asn}",
            asn_name = "{tc_asn_name}",
            bgp_prefix = "{tc_bgp_prefix}",
            registry = "{tc_registry}",
            country_code = '{tc_country_code}',
            pDNS = "{resolutions}"
        WHERE
            id = "{key}"
    ''')
    connect.commit()
    time.sleep(1)
else:
    if len(results) == 0:
        print ("No more records to update.")

# Save the database
connect.close()
if len(results) >= 1:
    print (f"{len(results):,} records successfully updated.")
    