# this script is begin forging at the begining
import requests
import csv
import copy
from solve_equilibria import *
import time
import threading
import json
from datetime import datetime
import math

nxt = 100000000
delay = 100
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
    print('user1:',r.content)
    print(thread_name,t)
    return r

def tonxt(bal):
    return bal/nxt

def get_account_id(url,secret):
    for i in range(10):   
        try:
            url1 = 'http://'+url+':7876/nxt?requestType=getAccountId'
            d = {'secretPhrase':secret}
            r = requests.post(url1, data=d)
            cont = r.content
            json_data = json.loads(cont)
            addr = json_data['accountRS']
            return addr
        except:
            print("get account fails retry")
            time.sleep(1)
            pass

def make_transfer(url,recipent,secret,amount):
    for i in range(10):
        try:
            sender = get_account_id(url, secret)
            print("make transfer from",sender,"to" , recipent, "for", amount)
            urlr = 'http://'+url+':7876/nxt?requestType=sendMoney'
            amt = int(amount)
            amt = max(amt-1000000,0)
            if amt == 0:    
                return True
            d = {'recipient':recipent,'amountNQT':amt,'secretPhrase':secret,'feeNQT':0,'deadline':100}
            r = requests.post(urlr, data=d)
            cont = r.content
            #print(cont)
            json_data=json.loads(cont)
            brdcs = json_data['broadcasted']
            #print(type(brdcs))
            if brdcs == True:
                print("transaction sent successfully")
                print(cont)
                return True
            time.sleep(1)
        except BaseException:
                print(cont)
                #print("resend transaction")
                #print(flag)
                time.sleep(1)
                continue
    print(cont)
    print("failure url",url)
    return False

def ini_forging(url,secret):
    while 1:
        try:
            d = "http://"+url+":7876/nxt?%2Fnxt&requestType=startForging&secretPhrase="+secret
            r = requests.post(d)
            print(r.content)
            return 0
        except:
            print("init forging fails")
            time.sleep(1)
            pass

def get_balance(url,addr):
    while 1:
        try:
            d = "http://"+url+":7876/nxt?=%2Fnxt&requestType=getBalance&account="+addr
            r = requests.post(d)
            cont = r.content
            json_data = json.loads(cont)
            balance = json_data['balanceNQT']
            return int(balance)
        except:
            print("get balance fails retry")
            print(cont)
            time.sleep(1)
            pass

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


def get_main_balance(url,list_add):
    len_list = len(list_add)
    balance_list = [1 for n in range(6)]
    for i in range(0,len_list):
        balance_temp = get_balance(url,list_add[i])
        balance_list[i] = balance_temp
    for i in range(0,len_list):
        print("addr:",list_add[i],"balance:",balance_list[i])
    return balance_list

def initialize(url,sec_list):
    len_list = len(sec_list)
    for i in range(0,len_list):
        ini_forging(url,sec_list[i])
    return True

def optimal_strategy(balance_list):
    total_balance = sum(balance_list)
    player_balance = [balance_list[i] for i in range(0,5)]
    player_balance_ratio = [(float(player_balance[i])/total_balance) for i in range(0,5)]
    s = np.zeros([5,5])
    strategy = iteration_equilibira(5,player_balance_ratio,s)
    return strategy,total_balance

def get_current_withhold_balance(url,withhold_id_list):
    withhold_balance = np.zeros([5,5])
    for i in range(0,5):
        for j in range(0,5):
            withhold_balance[i][j] = get_balance(url,withhold_id_list[i][j])
    return withhold_balance

def calculate_total_balance(main_balance,withhold_balance):
    total_balance_list = [0 for n in range(6)]
    total_balance_list = main_balance
    for i in range(0,5):
        for j in range(0,5):
            total_balance_list[i] += withhold_balance[i][j]
    return total_balance_list

def adjust_player_balance(url,player_number,main_list,withhold_list,main_pass,withhold_pass,main_balance,current_balance,target_balance):
    for i in range(0,player_number):
        for j in range(0,player_number):
            if current_balance[i][j] > target_balance[i][j] + 1000000:
                make_transfer(url,main_list[i],withhold_pass[i][j],current_balance[i][j] - target_balance[i][j])
            if current_balance[i][j] < target_balance[i][j] - 1000000:
                make_transfer(url,withhold_list[i][j],main_pass[i],target_balance[i][j]-current_balance[i][j])
    return 0

def distribute_profit(url,player_number,main_pass,main_addr,pre_main_balance,pre_withhold_balabce):
    from_sender_to_receiver_amount = np.zeros([5,5])
    been_withhold_amount = np.sum(pre_withhold_balabce,axis=0)
    current_main_balance = np.zeros(5)
    for i in range(0,player_number):
        current_sender_balance = get_balance(url,main_addr[i])
        current_main_balance[i]=current_sender_balance 
        for j in range(0,player_number):
            if i == j:
                continue
            ratio = pre_withhold_balabce[j][i] / (pre_main_balance[i] + been_withhold_amount[i] +1000000)
            from_sender_to_receiver_amount[i][j] = ratio*(current_sender_balance - pre_main_balance[i])
    for i in range(0,player_number):
        for j in range(0,player_number):
            if i == j:
                continue
            if from_sender_to_receiver_amount[i][j] > from_sender_to_receiver_amount[j][i] + 1000000:
                make_transfer(url,main_addr[j],main_pass[i],from_sender_to_receiver_amount[i][j] - from_sender_to_receiver_amount[j][i])
                temp = from_sender_to_receiver_amount[i][j] - from_sender_to_receiver_amount[j][i]
                current_main_balance[i] -= temp
                current_main_balance[j] += temp
    return current_main_balance

