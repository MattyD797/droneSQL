import sys
import os
import csv
import rosbag
import rospy
import sqlite3



#Reads in bag file
print('Reading Bag File...')
bag = rosbag.Bag('bags/blF1.bag')

#Initializes SQL db
print('Initializing SQL database...')
conn = sqlite3.connect('my_data.sqlite')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS my_data')
c.execute('''
CREATE TABLE "my_data"(
    "Time" FLOAT,
    "Monotonic" FLOAT,
    "AMSL" FLOAT,
    "Local" FLOAT,
    "Relative" FLOAT,
    "Terrain" FLOAT,
    "Bottom_Clearance" FLOAT
)
''')

#Gets all topics encased in bag file
topics = list(bag.get_type_and_topic_info()[1].keys())
print('Processing: '+ topics[0])

#reads in data encased in each topic
for topic, msg, t in bag.read_messages(topics[0]):
    time = (str(msg.header.stamp.secs)+'.'+str(msg.header.stamp.nsecs))
   
    sql = '''
            INSERT INTO my_data (Time,
                                Monotonic,
                                AMSL,
                                Local,
                                Relative,
                                Terrain,
                                Bottom_Clearance) VALUES (?,?,?,?,?,?,?)
        '''
    
    val = (time,
           msg.monotonic,
           msg.amsl,
           msg.local,
           msg.relative,
           msg.terrain,
           msg.bottom_clearance)
    
    c.execute(sql, val)
    
c.execute('SELECT * FROM my_data')
myresult = c.fetchall()
for x in myresult:
    print(x)