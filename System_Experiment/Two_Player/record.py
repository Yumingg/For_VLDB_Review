# this script is begin forging at the begining
import requests
import csv
import time
import threading
import json
from datetime import datetime
delay = 20
dummya_sec = "000"
dummyb_sec = "111"
private_sec = "0000"

def get_block_num(url):
    d = "http://"+url+":7876/nxt?=%2Fnxt&requestType=getBlockchainStatus"
    r = requests.post(d)
    #print(r.content)
    cont = r.content
    json_data = json.loads(cont)
    block_num = json_data['numberOfBlocks']
    return int(block_num)

def posty(thread_name,drs):
    r = requests.post(drs)
    t = datetime.now()
    #print('user1:',r.content)
    #print(thread_name,t)
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
    #print("transfer amount ", amt)
    d = {'recipient':recipent,'amountNQT':amt,'secretPhrase':secret,'feeNQT':0,'deadline':100}
    r = requests.post(url, data=d)
    #print(r.content)
    return r.content

def ini_forging(url,secret):
    d = "http://"+url+":7876/nxt?%2Fnxt&requestType=startForging&secretPhrase="+secret
    r = requests.post(d)
    #print(r.content)
    return 0

def get_balance(url,addr):
    d = "http://"+url+":7876/nxt?=%2Fnxt&requestType=getBalance&account="+addr
    r = requests.post(d)
    #print(r.content)
    cont = r.content
    json_data = json.loads(cont)
    balance = json_data['balanceNQT']
    return int(balance)

def balance_attacker(url,attacker_sec,dummy_sec,attacker_addr,dummy_addr):
    attacker_balance = get_balance(url,attacker_addr)
    dummy_balance = get_balance(url,dummy_addr)
    half = (attacker_balance + dummy_balance)/2
    if dummy_balance < half - 10:
        make_transfer(url,dummy_addr,attacker_sec,half-dummy_balance)

def victim_transfer_attacker(url, previctim_balance, victim_sec,victim_addr, attacker_addr,dummy_addr):
    new_vic_balance = get_balance(url,victim_addr)
    dummy_balance = get_balance(url,dummy_addr)
    ratio = dummy_balance/(previctim_balance + dummy_balance)
    yeild = (new_vic_balance - previctim_balance)*ratio
    if yeild > 10:
        make_transfer(url,attacker_addr,victim_sec,yeild)
    new_vic_balance = get_balance(url,victim_addr)
    return new_vic_balance

## Import the IP addresses list

addr = []
with open('addr.csv') as urlf:
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
print(" ******************* Begin Checking ****************")
fail = [0]*len(addr)
while 1:
    for ip in range(len(addr)):
        if fail[ip] > 3:
            continue
        try:
            url = addr[ip]
            player_b_id = int(10 + ( ip % 10 )+1)
            player_a_id = int( ip / 10 )
            player_a_sec = str(int(player_a_id))
            player_b_sec = str(int(player_b_id))
            player_a_addr = get_account_id(url , player_a_sec)
            player_b_addr = get_account_id(url, player_b_sec)
            dummy_a_addr = get_account_id(url , dummya_sec)
            dummy_b_addr = get_account_id(url, dummyb_sec)
            private_addr = get_account_id(url, private_sec)

            print("ok1")
            player_a_main_balance = get_balance(url,player_a_addr)
            player_b_main_balance = get_balance(url,player_b_addr)
            dummy_a_balance = get_balance(url,dummy_a_addr)
            dummy_b_balance = get_balance(url,dummy_b_addr)
            private_balance = get_balance(url,private_addr)

            player_a_balance = dummy_a_balance + player_a_main_balance
            player_b_balance = dummy_b_balance + player_b_main_balance
                
            num = get_block_num(url)
            file_name = "2player1solo/"+str(ip)+".csv"
            print("here")
            with open(file_name,"a+") as csvfile: 
                    writer = csv.writer(csvfile)
                    writer.writerow([num,player_a_balance,player_a_balance+player_b_balance+private_balance,(float)(player_a_balance/(player_a_balance+player_b_balance+private_balance)),(float)((player_b_balance)/(player_a_balance+player_b_balance+private_balance))])
        except:
            fail[ip] = fail[ip] + 1
            print("Some Error in recording", url)
    if (int(time.time()) - time_begin) < delay:
        time.sleep(delay-(int(time.time()) - time_begin))
    time_begin = int(time.time())