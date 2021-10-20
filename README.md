# Buncher
Service for getting samples from the database with certain conditions.

## Installation and starting
```bash
git clone https://github.com/FrankensteinPillow/buncher.git
cd buncher
python -m pip install -r requirements.txt

# start
python buncher/app.py
```
Before starting you can specify environment variables `db_url` and `servicese_port` in order to start the service with the appropriate settings. Or you can specify those settings in `config.py`.

For the service to work correctly, the specified database must contain the `dataset` table. Also, this table should contain the following columns: `date`, `channel`, `country`, `os`, `impressions`, `clicks`, `installs`, `spend`, `revenue`.

## Usage examples
1) Show the number of impressions and clicks that occurred before the 19 of May 2017, broken down by channel and country, sorted by clicks in descending order.
```bash
curl --location --request POST '127.0.0.1:3520/get_data' \
--header 'Content-Type: application/json' \
--data-raw '{
    "from_date": "inf",
    "to_date": "2017-05-19",
        "columns": [
        "channel",
        "country",
        "impressions",
        "clicks"
    ],
    "order_by": [
        "clicks",
        "desc"
    ],
    "group_by": [
        "channel",
        "country"
    ]
}'
```
Out:
```json
{
    "msg": "Ok",
    "status_code": 200,
    "data": [
        {
            "channel": "adcolony",
            "country": "US",
            "clicks": 2479,
            "impressions": 101292
        },
        {
            "channel": "apple_search_ads",
            "country": "US",
            "clicks": 2137,
            "impressions": 67560
        },
        {
            "channel": "vungle",
            "country": "GB",
            "clicks": 1766,
            "impressions": 50614
        },
        {
            "channel": "unityads",
            "country": "US",
            "clicks": 1441,
            "impressions": 40164
        },
...
```
2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
```bash
curl --location --request POST '127.0.0.1:3520/get_data' \
--header 'Content-Type: application/json' \
--data-raw '{
    "from_date": "2017-05-01",
    "to_date": "2017-05-31",
    "columns": [
        "date",
        "installs"
    ],
    "filters": [
        ["os", "ios"]
    ],
    "order_by": "date",
    "group_by": [
        "date"
    ]
}'
```
Out:
```json
{
    "msg": "Ok",
    "status_code": 200,
    "data": [
        {
            "date": "2017-05-17",
            "installs": 755
        },
        {
            "date": "2017-05-18",
            "installs": 765
        },
        {
            "date": "2017-05-19",
            "installs": 745
        },
        {
            "date": "2017-05-20",
            "installs": 816
        },
        {
            "date": "2017-05-21",
            "installs": 751
        },
        {
            "date": "2017-05-22",
            "installs": 781
        },
        {
            "date": "2017-05-23",
            "installs": 813
        },
        {
            "date": "2017-05-24",
            "installs": 789
        },
        {
            "date": "2017-05-25",
            "installs": 875
        },
        {
            "date": "2017-05-26",
            "installs": 725
        },
        {
            "date": "2017-05-27",
            "installs": 712
        },
        {
            "date": "2017-05-28",
            "installs": 664
        },
        {
            "date": "2017-05-29",
            "installs": 752
        },
        {
            "date": "2017-05-30",
            "installs": 762
        },
        {
            "date": "2017-05-31",
            "installs": 685
        }
    ]
}
```
3) Show revenue, earned on May 17, 2017 in US, broken down by operating system and sorted by revenue in descending order.
```bash
curl --location --request POST '127.0.0.1:3520/get_data' \
--header 'Content-Type: application/json' \
--data-raw '{
    "from_date": "2017-05-17",
    "to_date": "2017-05-17",
    "columns": [
        "date",
        "os",
        "revenue"
    ],
    "filters": [
        ["country", "US"]
    ],
    "order_by": ["revenue", "desc"],
    "group_by": [
        "os"
    ]
}'
```
Out:
```json
{
    "msg": "Ok",
    "status_code": 200,
    "data": [
        {
            "date": "2017-05-17",
            "os": "ios",
            "revenue": 1138.4799999999998
        },
        {
            "date": "2017-05-17",
            "os": "android",
            "revenue": 880.5799999999999
        }
    ]
}
```
4) Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.
```bash
curl --location --request POST '127.0.0.1:3520/get_data' \
--header 'Content-Type: application/json' \
--data-raw '{
    "columns": [
        "channel",
        "CPI",
        "spend"
    ],
    "filters": [
        ["country", "CA"]
    ],
    "order_by": ["CPI", "desc"],
    "group_by": [
        "channel"
    ]
}'
```
Out:
```json
{
    "msg": "Ok",
    "status_code": 200,
    "data": [
        {
            "channel": "facebook",
            "spend": 1164.0,
            "CPI": 2.0748663101604277
        },
        {
            "channel": "chartboost",
            "spend": 1274.0,
            "CPI": 2.0
        },
        {
            "channel": "unityads",
            "spend": 2642.0,
            "CPI": 2.0
        },
        {
            "channel": "google",
            "spend": 999.9000000000004,
            "CPI": 1.7419860627177708
        }
    ]
}
```