#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:26:20 2020

@author: gavin
"""
import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def write_to_file(content):
    with open("result.txt","a",encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
        
#解析一个网页的内容，返回电影信息列表
def parse_one_page(html):
    soup = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
    
    #数组，含有dd标签的信息
    items = soup.find_all('dd')
    
    for item in items:
        yield{
            '排名:':item.find(class_="board-index").text,
            '电影名称':item.find(class_="name").a.getText(),
            '主演':item.find(class_="star").text.strip()[3:],
            '上映时间':item.find(class_="releasetime").text.strip()[5:],
            '得分':item.find(class_="integer").text+item.find(class_="fraction").text
            }

#获取url对应的页面
def get_one_page(url):
    try:
        #加头部信息，模拟google浏览器访问
        user_agent = 'Mozilla/5.0 (Windows NT 10.0 ; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/60.0.3112.'
        headers = {"User-Agent":user_agent} #设置处理
        
        response = requests.get(url,headers=headers)
        if response.status_code == 200:#判断是否获取页面正确响应
            #print(response.text)
            return response.text
        return None
    except RequestException:
        return None

def main(offset):
    url="https://maoyan.com/board/4?offset="+str(offset)
    #1 获取一个页面的html
    html= get_one_page(url)
    
    #2 解析html的代码
    moviesinfo = parse_one_page(html)
    
    for item in moviesinfo:
        print(item)
        #3 保存电影信息到一个txt文档中
        write_to_file(item)
        
#程序入口Mian（）函数
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    
