# Mihari SQL Queries

Use with the sqlite CLI, the `Mihari.ipnb` Jupyter Notebook, Datasette or when developing Grafana dashboards.


---


### Date Filters
Appended after the `FROM` or `INNER JOIN` statements, can be used to constrain results to a specific time period.


#### By Today
``` sql
WHERE date(artifacts.created_at) = date('now')
```


#### Between a Date Range
``` sql
SELECT
    alerts.title AS "Alert Type",
    COUNT(*) AS "Total"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
WHERE date(artifacts.created_at) >= "2021-01-01"
  AND date(artifacts.created_at) <= "2021-04-01"
GROUP BY
    "Alert Type"
ORDER BY
    "Total" DESC,
    lower("Alert Type") ASC
```


#### _n_ Days Ago
``` sql
WHERE date(artifacts.created_at) = date('now', '-7 day')
```

#### _n_ Months Ago
``` sql
WHERE date(artifacts.created_at) = date('now', '-1 month')
```


#### _n_ Years Ago
``` sql
WHERE date(artifacts.created_at) = date('now', '-1 year')
```

---


## Queries

### Artefacts

#### C2s and Corresponding IPs / URLs by Date
``` sql
SELECT
    strftime("%Y-%m-%d", alerts.created_at) AS "Date",
    alerts.title AS "Alert Type",
    artifacts.data AS "IP"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
ORDER BY
    "Date" DESC
```


#### C2s with pDNS by Date
``` sql
SELECT
    strftime("%Y-%m-%d", alerts.created_at) AS "Date",
    alerts.title AS "Alert Type",
    artifacts.data AS "IP",
    artifacts.pDNS AS "pDNS, Last 10 Days"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
WHERE pDNS IS NOT ""
  AND pDNS IS NOT NULL
ORDER BY
    "Date" DESC
```


#### Phishing Alerts by Date
``` sql
SELECT
    strftime("%Y-%m-%d", alerts.created_at) AS "Date",
    alerts.title AS "Alert Type",
    data AS "Website"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
WHERE data_type = "url"
ORDER BY
    "Date" DESC
```


---


### Insights
#### Total Alerts by Date
``` sql
SELECT
    strftime("%Y-%m-%d", created_at) AS "Date",
    count(strftime("%Y-%m-%d", created_at)) AS "Total"
FROM artifacts
GROUP BY
    "Date"
ORDER BY
    "Date" ASC
```


#### Total Alerts by Month
```sql
SELECT
    strftime("%Y-%m", created_at) AS "Month",
    count(strftime("%Y-%m", created_at)) AS "Count"
FROM artifacts
GROUP BY
    "Month"
ORDER BY
    "Month" ASC
```


#### Total Alerts by Year
``` sql
SELECT
    strftime("%Y", created_at) AS "Year",
    count(strftime("%m", created_at)) AS "Count"
FROM artifacts
GROUP BY
    "Year"
ORDER BY
    "Year" ASC
```


#### Total Alerts by Day of Week
``` sql
SELECT
    day AS "Day of Week",
    count(*) AS "Total"
FROM artifacts
INNER JOIN date ON date.day_id = strftime("%w", created_at)
GROUP BY
    "Day of Week"
ORDER BY
    date.sorder ASC
```


#### Totals Alerts by Tag
``` sql
SELECT
    name AS "Tag",
    count(*) AS "Total"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
INNER JOIN taggings ON taggings.alert_id = alerts.id
INNER JOIN tags ON tags.id = taggings.tag_id
GROUP BY
    "Tag"
ORDER BY
    "Total" DESC
```


#### Total Alerts by Detection Rule
``` sql
SELECT
    alerts.title AS "Alert Type",
    count(*) AS "Total"
FROM artifacts
INNER JOIN alerts ON alerts.id = artifacts.alert_id
GROUP BY
    "Type"
ORDER BY
    "Total" DESC
```


#### Total Rules per Detection Rule
``` sql
SELECT
    title AS "Alert Type",
    count(description) AS "Total Rules"
FROM (
    SELECT DISTINCT
           title,
           description
    FROM alerts)
GROUP BY
    "Alert Type"
ORDER BY
    lower("Alert Type") ASC
```


