import bagpy
from bagpy import bagreader
import pandas as pd 
import seaborn as sea
import matplotlib.pyplot as plt
import time
import numpy as np
import multiprocessing as mp
import sqlite3
from pathlib import Path

#Read bag file into Python
b=bagreader('bags/blF1.bag')

#Open SQL database
conn = sqlite3.connect('my_data.sqlite')
c = conn.cursor()

#TODO: finish creating table in SQL
#Need data types of each column
#Error in csv 1 & 2: doesn't start collecting all data until row 8
#copies column R-V in csv #2 and strange error in csv#1 as well
c.execute('DROP TABLE IF EXISTS my_data.sqlite')
c.execute('''
CREATE TABLE "my_data"(
    "Time" REAL,
    "" 
)
''')

#Read in all message files in the bag as seperate csvs
csvfiles = []
for t in b.topics:
    print(t)
    data = b.message_by_topic(t)
    csvfiles.append(data)
    
