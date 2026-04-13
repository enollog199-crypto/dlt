import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from core.models import db, LotteryData

def fetch_500_lottery():
    url = "https://datachart.500.com/dlt/history/newinc/history.php?limit=1"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        row = soup.find('tr', class_='t_tr1') # 获取最新一行
        if row:
            tds = row.find_all('td')
            # 简化解析逻辑，实际需根据页面具体结构调整
            period = tds[0].text.strip()
            # 示例逻辑：如果数据库没这期，就存入
            print(f"检查到最新期号: {period}")
    except Exception as e:
        print(f"抓取失败: {e}")

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    # 每隔 6 小时检查一次更新
    scheduler.add_job(func=fetch_500_lottery, trigger="interval", hours=6)
    scheduler.start()
