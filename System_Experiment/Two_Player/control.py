# this script is begin forging at the begining
import requests
import csv
from solve_quilibria import *
import time
import threading
import json
from datetime import datetime
import math
nxt = 100000000
delay = 100
delay_short = 20 
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
                #print(cont)
                return True
            time.sleep(1)
        except BaseException:
                #print(cont)
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

#     #######  
def balance_player(url, my_addr, his_addr,my_dummy_addr, his_dummy_addr,my_main_key,my_dummy_key):
    main_balance = get_balance(url,my_addr)
    dummy_balance = get_balance(url,my_dummy_addr)
    his_main_balance = get_balance(url,his_addr)
    his_dummy_balance = get_balance(url,his_dummy_addr)
    total_balance = main_balance+dummy_balance+his_main_balance+his_dummy_balance
    ratio_a = (main_balance+dummy_balance)/total_balance
    ratio_b = (his_dummy_balance+his_main_balance)/total_balance
    [x1,x2] = solve_quilibria(ratio_a,ratio_b)
    dummy_ratio = x1
    if ratio_a < 0.2 :
        dummy_ratio = 0
    if ratio_a > 0.8:
        dummy_ratio =  ratio_a/2
    dummy_later = dummy_ratio * total_balance
    #print("Balance later = ", dummy_later,"Balance transfer = ",dummy_later-dummy_balance)
    if dummy_balance < dummy_later - 10:
        make_transfer(url,my_dummy_addr,my_main_key,dummy_later-dummy_balance)
    if dummy_balance > dummy_later + 10:
        make_transfer(url,my_addr,my_dummy_key,dummy_balance-dummy_later)

def calculate_after_balance(my_balance, his_balance,my_dummy_balance, his_dummy_balance,priv_balance):
    total_balance = my_balance+his_balance+my_dummy_balance+his_dummy_balance+priv_balance
    print("total_balance = ", tonxt(total_balance))
    ratio_a = (my_balance+my_dummy_balance)/total_balance
    ratio_b = (his_balance+his_dummy_balance)/total_balance
    print("ratio_a = ", ratio_a , "ratio_b = ", ratio_b)
    x1,x2 = solve_equilibria(ratio_a,ratio_b)
    print("x1 = ", x1 , "x2 = ", x2)    
    dummy_ratio = x1
    dummy_later = dummy_ratio * total_balance
    main_later = my_balance + my_dummy_balance - dummy_later
    #print(dummy_later, main_later)
    return dummy_later, main_later

def print_everyone_balance(URL,a_main,b_main,a_dummy,b_dummy,private_addr):
    main_a_balance = get_balance(url,a_main)
    dummy_a_balance = get_balance(url,a_dummy)
    main_b_balance = get_balance(url,b_main)
    dummy_b_balance = get_balance(url,b_dummy)
    priv_balance = get_balance(url,private_addr)
    print("main a balance = ",tonxt(main_a_balance), "main b balance = ",tonxt(main_b_balance),"dummy a balance = ",tonxt(dummy_a_balance),"dummy b balance = " ,tonxt(dummy_b_balance),"private=",tonxt(priv_balance))
######  

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

pre_main_a_balance = [0 for i in range(len(addr))]
pre_main_b_balance = [0 for i in range(len(addr))]
pre_dummy_a_balance = [0 for i in range(len(addr))]
pre_dummy_b_balance = [0 for i in range(len(addr))]

