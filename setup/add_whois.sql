-- Update the existing artefacts table with whois columns

PRAGMA foreign_keys = off;

BEGIN;

CREATE TABLE _artifacts_new (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT
  , data varchar NOT NULL
  , data_type varchar NOT NULL
  , alert_id bigint
  , created_at datetime(6) NOT NULL
  , updated_at datetime(6) NOT NULL
  , asn integer
  , asn_name varchar
  , bgp_prefix varchar
  , registry varchar
  , country_code varchar
  , FOREIGN KEY(alert_id) REFERENCES alerts(id) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION
);

INSERT INTO _artifacts_new (
    id
  , data
  , data_type
  , alert_id
  , created_at
  , updated_at
)
SELECT
    id
  , data
  , data_type
  , alert_id
  , created_at
  , updated_at
FROM artifacts;

DROP TABLE artifacts;

PRAGMA legacy_alter_table = ON;

ALTER TABLE _artifacts_new RENAME TO artifacts;

PRAGMA legacy_alter_table = off;

CREATE INDEX index_artifacts_on_alert_id ON artifacts(alert_id COLLATE BINARY ASC);

COMMIT;

PRAGMA foreign_keys = ON;