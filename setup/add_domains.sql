CREATE TABLE domains (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    pDNS varchar NOT NULL,
    fqdn varchar,
    subdomain varchar,
    domain varchar,
    tld varchar,
    UNIQUE(id ASC)
);