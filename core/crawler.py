import requests
from bs4 import BeautifulSoup
from core.models import db, LotteryData

def run_spider():
    # 来源1: 500彩票网
    url1 = "https://datachart.500.com/dlt/history/newinc/history.php?limit=1"
    
    try:
        r = requests.get(url1, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        row = soup.find('tr', class_='t_tr1')
        if not row: return
        
        tds = [td.text.strip() for td in row.find_all('td')]
        
        # 字段映射 (根据500网实际结构)
        period = tds[0]
        front = f"{tds[1]},{tds[2]},{tds[3]},{tds[4]},{tds[5]}"
        back = f"{tds[6]},{tds[7]}"
        date = tds[14] if len(tds) > 14 else "2026-01-01"

        # 检查是否已存在
        exists = LotteryData.query.filter_by(period=period).first()
        if not exists:
            new_data = LotteryData(
                period=period,
                draw_date=date,
                front_balls=front,
                back_balls=back
            )
            db.session.add(new_data)
            db.session.commit()
            print(f"成功同步第 {period} 期数据")
            
    except Exception as e:
        print(f"爬虫出错: {str(e)}")
