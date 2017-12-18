
# coding: utf-8

# ## Guidelines

# The task involves reading data from an API, saving to a relational database, and compiling the results into a spreadsheet. The API we will be using is the EONET API from NASA: https://eonet.sci.gsfc.nasa.gov/ The events we would like to pull from here are wildfires, severe storms, and landslides from the past month.
#  
# The deliverable for this project is a Python script (or set of scripts) that does the following:
#  
# 1. Sets up a database to hold the event data
# 2. Downloads the event data from the API
# 3. Saves the data to the database
# 4. Compiles the data into a spreadsheet
# 5. Emails the spreadsheet to an email address specified either as a command-line parameter or by configuration

# ## Input 

# In[1]:

email_recepient = 'jb.vanderstraeten@gmail.com'


# # 0. Import libraries

# In[2]:

import json
import requests
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# # 1. Sets up a database to hold the event data

# ## 1.1 Creation SQLite database

# In[3]:

# Creating and connecting to the database file
conn = sqlite3.connect('EONET_db.sqlite')
c = conn.cursor()

# Creating a new SQLite table

c.execute('''DROP TABLE eonet_data''')
c.execute('''
CREATE TABLE eonet_data 
(event_id text, 
 event_title text,
 event_description text,
 event_link text,
 closed text,
 category_id integer,
 category_title text,
 source_id text,
 source_url text,
 date text,
 geometry_type text,
 coordinates text
 )
 ''')

# Committing changes
conn.commit()


# # 2. Downloads the event data from the API

# ## 2.1 Connect to the EONET API & check connection status

# In[4]:

# Define API parameters. Rational of 60 days parameter is to reduce size of the sample. 
parameters = {'status':'closed','days':'60'}

# Connection to API and get data
fires = requests.get('https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/8',parameters)
storms = requests.get('https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/10',parameters)
landslides = requests.get('https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/14',parameters)

# Verifying connection status
print(fires, storms, landslides)


# ## 2.2 Define date last month

# In[10]:

fulldate_last_month = datetime.now() - relativedelta(months=1) 
last_month = fulldate_last_month.strftime("%Y-%m")
print(last_month)
last_month = '2017-10'


# ## 2.3 Data extraction and cleaning 

# # 3. Saves the data to the database & select october events
# 

# In[14]:

# Json file dictionnary keys
events_keys = ['id','title','description','link','closed']
categories_keys = ['id','title']
sources_keys = ['id','url']
others_keys = ['date','type','coordinates']

# Extract data from API to list of list

all_incidents =[] 

for i in fires,storms,landslides:
    data = i.json()
    print(data)
      
    for z in range(0,len(data['events'])):
        incident_data = []
        
        for i in events_keys:
            events = data['events'][z][i]
            incident_data.append(events) 
        
        for i in categories_keys:
            categories_data = data['events'][z]['categories'][0][i]
            incident_data.append(categories_data) 
        
        for i in sources_keys:
            sources_data = data['events'][z]['sources'][0][i]
            incident_data.append(sources_data)
        
        for i in others_keys:
            others_data = data['events'][z]['geometries'][0][i]
            if i == 'coordinates':
                others_data = str(others_data)
            incident_data.append(others_data)
        
        # Filter data of last 60 days on last month
        if last_month in incident_data[9]:
            all_incidents.append(incident_data)


# In[12]:

# Transfer data to SQLite database
for i in all_incidents:
    c.execute("INSERT INTO eonet_data VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (i))


# In[13]:

# Read table in pandas and data cleaning
df = pd.read_sql_query("SELECT * from eonet_data", conn)

for i in ['closed','date']:
    df[i] = df[i].replace(to_replace =['T','Z'],value = ' ', regex=True)

# Visualisation of table
df.head(len(all_incidents))


# # 4. Compiles the data into a spreadsheet

# In[ ]:

# Create a Pandas Excel writer using XlsxWriter as the engine
excel_file_name = 'EONET_data_%s.xlsx' %last_month
writer = pd.ExcelWriter(excel_file_name, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object
df.to_excel(writer, sheet_name='event_data')
workbook  = writer.book

# Close the Pandas Excel writer and output the Excel file.
writer.save()


# # 5. Emails the spreadsheet to an email address specified either as a command-line parameter or by configuration

# In[ ]:

import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_mail(send_from,send_to,subject,text,files,server,port,username='',password='',isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(excel_file_name, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="EONET_data_%s.xlsx"' %last_month )
    msg.attach(part)

    #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
    #SSL connection only working on Python 3+
    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    
send_mail(send_from='test.maplecroft@gmail.com',send_to=email_recepient,subject='EONET Data (Fires, Storms, Landslides)',text='Hi. You will find attached to this mail the EONET data for the period %s. Cheers. Jean-Bruno' %last_month,files=workbook,server='smtp.gmail.com',port='587',username='test.maplecroft@gmail.com',password='Test1212',isTls=True)