time_begin = int(time.time())
##### Game Balance  ######## Begin forging for all addresses 
print(" ******************* Forgin Begin ****************")
fail = [0]*len(addr)
for ip in range(len(addr)):
    if fail[ip] > 3:
        continue    
    try:
        print("----------------------- IP = ", ip,"---------------------")
        url = addr[ip]
        player_b_id = 10 + ( ip % 10 )+1
        player_a_id = int( ip / 10 )
        print("player a id:",player_a_id,"player b id:", player_b_id)
        player_a_sec = str(int(player_a_id))
        player_b_sec = str(int(player_b_id))
        print("",url)
        try:    
            ini_forging(url,private_sec)
            time.sleep(1)
            ini_forging(url,player_a_sec)
            time.sleep(1)
            ini_forging(url,player_b_sec)
            time.sleep(1)
            ini_forging(url,private_sec)
            time.sleep(1)
            ini_forging(url,player_a_sec)
            time.sleep(1)
            ini_forging(url,player_b_sec)
            print("Ini forging ok ip=",url)
        except:
            print("IP=",url,"Initial Forgin Fails")
            fail[ip] = fail[ip] + 3
        print(" No. ",ip ,"player a sec" + player_a_sec + "player b sec" + player_b_sec ,"initial success") 

        player_a_addr = get_account_id(url , player_a_sec)
        player_b_addr = get_account_id(url, player_b_sec)
        dummy_a_addr = get_account_id(url , dummya_sec)
        dummy_b_addr = get_account_id(url, dummyb_sec)
        private_addr = get_account_id(url, private_sec)

        print("private_addr",private_addr)

        main_a_balance = get_balance(url,player_a_addr)
        dummy_a_balance = get_balance(url,dummy_a_addr)
        main_b_balance = get_balance(url,player_b_addr)
        dummy_b_balance = get_balance(url,dummy_b_addr)
        priv_balance = get_balance(url,private_addr)
        print("ok2")

        print("main a balance = ",tonxt(main_a_balance), "main b balance = ",tonxt(main_b_balance),"dummy a balance = ",tonxt(dummy_a_balance),"dummy b balance = " ,tonxt(dummy_b_balance),"private balance = " ,tonxt(priv_balance))
        pre_dummy_a_balance[ip],pre_main_a_balance[ip] =  calculate_after_balance(main_a_balance, main_b_balance,dummy_a_balance, dummy_b_balance,priv_balance)
        pre_dummy_b_balance[ip],pre_main_b_balance[ip] =  calculate_after_balance(main_b_balance, main_a_balance,dummy_b_balance, dummy_a_balance,priv_balance)
        print("IP=",ip,"A main Balance = ",tonxt(pre_main_a_balance[ip]),"B main Balance = ",tonxt(pre_main_b_balance[ip]),"A dummy balance",tonxt(pre_dummy_a_balance[ip]),"B dummy balance",tonxt(pre_dummy_b_balance[ip]))   
        print("yes 1")
        make_transfer(url,dummy_a_addr,player_a_sec,pre_dummy_a_balance[ip])
        make_transfer(url,dummy_b_addr,player_b_sec,pre_dummy_b_balance[ip])
        print_everyone_balance(url,player_a_addr,player_b_addr,dummy_a_addr,dummy_b_addr,private_addr)
        print(" ******************* Initialization  Complete ****************")
    except:
        print("something wrong in ", url)
        fail[ip] = fail[ip] + 1
    finally:
        pass
#Readjustment and Rebasement

if (int(time.time()) - time_begin) < delay:
    time.sleep(delay-(int(time.time())- time_begin))

