# Business case script EONET

## A. Project description & usage

The script is available here (.py and jupyter file): 

* https://github.com/radium0022/business_case_EONET/blob/master/Business%2Bcase%2BMaple%2Bcroft%2B-%2Bscript.py 

* https://github.com/radium0022/business_case_EONET/blob/master/Business%2Bcase%2BMaple%2Bcroft%2B-%2Bscript.ipynb

It does the following task:

1. Sets up a SQLite database to hold the data

2. Downloads the event data (i.e. wildfires, severe storms, and landslides) from the EONET API for the last month (i.e. events terminated during the last month). 

3. Saves the data to the database

4. Compiles the data into an excel spreadsheet

5. Emails the spreadsheet to an email address specified either as a command-line parameter.

## B. Installation

In order to be run the script, you need:

* Python 3 or later

* The below libraries have to be installed

```
import json

import requests

import sqlite3

import pandas as pd

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

import smtplib,ssl

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email.mime.text import MIMEText

from email.utils import formatdate

from email import encoders
```

* The email address of the recipient has to be specified in the variable "email_recepient"


## C. Critique & limitations

* It has been difficult to transform the data form the EONET API as the JSON file was containing nested dictionaries and list. It needed me some manual work and cleaning to transform the data into a list of list (see point 2.3 in the script), and hence to upload it into the SQLite database.

* The final output only take into consideration terminated events. In other words, these events have started in October (see column date in the database) and are finished now (see column closed in the database). It might also be of interest to  monitor open events in another report, on a weekly basis for example.

* This script is only working if the sender has a gmail account. It might be useful to create a script working with other kind of email account. 

* The transfer of the API data to the SQLite database might be risky (see point 3 in the script). In case the data structure in the API is changing, a data quality check should be run in order to verify that the output is valid. 

## D. To go further

* If I had more time, I would use functions and or class to give more structure to the code and to make it easier to use (e.g. for data extraction from the API). 

* I would create additional insights in the report (e.g. plotting the events on a map with basemap or folium using the coordinates)

* I would automate the running of the script on a monthly basis, for example using the software Cron in Linux.
