import csv

from numpy.lib.shape_base import expand_dims
from solve_equilibria import *
import time
import threading
import json
from datetime import datetime
import math
import numpy as np

def getR(m,x):
    total_effective = 1 - np.sum(x)
    rr = np.transpose(np.sum(x,axis=1))
    R = m - rr
    R = R / total_effective
    return np.reshape(R,[5,1])

def getprofit(R,x,m,r):
    total_fake_stake = m + np.sum(x,axis=0)
    profit = np.dot(x,r) + R
    total_fake_stake = np.reshape(total_fake_stake,[5,1])
    profit = profit/total_fake_stake
    return profit

def calculate_iteration_profit(number,s,m,player,threshold):
    round = 0 
    err = 1
    profit = np.zeros([number,1])
    sz = player
    new_profit=np.zeros([number,1])
    itr = 1
    while (err > threshold):
        itr += 1 
        R= getR(m,s)
        for i in range(0,number):
            profit_new = getprofit(R,s,m,new_profit)
            player_profit_new = profit_new[i]
            new_profit[i] = player_profit_new
        err = max(abs(new_profit-profit))
        profit = new_profit
    ave_profit = profit[player]
    return ave_profit

def iteration_equilibira(number,m,s):
    alpha = 0.001
    threshold = 0.00001
    delta = 0.00000001
    err = 1
    round = 0 
    s1 = s
    while(err > threshold):
#        print(s)
        err = 0 
        round += 1
        for i in range(0,number):
            for j in range(0,number):
                s2 = s1
                s2[i][j] = s2[i][j] + delta
                uni_profit1 = calculate_iteration_profit(number,s1,m,i,threshold)
                s1[i][j] = s1[i][j] + delta
                uni_profit2 = calculate_iteration_profit(number,s1,m,i,threshold)
                s1[i][j] = s1[i][j] - delta
                der = (uni_profit2 - uni_profit1)/delta
                new_strategy = s1[i,j]+ alpha * der
                new_strategy = min(new_strategy,m[i])
                new_strategy = max(new_strategy,0)
                err = max(err, abs(new_strategy-s1[i][j]))
                s1[i,j] = new_strategy
    return s1

