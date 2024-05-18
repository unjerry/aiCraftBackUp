import matplotlib.pyplot as plt
import numpy as np
import requests  # send request
from time import sleep  # set interval prevent to be blocked
import random  # generate random number
import json
from datetime import datetime
from bs4 import BeautifulSoup

header = {
    "cookie": "_s_tentry=weibo.com; Apache=7485007942317.74.1715497752915; SINAGLOBAL=7485007942317.74.1715497752915; ULV=1715497752918:1:1:1:7485007942317.74.1715497752915:; WBtopGlobal_register_version=2024051215; SUB=_2A25LRBvTDeRhGeBN71MW9C3NyjmIHXVoOBEbrDV8PUNbmtB-LXLmkW9NRGEc62_jcvitaKWXZ1G1wLJQCjxNza8_; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.bzodw6CNGcOqvZm676g85JpX5KzhUgL.Foq0Sh2NShepeK-2dJLoIEBLxK-L12-L1-qLxKqLBK5LB-2LxK.LB.-L1K.LxKnL1K2LBo-t; ALF=02_1718089859",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}
company_url = "https://s.weibo.com/weibo?"
url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?"
company_parameter = {
    "q": "泰达股份",
    "typeall": 1,
    "suball": 1,
    "timescope": "custom:2018-01-01:2018-01-01",
    "Refer": "g",
    "page": 1,
}
response = requests.get(company_url, headers=header, params=company_parameter)
# sdt = 1685548800  # 20230601
sdt = 1704038400  # 20240101
# sdt = 1514736000  # 20180101
dle = 86400
L = []
T = []
""" 12 * 30 * 6 + 6 * 30 """
for dt in range(6 * 30):
    # sleep(0.1 + 0.1 * random.random())
    tm = sdt + dt * dle
    T.append(tm)
    timerange = datetime.strftime(
        datetime.fromtimestamp(tm), "custom:%Y-%m-%d:%Y-%m-%d"
    )
    company_parameter["page"] = 1
    company_parameter["timescope"] = timerange
    response = requests.get(company_url, headers=header, params=company_parameter)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    sdf = soup.find_all("div", attrs={"action-type": "feed_list_item"})
    ul = soup.find("ul", attrs={"node-type": "feed_list_page_morelist"})
    ans = 0
    if ul != None:
        # print(ul)
        li = ul.find_all("li")
        lenn = len(li)
    else:
        lenn = 1
    for i in range(1, lenn + 1):
        company_parameter["page"] = i
        response = requests.get(company_url, headers=header, params=company_parameter)
        soup = BeautifulSoup(response.text, "html.parser")
        # with open("div", "w", encoding="UTF-8") as file:
        #     file.write(f"{soup}")
        wei = soup.find(string="抱歉，未找到相关结果。")
        if wei == None:
            sdf = soup.find_all("div", attrs={"action-type": "feed_list_item"})
            tm = 0.001 + 0.001 * random.random()
            sleep(tm)
            # print(i, len(sdf), tm)
            ans += i
        else:
            print(wei)
    print(timerange, lenn, ans)
    L.append(ans)
    np.save(company_parameter["q"][-2:] + "LL", L)
    np.save(company_parameter["q"][-2:] + "TT", T)


# with open("L", "w") as file:
#     file.write(f"{L}")
# with open("T", "w") as file:
#     file.write(f"{T}")
np.save(company_parameter["q"][-2:] + "LL", L)
np.save(company_parameter["q"][-2:] + "TT", T)
plt.rcParams["figure.dpi"] = 500
plt.plot(L)
plt.savefig("assa")