while 1:
    time_begin = int(time.time())
    for ip in range(len(addr)):
            if fail[ip] > 3:
                continue
            try:
                print("----------------------- IP = ", ip,"---------------------")
                url = addr[ip]
                player_b_id = 10 + ( ip % 10 )+1
                player_a_id = ( ip / 10 )
                player_a_sec = str(int(player_a_id))
                player_b_sec = str(int(player_b_id))
                player_a_addr = get_account_id(url , player_a_sec)
                player_b_addr = get_account_id(url, player_b_sec)
                dummy_a_addr = get_account_id(url , dummya_sec)
                dummy_b_addr = get_account_id(url, dummyb_sec)
                

                main_a_balance = get_balance(url,player_a_addr)
                dummy_a_balance = get_balance(url,dummy_a_addr)
                main_b_balance = get_balance(url,player_b_addr)
                dummy_b_balance = get_balance(url,dummy_b_addr)
                priv_balance = get_balance(url,private_addr)

                print_everyone_balance(url,player_a_addr,player_b_addr,dummy_a_addr,dummy_b_addr,private_addr)
                print("miner A previous main balance", tonxt(pre_main_a_balance[ip]), "current main balance", tonxt(main_a_balance), "A win",tonxt(main_a_balance - pre_main_a_balance[ip]))
                print("miner B previous main balance", tonxt(pre_main_b_balance[ip]), "current main balance", tonxt(main_b_balance), "B win",tonxt(main_b_balance - pre_main_b_balance[ip]))
                print("miner A total",tonxt(main_a_balance+ dummy_a_balance),"miner B total",tonxt(main_b_balance+ dummy_b_balance))
                a_payable_to_b = (main_a_balance - pre_main_a_balance[ip]) * (pre_dummy_b_balance[ip]/(pre_dummy_b_balance[ip] + pre_main_a_balance[ip]))
                b_payable_to_a = (main_b_balance - pre_main_b_balance[ip]) * (pre_dummy_a_balance[ip]/(pre_dummy_a_balance[ip] + pre_main_b_balance[ip]))
                print("miner A payable to B", tonxt(a_payable_to_b))
                print("miner B payable to A", tonxt(b_payable_to_a))
                temp_a_main = main_a_balance - a_payable_to_b + b_payable_to_a
                temp_b_main = main_b_balance - b_payable_to_a + a_payable_to_b
                temp_a_dummy = dummy_a_balance
                temp_b_dummy = dummy_b_balance

                pre_dummy_a_balance[ip],pre_main_a_balance[ip] =  calculate_after_balance(temp_a_main, temp_b_main,temp_a_dummy, temp_b_dummy,priv_balance)
                pre_dummy_b_balance[ip],pre_main_b_balance[ip] =  calculate_after_balance(temp_b_main, temp_a_main,temp_b_dummy, temp_a_dummy,priv_balance)
                print("temp_a_dummy = ", tonxt(temp_a_dummy) ,'pre_dummy_a_balance', tonxt(pre_dummy_a_balance[ip]))
                print("temp_b_dummy = ", tonxt(temp_b_dummy) ,'pre_dummy_b_balance', tonxt(pre_dummy_b_balance[ip]))
            except:
                print("Fail when adjust   IP=", url)
                fail[ip] = fail[ip] + 1
            try: 
                if a_payable_to_b > b_payable_to_a:
                    pay_flag = make_transfer(url,player_b_addr,player_a_sec,a_payable_to_b-b_payable_to_a)
                    if pay_flag == True:
                        print("transfer from a to b", tonxt(a_payable_to_b-b_payable_to_a))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        print("transfer failure","ip=",ip,"a pay b",tonxt(a_payable_to_b-b_payable_to_a))
                        continue

                else:
                    pay_flag = make_transfer(url,player_a_addr,player_b_sec,b_payable_to_a - a_payable_to_b)
                    if pay_flag == True:
                        print("transfer from b to a", tonxt(b_payable_to_a-a_payable_to_b))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        print("transfer failure","ip=",ip,"b pay a",tonxt(b_payable_to_a-a_payable_to_b))
                        
                        continue
                if pre_dummy_a_balance[ip] > temp_a_dummy:
                    pay_flag = make_transfer(url,dummy_a_addr,player_a_sec,pre_dummy_a_balance[ip] - temp_a_dummy)
                    if pay_flag == True:
                        print("transfer from a main to a dummy", tonxt(pre_dummy_a_balance[ip] - temp_a_dummy))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        print("transfer failure","ip=",ip,"a transfer to dummy a",tonxt(pre_dummy_a_balance[ip] - temp_a_dummy))
                        continue
                else:
                    pay_flag = make_transfer(url,player_a_addr,dummya_sec, temp_a_dummy - pre_dummy_a_balance[ip])
                    if pay_flag == True:
                        print("transfer from a dummy to a main", tonxt(temp_a_dummy - pre_dummy_a_balance[ip]))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        print("transfer failure","ip=",ip,"dummy a to a ",tonxt(temp_a_dummy - pre_dummy_a_balance[ip]))
                        continue
                if pre_dummy_b_balance[ip] > temp_b_dummy:
                    pay_flag = make_transfer(url,dummy_b_addr,player_b_sec,pre_dummy_b_balance[ip] - temp_b_dummy)
                    if pay_flag == True:
                        print("transfer from b main to b dummy", tonxt(pre_dummy_b_balance[ip] - temp_b_dummy))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        continue
                else:
                    pay_flag = make_transfer(url,player_b_addr,dummyb_sec, temp_b_dummy - pre_dummy_b_balance[ip])
                    if pay_flag == True:
                        print("transfer from b dummy to b main", tonxt(temp_b_dummy - pre_dummy_b_balance[ip] ))
                    else:
                        pre_dummy_a_balance[ip] =  get_balance(url,dummy_a_addr)
                        pre_main_a_balance[ip] = get_balance(url,player_a_addr)
                        pre_dummy_b_balance[ip] = get_balance(url,dummy_b_addr)
                        pre_main_b_balance[ip] = get_balance(url,player_b_addr)
                        continue
            except:
                print("Fail when adjust   IP=", url)
                fail[ip] = fail[ip] + 1
            try:
                print_everyone_balance(url,player_a_addr,player_b_addr,dummy_a_addr,dummy_b_addr,private_addr)
                pre_dummy_a_balance[ip],pre_main_a_balance[ip] =  calculate_after_balance(temp_a_main, temp_b_main,temp_a_dummy, temp_b_dummy,priv_balance)
                pre_dummy_b_balance[ip],pre_main_b_balance[ip] =  calculate_after_balance(temp_b_main, temp_a_main,temp_b_dummy, temp_a_dummy,priv_balance)
            except:
                print("Error when print balance")
                fail[ip] = fail[ip] + 1
    if (int(time.time()) - time_begin) < delay:
        time.sleep(delay-(int(time.time())- time_begin))