addr = []
with open('addr.csv') as urlf:
    lines=csv.reader(urlf)
    for line in lines:
        if (len(line) < 1):
            continue
        if (len(line[0]) > 5):
            addr.append(line[0])

[dummy_sec_list,dummy_addr_list] = get_dummy_list_addr(addr[0])

instance_number = len(addr)
prev_withhold_balance=np.zeros((instance_number,5,5))
prev_main_balance=np.zeros((instance_number,6))
pre_total_balance=np.zeros((instance_number,6))
current_withhold_balance=np.zeros((5,5))
current_main_balance=np.zeros(6)
current_total_balance=np.zeros(6)
current_strategy = np.zeros((instance_number,5,5))

####  Initialization
main_pass = [['z' for i in range(0,6)] for j in range(0,instance_number)]
main_addr = [['z' for i in range(0,6)] for j in range(0,instance_number)]
time_begin = int(time.time())
for i in range(0,instance_number):
    print("-------No", i)
    player_sec_list = get_player_list_sec(i)
    main_pass[i] = player_sec_list
    player_addr_list = get_player_list_addr(addr[i],player_sec_list)
    main_addr[i] = player_addr_list
    initialize(addr[i],player_sec_list)
    initialize(addr[i],player_sec_list)
    initialize(addr[i],player_sec_list)
    initialize(addr[i],player_sec_list)
time_end = int(time.time())
if (time_end - time_begin) < 30:
    time.sleep(30-time_end +time_begin)
#### Initial Balance
print('--------Initial strategy')
time_begin = int(time.time())
for i in range(0,instance_number):
    current_withhold_balance = get_current_withhold_balance(addr[i],dummy_addr_list)
    current_main_balance = get_main_balance(addr[i],player_addr_list)
    current_player_total_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
    strategy,total_balance = optimal_strategy(current_player_total_balance)
    current_balance_strategy = strategy*total_balance
    adjust_player_balance(addr[i],5,main_addr[i],dummy_addr_list,main_pass[i],dummy_sec_list,current_withhold_balance,current_balance_strategy)
time_end = int(time.time())
if (time_end - time_begin) < 30:
    time.sleep(30-time_end +time_begin)
time_begin = int(time.time())
for i in range(0,instance_number):
    current_withhold_balance = get_current_withhold_balance(addr[i],dummy_addr_list)
    current_main_balance = get_main_balance(addr[i],player_addr_list)
    prev_withhold_balance[i] = copy.deepcopy(current_withhold_balance)
    prev_main_balance[i] = copy.deepcopy(current_main_balance)
    current_main_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
time_end = int(time.time())
if (time_end - time_begin) < 50:
    time.sleep(50-time_end +time_begin)

### Update Balance
time.sleep(50)
while (True):
    time_begin = int(time.time())
    for i in range(0,instance_number):
        current_withhold_balance = get_current_withhold_balance(addr[i],dummy_addr_list)
        current_main_balance = get_main_balance(addr[i],player_addr_list)
        current_total_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
        current_main_balance = distribute_profit(addr[i],5,main_pass[i],main_addr[i],prev_main_balance[i],prev_withhold_balance[i])
    time_end = int(time.time())
    if (time_end - time_begin) < 30:
        time.sleep(30-time_end +time_begin)

    time_begin = int(time.time())
    for i in range(0,instance_number):
        current_withhold_balance = get_current_withhold_balance(addr[i],dummy_addr_list)
        current_main_balance = get_main_balance(addr[i],player_addr_list)
        current_total_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
        strategy,total_balance = optimal_strategy(current_total_balance)
        current_balance_strategy = strategy*total_balance
        adjust_player_balance(addr[i],5,main_addr[i],dummy_addr_list,main_pass[i],dummy_sec_list,current_withhold_balance,current_balance_strategy)
    time_end = int(time.time())
    if (time_end - time_begin) < 30:
        time.sleep(30-time_end +time_begin)

    time_begin = int(time.time())
    for i in range(0,instance_number):
        current_withhold_balance = get_current_withhold_balance(addr[i],dummy_addr_list)
        current_main_balance = get_main_balance(addr[i],player_addr_list)
        prev_withhold_balance[i] = copy.deepcopy(current_withhold_balance)
        prev_main_balance[i] = copy.deepcopy(current_main_balance)
        current_main_balance = calculate_total_balance(current_main_balance,current_withhold_balance)
    time_end = int(time.time())
    if (time_end - time_begin) < 50:
        time.sleep(50-time_end +time_begin)
