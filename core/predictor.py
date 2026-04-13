import random
from core.models import LotteryData

def generate_ai_prediction():
    """
    基础AI逻辑：结合历史热号与随机分布
    实际进阶可在此引入 6.1 节提到的 LSTM 模型
    """
    # 获取最近30期数据
    history = LotteryData.query.order_by(LotteryData.period.desc()).limit(30).all()
    
    # 模拟简单的热号统计（示例逻辑）
    # 正常开发应解析 history 中的字符串并统计频率
    hot_front = ["05", "12", "18", "23", "30"] 
    hot_back = ["02", "11"]

    predictions = [
        {
            "type": "热号追踪型",
            "numbers": f"{' '.join(hot_front)} + {' '.join(hot_back)}"
        },
        {
            "type": "区间平衡型",
            "numbers": "03 15 22 28 33 + 05 09"
        },
        {
            "type": "冷号回补型",
            "numbers": "01 07 14 26 31 + 04 08"
        }
    ]
    return predictions
