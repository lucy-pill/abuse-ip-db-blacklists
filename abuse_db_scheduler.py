import time
import schedule
import subprocess
import os

def Fxxk_Request_JSON():
    subprocess.call(["python", 'request-json.py'], cwd= "/Users/KSCLOUD/Desktop/BOX/abuse-ip-db-blacklist", shell=True)

def Fxxk_Abuse_IP_To_DB():
    subprocess.call(["python", 'data-list-up.py'], cwd= "/Users/KSCLOUD/Desktop/BOX/abuse-ip-db-blacklist", shell=True)

def Fxxk_Abuse_IP_To_Local():
    subprocess.call(["python", 'store.py'], cwd= "/Users/KSCLOUD/Desktop/BOX/abuse-ip-db-blacklist", shell=True)

os.system('cls')
print("\n")
print("────────────────────────────────────────────────")
print("\n")
print("        Abuse DB Process 실행 대기 중...")
print("\n")
print("────────────────────────────────────────────────")

schedule.every().day.at("13:35").do(Fxxk_Request_JSON)
schedule.every().day.at("13:36").do(Fxxk_Abuse_IP_To_DB)
schedule.every().day.at("13:37").do(Fxxk_Abuse_IP_To_Local)

while(True):
    schedule.run_pending()
    time.sleep(1)