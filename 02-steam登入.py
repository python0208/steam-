"""
steam模拟登入：
js逆向：非对称加密 rsa
第一个包请求到公钥
"""

import requests
import execjs
import time
import random

url = 'https://help.steampowered.com/zh-cn/login/getrsakey/'

header = {
    'Host': 'help.steampowered.com',
    'Origin': 'https://help.steampowered.com',
    'Referer': 'https://help.steampowered.com/zh-cn/wizard/Login',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',

    'sec-ch-ua-platform': 'Windows',

    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    U'ser-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
    'X-Requested-With': 'XMLHttpRequest'
}
t = time.time()
print(int(t * 1000))
data = {
    'donotcache': int(t * 1000),
    'username': '账号'
}
session = requests.session()
res_json = session.post(url, headers=header, data=data).json()
# print(res_json)
mod = res_json['publickey_mod']  # 非对称秘钥加密的 公钥
exp = '010001'

# 使用execjs方法加密
node = execjs.get()
ctx = node.compile(open('steam.js', encoding='utf8').read())
functionname = 'getpassword("{}","{}","{}")'.format('密码', mod, exp)
password = ctx.eval(functionname)  # 获取得到密码加密的密文参数

print(password)
timestamp = res_json['timestamp']
url_login = "https://help.steampowered.com/zh-cn/login/dologin/"

t = int(time.time() * 1000)
data_login = {
    'donotcache': t,
    'password': password,
    'username': '账号',
    'twofactorcode': '',
    'emailauth': '',
    'loginfriendlyname': '',
    'captchagid': -1,
    'captcha_text': '',
    'emailsteamid': '',
    'rsatimestamp': timestamp,
    'remember_login': 'false'
}

resp_login = session.post(url_login, headers=header, data=data_login)
print(session.cookies.get_dict())  # 获取session的cookie
print(resp_login.text)

