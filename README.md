# Business case script EONET

## A. Project description & usage

The python script available at this link does the following task:

1. Sets up a SQLite database to hold the data

2. Downloads the event data (i.e. wildfires, severe storms, and landslides) from the EONET API for the last month

3. Saves the data to the database

4. Compiles the data into an excel spreadsheet

5. Emails the spreadsheet to an email address specified either as a command-line parameter.

## B. Installation

In order to be run the script:

* The the below python libraries have to be installed

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


* The email address of the recepient has te be specified in the variable "email_recepient"


## C. Limitations 



## D. To go further



## E. Credits
