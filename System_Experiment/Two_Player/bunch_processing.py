import os
import json
import csv
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
path = "2player1solo"
blocks = [200,200,500,1000,2000,5000]
files =  os.listdir(path)
file_name = "305020"
# Get number of test case
stake_list = []
file_index = -1
for file in files:
    file_info = os.path.splitext(file)
    filename,type = file_info
    if not os.path.isdir(file) and type=='.csv':
        file_index += 1
        print("Cases",file_index,":","filename=",filename)
        loc = path+"/"+file
        try:
            with open(loc, "r") as csvfile:
                table = []
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    newlist = [int(row[0]),float(row[3])]
                    table.append(newlist)
                minum = []

                for block in range(0,6):
                    ll = [n for n in table if ( (n[0]> blocks[block] - 100) and (n[0]< blocks[block] + 100))]
                    ls = np.array(ll)
                    minum.append(np.amin(ls,axis=0)[1])
                    print(minum)
                stake_list.append(minum)
        except:
            print("something wrong",file_index)
try:
    with open(file_name+".csv","a+") as csvfile: 
        wr = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for r in stake_list:
            wr.writerow(r)
except:
    print("something wrong")