import requests  # send request
from time import sleep  # set interval prevent to be blocked
import random  # generate random number
import json

header = {
    "cookie": "_s_tentry=weibo.com; Apache=7485007942317.74.1715497752915; SINAGLOBAL=7485007942317.74.1715497752915; ULV=1715497752918:1:1:1:7485007942317.74.1715497752915:; WBtopGlobal_register_version=2024051215; SUB=_2A25LRBvTDeRhGeBN71MW9C3NyjmIHXVoOBEbrDV8PUNbmtB-LXLmkW9NRGEc62_jcvitaKWXZ1G1wLJQCjxNza8_; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.bzodw6CNGcOqvZm676g85JpX5KzhUgL.Foq0Sh2NShepeK-2dJLoIEBLxK-L12-L1-qLxKqLBK5LB-2LxK.LB.-L1K.LxKnL1K2LBo-t; ALF=02_1718089859",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}
company_url = "https://s.weibo.com/weibo?"
url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?"
company_parameter = {
    "q": "长江电力",
    "typeall": 1,
    "suball": 1,
    "timescope": "custom:2024-04-01:2024-04-01",
    "Refer": "g",
    "page": 1,
}
response = requests.get(company_url, headers=header, params=company_parameter)

with open("cjdl.html", "w", encoding="UTF-8") as file:
    file.write(response.text)

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())
with open("pars", "w", encoding="UTF-8") as file:
    file.write(soup.prettify())

sdf = soup.find_all("div", attrs={"action-type": "feed_list_item"})
ul = soup.find("ul", attrs={"node-type": "feed_list_page_morelist"})
li = ul.find_all("li")
# print(len(sdf))
print(len(li))
with open("div", "w", encoding="UTF-8") as file:
    file.write(f"{sdf}")
    # print()
ans = 0
for i in range(1, len(li) + 1):
    company_parameter["page"] = i
    response = requests.get(company_url, headers=header, params=company_parameter)
    soup = BeautifulSoup(response.text, "html.parser")
    with open("div", "w", encoding="UTF-8") as file:
        file.write(f"{soup}")
    # print()
    wei = soup.find(string="抱歉，未找到相关结果。")
    # print(wei)
    if wei == None:
        sdf = soup.find_all("div", attrs={"action-type": "feed_list_item"})
        tm = 0.1 + 0.1 * random.random()
        sleep(tm)
        print(i, len(sdf), tm)
        ans += i
    else:
        print(wei)
print("tot", ans)
# soupdff = BeautifulSoup(sdf[0], "div.parser")
# with open("divf", "w", encoding="UTF-8") as file:
#     file.write(f"{soupdff}")
