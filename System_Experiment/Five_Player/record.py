# this script is begin forging at the begining
import requests
import csv
import time
import threading
import copy
import json
import numpy as np
from datetime import datetime
nxt = 100000000
initial_stake = [3000000000-1, 1250000000-1, 1250000000-1, 1250000000-1, 1250000000-1, 2000000000-1]
delay = 10
delay_short = 20 
dummy_sec = "000"
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
    try:
        d = "http://"+url+":7876/nxt?=%2Fnxt&requestType=getBalance&account="+addr
        r = requests.post(d)
        #print(r.content)
        cont = r.content
        json_data = json.loads(cont)
        balance = json_data['balanceNQT']
    except:
        print("get balance error")
        print(cont)
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

def get_player_list_sec(seed):
    player_b_id = 10 + ( seed % 10 )+1
    player_a_id = int( seed / 10 )
    player_a_sec = str(int(player_a_id))
    player_b_sec = str(int(player_b_id))
    player_list = [player_a_sec,player_b_sec,'player3','player4','player5','solo']
    return player_list
## Import the IP addresses list

def get_player_list_addr(url,sec_list):
    len_list = len(sec_list)
    addr_list = [1 for n in range(6)]
    for i in range(0,len_list):
        addr_temp = get_account_id(url,sec_list[i])
        addr_list[i] = addr_temp
    #for i in range(0,len_list):
    #    print("sec:",sec_list[i],"addr:",addr_list[i])
    return addr_list
## Import the IP addresses list

def get_main_balance(url,list_add):
    len_list = len(list_add)
    balance_list = [1 for n in range(6)]
    for i in range(0,len_list):
        balance_temp = get_balance(url,list_add[i])
        balance_list[i] = balance_temp
    for i in range(0,len_list):
        print("addr:",list_add[i],"balance:",balance_list[i])
    return balance_list

def get_current_withhold_balance(url,withhold_id_list):
    withhold_balance = np.zeros([5,5])
    for i in range(0,5):
        for j in range(0,5):
            withhold_balance[i][j] = get_balance(url,withhold_id_list[i][j])
    return withhold_balance

def calculate_total_balance(main_balance,withhold_balance):
    total_balance_list = [0 for n in range(6)]
    total_balance_list = copy.deepcopy(main_balance)
    for i in range(0,5):
        for j in range(0,5):
            total_balance_list[i] += withhold_balance[i][j]
    return total_balance_list


def get_dummy_list_addr(url):
    global dummy_sec
    zz=['aa','aa','aa','aa','aa']
    zzz = [zz,zz,zz,zz,zz]
    dummy_sec_list = [['aa' for n in range(5)]for row in range(5)]
    dummy_addr_list = [['aa' for n in range(5)]for row in range(5)]
    for attacker in range(0,5):
        for victim in range(0,5):
            tt = dummy_sec + str(attacker) + str(victim)
            dummy_sec_list[attacker][victim] = tt
            dummy_addr_list[attacker][victim] = get_account_id(url,dummy_sec_list[attacker][victim])
    return dummy_sec_list,dummy_addr_list

addr = []
with open('addr.csv') as urlf:
    lines=csv.reader(urlf)
    for line in lines:
        if (len(line) < 1):
            continue
        if (len(line[0]) > 5):
            addr.append(line[0])


[dummy_sec_list,dummy_addr_list] = get_dummy_list_addr(addr[0])
print("get dummy id")

time_begin = int(time.time())
## Begin forging for all addresses 
print(" ******************* Begin Checking ****************")

instance_number = len(addr)
main_pass = [['z' for i in range(0,6)] for j in range(0,instance_number)]
main_addr = [['z' for i in range(0,6)] for j in range(0,instance_number)]
for i in range(0,instance_number):
    print("-------No", i)
    player_sec_list = get_player_list_sec(i)
    main_pass[i] = copy.deepcopy(player_sec_list)
    player_addr_list = get_player_list_addr(addr[i],player_sec_list)
    main_addr[i] = copy.deepcopy(player_addr_list)

fail = [0]*len(addr)
while 1:
    for ip in range(len(addr)):
        if fail[ip] > 3:
            continue
        try:
            url = addr[ip]
            current_withhold_balance = get_current_withhold_balance(url,dummy_addr_list)
            print("Withhold Balance")
            print(current_withhold_balance)
            current_main_balance = get_main_balance(url,main_addr[ip])
            print("Main Balance")
            print(current_main_balance)
            current_total_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
            print("Total Balance")
            print(current_total_balance)
            stake_earned = [current_total_balance[i]-initial_stake[i] for i in range(0,6)]
            print("stake_earned Balance")
            print(stake_earned)
            current_ratio = stake_earned/np.sum(stake_earned)
            num = get_block_num(url)
            file_name = "pos/"+str(ip)+".csv"
            print("here")
            with open(file_name,"a+") as csvfile: 
                    writer = csv.writer(csvfile)
                    writer.writerow([num,current_ratio[0],current_ratio[1],current_ratio[2],current_ratio[3],current_ratio[4],current_ratio[5]])
        except:
            fail[ip] = fail[ip] + 1
            print("Some Error in recording", url)
    if (int(time.time()) - time_begin) < delay:
        time.sleep(delay-(int(time.time()) - time_begin))
    time_begin = int(time.time())