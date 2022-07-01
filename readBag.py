
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
import os

print(os.getcwd())
b=bagreader('bags/blF1.bag')

Path('my_data.db').touch()
conn = sqlite3.connect('my_data.db')
c = conn.cursor

csvfiles = []
for t in b.topics:
    data = b.message_by_topic(t)
    csvfiles.append(data)
