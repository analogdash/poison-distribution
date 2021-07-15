import random
import requests
import time
import datetime

with open('10k-most-common.txt', 'r') as fp:
    pwlist = []
    for line in fp.readlines():
        line = line.strip()
        line = ''.join(ch for ch in line if ch.isalnum())
        if len(line) > 6:
            pwlist.append(line)

def gen_pwd():
    subs=[('e', '3'),
          ('o', '0'),
          ('l', '1'),
          ('i', '1'),
          ('a', '4')]
    sub = random.choice(subs)
    pw = random.choice(pwlist)
    if random.choice([True, False]):
        pw = pw.replace(*sub)
    return pw

with open('prefixes.txt', 'r') as fp:
    prefixlist = [line.strip() for line in fp.readlines()]

def gen_num():
    num = [random.choice(['0', '63']),
        random.choice(prefixlist),
        str(random.randint(1000000, 9999999))]
    return ''.join(num)
    
with open('fnames.txt', 'r') as fp:
    fnames = []
    for line in fp.readlines():
        line = line.strip()
        line = ''.join(ch for ch in line if ch.isalnum() or ch in ['-', '_', '.', ' '])
        fnames.append(line)

with open('lnames.txt', 'r') as fp:
    lnames = []
    for line in fp.readlines():
        line = line.strip()
        line = ''.join(ch for ch in line if ch.isalnum() or ch in ['-', '_', '.', ' '])
        lnames.append(line)

def gen_birthyear():
    yearset = list(range(1970,2002))
    return str(random.choices(yearset, weights=range(2,2+len(yearset)), k=1)[0])

def gen_username():
    split = random.choice(['', '.', '_'])
    fname = random.choice(fnames).replace(' ', split)
    fname = random.choice([fname, fname[0:random.randint(0, len(fname))]])
    split = random.choice(['', '.', '_'])
    lname = random.choice(lnames).replace(' ', split)
    yr = gen_birthyear()
    yr = random.choices(['', yr, yr[-2:]], weights=[10,4,2], k=1)[0]
    split = random.choice(['', '.', '_'])
    name = [fname,lname]
    random.shuffle(name)
    uname = (split.join(name) + yr).strip(' ._-')
    if random.choice([True, True, True, False]):
        uname = uname.lower()
    return uname
    

def gen_email():
    domains = ['gmail.com', 'yahoo.com', 'yahoo.com.ph', 'icloud.com', 'hotmail.com', 'outlook.com',]
    return gen_username() + '@' + random.choices(domains, weights=[10,2,2,1,1,1], k=1)[0]

def gen_pair():
    return {
        'email': random.choice([gen_email(), gen_num()]),
        'passwd' : gen_pwd()
        }

endpoint = 'http://13.76.46.162/login/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'http://13.76.46.162/home/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://13.76.46.162',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

count = 0
while True:
    count+=1
    pair = gen_pair()
    for _ in range(0,20):
        try:
            resp = requests.post(endpoint, headers=headers, data=pair, allow_redirects=False)
        except:
            print('fail')
            pass
        else:
            print(datetime.datetime.now(), count, resp.status_code, pair)
            break
    else:
        print('fail after 20')
        exit()
    time.sleep(1)
    if resp.status_code != 302:
        break