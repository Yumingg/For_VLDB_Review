# this script is begin forging at the begining
import requests
import csv
import time
import threading
import json
from datetime import datetime

nxt = 100000000
delay = 100
dummy_sec = "000"
def posty(thread_name,drs):
    r = requests.post(drs)
    t = datetime.now()
    print('user1:',r.content)
    print(thread_name,t)
    return r

def get_account_id(url,secret):
    url = 'http://'+url+':7876/nxt?requestType=getAccountId'
    d = {'secretPhrase':secret}
    r = requests.post(url, data=d)
    cont = r.content
    json_data = json.loads(cont)
    addr = json_data['accountRS']
    return addr

def make_transfer(url,recipent,secret,amount):
    url = 'http://'+url+':7876/nxt?requestType=sendMoney'
    amt = int(amount)
    d = {'recipient':recipent,'amountNQT':amt,'secretPhrase':secret,'feeNQT':0,'deadline':100}
    r = requests.post(url, data=d)
    return r.content

def ini_forging(url,secret):
    d = "http://"+url+":7876/nxt?%2Fnxt&requestType=startForging&secretPhrase="+secret
    r = requests.post(d)
    return 0

def get_balance(url,addr):
    d = "http://"+url+":7876/nxt?=%2Fnxt&requestType=getBalance&account="+addr
    r = requests.post(d)
    cont = r.content
    json_data = json.loads(cont)
    balance = json_data['balanceNQT']
    return int(balance)

def balance_attacker(url,attacker_sec,dummy_sec,attacker_addr,dummy_addr):
    attacker_balance = get_balance(url,attacker_addr)
    dummy_balance = get_balance(url,dummy_addr)
    half = (attacker_balance + dummy_balance)/2
    print("Balance Transfer to Dummy", (half-dummy_balance)/2)
    if dummy_balance < half - 10:
        make_transfer(url,dummy_addr,attacker_sec,half-dummy_balance)

def victim_transfer_attacker(url, previctim_balance, victim_sec,victim_addr, attacker_addr,dummy_addr):
    new_vic_balance = get_balance(url,victim_addr)
    dummy_balance = get_balance(url,dummy_addr)
    ratio = dummy_balance/(previctim_balance + dummy_balance)
    print("Make a new victim yield")

    yeild = (new_vic_balance - previctim_balance)*ratio
    if yeild > 10:
        make_transfer(url,attacker_addr,victim_sec,yeild)
    print("Attacker has ", new_vic_balance/nxt, "previously",previctim_balance/nxt, "Dummy has ", dummy_balance/nxt)
    print("Attacker transfers", yeild/nxt)
    if (yeild < 0) :
        return previctim_balance
    else:
        return new_vic_balance - yeild

## Import the IP addresses list

addr = []
with open('ip10037.csv') as urlf:
    lines=csv.reader(urlf)
    for line in lines:
        if (len(line) < 1):
            continue
        if (len(line[0]) > 5):
            addr.append(line[0])
    print(addr)
    flag = [1]*len(addr)
    print(flag)

time_begin = int(time.time())
## Begin forging for all addresses 
print(" ******************* Forgin Begin ****************")
for ip in range(len(addr)):
    try:
        url = addr[ip]
        attacker_id = 10 + ( ip % 10 )+1
        victim_id = ( ip / 10 )
        attacker_sec = str(int(attacker_id))
        victim_sec = str(int(victim_id))
        print(" No. ",ip ,"attacker sec" + attacker_sec + "victim sec" + victim_sec ) 
        attacker_addr = get_account_id(url , attacker_sec)
        victim_addr = get_account_id(url, victim_sec)
        dummy_addr = get_account_id(url,dummy_sec)
        ini_forging(url,attacker_sec)
        ini_forging(url,victim_sec)
        print(" ******************* Forgin Complete ****************")
    except:
        print("something wrong1 with instance",url)

#Readjustment and Rebasement
if (int(time.time()) - time_begin) < delay:
    time.sleep(delay-(int(time.time())- time_begin))


pre_victim_balance = [0 for i in range(len(addr))]
for ip in range(len(addr)):
    try:
        url = addr[ip]
        url = addr[ip]
        victim_id = ( ip / 10 )
        victim_addr = get_account_id(url, victim_sec)
        pre_victim_balance[ip] = get_balance(url,victim_addr)
        print("victim_id", victim_id, "victim_sec", victim_sec, "victim balance", pre_victim_balance[ip])
    except:
        print("something wrong2 with instance",url)

while 1:
    time_begin = int(time.time())
    for ip in range(len(addr)):
        try:
            url = addr[ip]
            url = addr[ip]
            attacker_id = 10 + ( ip % 10 ) +1
            victim_id = ( ip / 10 )
            attacker_sec = str(int(attacker_id))
            victim_sec = str(int(victim_id))
            attacker_addr = get_account_id(url , attacker_sec)
            victim_addr = get_account_id(url, victim_sec)
            dummy_addr = get_account_id(url,dummy_sec)
            pre_victim_balance[ip] = victim_transfer_attacker(url, pre_victim_balance[ip], victim_sec,victim_addr, attacker_addr,dummy_addr)
        except: 
            print("something wrong3 with instance",url)
    if (int(time.time()) - time_begin) < delay:
        time.sleep(delay -(int(time.time()) - time_begin))
    time_begin = int(time.time())

    for ip in range(len(addr)):
        try:
            url = addr[ip]
            url = addr[ip]
            attacker_id = 10 + ( ip % 10 ) +1
            victim_id = ( ip / 10 )
            attacker_sec = str(int(attacker_id))
            victim_sec = str(int(victim_id))
            attacker_addr = get_account_id(url , attacker_sec)
            victim_addr = get_account_id(url, victim_sec)
            dummy_addr = get_account_id(url,dummy_sec)
            balance_attacker(url,attacker_sec,dummy_sec,attacker_addr,dummy_addr)
        except:
            print("something wrong4 with instance",url)
    if (int(time.time()) - time_begin) < delay:
        time.sleep(delay -(int(time.time()) - time_begin))
    time_begin = int(time.time())