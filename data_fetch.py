import requests
import sqlite3
from datetime import datetime
import time
from bs4 import BeautifulSoup

history_url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp"
current_url = "https://www.boc.cn/sourcedb/whpj/index.html"
# headers
headers = {
}
# data
data = {
    "erectDate": "2024-12-01",
    "nothing": datetime.now().strftime("%Y-%m-%d"),
    "pjname": "澳大利亚元",
    "page": "1",
    "head": "head_620.js",
    "bottom": "bottom_591.js",
    "paramtk": "",
    "token": "",
}


def fetch_history_exchange_rate():
    response = requests.post(history_url, headers=headers, data=data)
    print(response.text)
    
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码: {response.status_code}")
    
    if not response.text:
        raise Exception("响应内容为空")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('div', class_='BOC_main publish').find('table')
    rows = table.find_all('tr')[1:]  # skip header
    rates = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 7:
            continue  # skip invalid rows
        currency = cells[0].get_text(strip=True)
        rate = float(cells[1].get_text(strip=True)) 
        rates.append((currency, rate))
    print(rates)
    return rates

def fetch_current_exchange_rate():
    response = requests.get(current_url)
    # 设置响应内容的编码格式
    response.encoding = "utf-8"
    # 检查响应状态码
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码: {response.status_code}")
    # 检查响应内容
    if not response.text:
        raise Exception("响应内容为空")
    

    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取“澳大利亚元”对应的数据行
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[0].get_text(strip=True) == '澳大利亚元':
            data = [col.get_text(strip=True) for col in cols]
            break
    # 输出提取的内容
    columns = ["货币名称", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "中行折算价", "发布日期", "发布时间"]
    result = dict(zip(columns, data))
    #print(result)

    rate = float(result["现汇卖出价"])
    #print(rate)
    return rate

# 保存到数据库
def save_to_db(currency, rate):
    conn = sqlite3.connect("exchange_rate.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rates (currency, rate) VALUES (?, ?)", (currency, rate))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # loop get current exchange rate
    while True:
        #use try except to catch the error, prevent the program from crashing
        try:
            #get the current exchange rate
            rate = fetch_current_exchange_rate()
            #print the rate and time
            #print(f"澳大利亚元汇率: {rate}, 时间: {datetime.now()}")
            save_to_db("澳大利亚元", rate)
            time.sleep(30)
        except Exception as e:
            print(f"获取历史汇率失败: {e}")
        
        

        

    
