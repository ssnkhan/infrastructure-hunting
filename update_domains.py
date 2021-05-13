#!/usr/bin/python3
# Sajid Nawaz Khan, released under the CC0 1.0 Universal license
# Last Updated: Sunday 28 March 2021
# For further information, visit https://github.com/ssnkhan/infrastructure-hunting/


import sqlite3
import tldextract
from collections import Counter
import operator


# Fetch rows with pDNS data
connect = sqlite3.connect('mihari.db')
mihari = connect.cursor()


# Purge all entries in the current table
mihari.execute(f'''
    DELETE FROM domains;
''')
connect.commit()

mihari.execute(f'''
    DELETE FROM sqlite_sequence WHERE name='domains';
''')
connect.commit()


results = mihari.execute('''
SELECT
        strftime("%Y-%m-%d", alerts.created_at) AS "Date",
        alerts.title AS "Alert Type",
        artifacts.pDNS AS "pDNS"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
    AND pDNS IS NOT ""
    AND pDNS IS NOT NULL
ORDER BY
        "Date" DESC;
''')

results = results.fetchall()


for row in results:
    type = row[1]
    oDNS = row[2]
    
    oDNS = str(oDNS)
    oDNS = oDNS.replace('"', '')


    # Clean up the existing Python List
    pDNS = oDNS
    pDNS = pDNS.replace("[", "")
    pDNS = pDNS.replace("]", "")
    pDNS = pDNS.replace('"', "")
    pDNS = pDNS.replace("'", '')
    pDNS = pDNS.split(", ")


    # Create a list containing elements of the domain
    for fqdn in pDNS:
        ofqdn = fqdn
        fqdn = tldextract.extract(fqdn)
        
        subdomain = fqdn.subdomain
        domain = fqdn.domain
        tld = fqdn.suffix
        
    
        # Update the table
        mihari.execute(f'''
            INSERT INTO domains (pDNS, fqdn, subdomain, domain, tld)
            VALUES ("{oDNS}",
            "{ofqdn}",
            "{subdomain}",
            "{domain}",
            "{tld}");
        ''')
        connect.commit()
    

# Save the database
connect.close()
if len(results) >= 1:
    print (f"{len(results):,} rows successfully analysed.")