#### Totals by Country
``` sql
SELECT
    countries.name AS "Country",
    count(*) AS "Total"
FROM artifacts
INNER JOIN countries ON countries."alpha-2" = artifacts.country_code
GROUP BY
    country_code
ORDER BY
    "Total" DESC,
    "Country" ASC
```


#### Totals by Region
``` sql
SELECT
    countries.region AS "Region",
    count(*) AS "Total"
FROM artifacts
INNER JOIN countries ON countries."alpha-2" = artifacts.country_code
GROUP BY
    "Region"
ORDER BY
    "Total" DESC,
    "Region" ASC
```


#### Totals by Sub Region
``` sql
SELECT
    "sub-region" AS "Sub Region",
    count(*) AS "Total"
FROM artifacts
INNER JOIN countries ON countries."alpha-2" = artifacts.country_code
GROUP BY
    "Sub Region"
ORDER BY
    "Total" DESC,
	"Sub Region" ASC
```


#### Totals by ASN
``` sql
SELECT
    asn AS "ASN",
    asn_name AS "ASN Name",
    count(*) AS "Total"
FROM artifacts
GROUP BY
    "ASN"
ORDER BY
    "Total" DESC,
    "ASN" ASC
```


#### Average Alerts
``` sql
SELECT
    round(avg(count)) AS "Average"
FROM (
       SELECT
           strftime("%Y-%m-%d", created_at) AS "Day",
           count(strftime("%Y-%m-%d", created_at)) AS "Count"
       FROM artifacts
       GROUP BY
           "Day")
```


#### Average Alerts over _n_ Days
``` sql
SELECT
    round(avg(count)) AS "Average"
FROM (
       SELECT
           strftime("%Y-%m-%d", created_at) AS "Day",
           count(strftime("%Y-%m-%d", created_at)) AS "Count"
       FROM artifacts
       WHERE date(artifacts.created_at) = date('now', '-7 day')
       GROUP BY
           "Day")
```


#### Totals by TLD
``` sql
SELECT
    tld AS "TLD",
    count(*) AS "Total"
FROM domains
GROUP BY
    "TLD"
ORDER BY
    "Total" DESC,
    "TLD" ASC
```


#### Delta From Previous Day
``` sql
SELECT
    strftime("%Y-%m-%d", created_at) AS "Date",
    count(strftime("%Y-%m-%d", created_at)) AS "Total",
    count(*) - LAG(count(strftime("%Y-%m-%d", created_at)), 1, 0)
    OVER (
           PARTITION BY "Date"
           ORDER BY
               "Total"
         ) AS "Δ"
FROM artifacts
GROUP BY
    "Date"
ORDER BY
    "Date" DESC
```


#### Rule Counts per Alert Type
``` sql
SELECT
    title AS "Alert Type",
    count(description) AS "Rules"
FROM (
    SELECT DISTINCT
           title,
           description
    FROM alerts)
GROUP BY
    "Alert"
ORDER BY
    "Alert" ASC
```


---


### API / Providers

#### Detections by Provider
Helpful in understanding reliance on specific data sources.
``` sql
SELECT
    source AS "Provider",
    count(*) AS "Total"
FROM alerts
INNER JOIN artifacts ON artifacts.alert_id = alerts.id
GROUP BY
    "Provider"
ORDER BY
    "Provider" ASC
```


#### Days Since Last Alert by Provider
Helpful in detecting API health concerns — including API quota exhaustion, and staleness in provider data.
``` sql
SELECT
    "Provider",
    "Last Observed",
    round(julianday(date("now")) - julianday("Last Observed")) AS "Days Since Last Alert"
FROM (
       SELECT
           source AS "Provider",
           strftime("%Y-%m-%d", artifacts.created_at) AS "Last Observed"
       FROM alerts
       INNER JOIN artifacts ON artifacts.alert_id = alerts.id
       ORDER BY
           "Last Observed" DESC)
GROUP BY
    "Provider"
ORDER BY
    "Provider" ASC
```