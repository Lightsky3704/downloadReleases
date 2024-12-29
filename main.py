#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:qiao xiong
# datetime:2024/12/29 22:44
# name: main

# 1. 导入reequests库、os
import requests
import os
from tqdm import tqdm

# 2. 设置api.github的代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 3. 获取批量下载链接的函数
def get_dlist(gurl: str) -> list:
    dlist = []
    # res = requests.get(url=gurl, proxies=proxies,verify=False)
    res = requests.get(url=gurl, verify=False)

    if res.status_code == 200:
        # print(res.status_code)
        for asset in res.json().get("assets", []):
            dlist.append(asset["browser_download_url"])
    return dlist


# 4. 通过下载链接下载文件
def download_release(durl: str):
    path_parts = durl.split('://')[1].split('/')
    save_dir = os.path.join(*path_parts[0:3], path_parts[5])
    file_name = path_parts[-1]
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, file_name)

    try:
        response = requests.get(durl, stream=True)
        total_size = int(response.headers.get('Content-Length', 0)) 
        
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in tqdm(response.iter_content(chunk_size=1024),
                                  total=total_size // 1024,
                                  unit='KB',
                                  desc=file_name):
                    if chunk:
                        file.write(chunk)
        else:
            print(f"下载失败，状态码: {response.status_code}")
    except Exception as e:
        print("下载出错: {}".format(e))

def main():
    gurl = 'https://api.github.com/repos/XTLS/Xray-core/releases/tags/v24.12.18'
    dlist = get_dlist(gurl)
    for durl in dlist:
        download_release(durl)

if __name__ == '__main__':
    main()
