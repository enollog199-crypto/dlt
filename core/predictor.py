import random

def generate_ai_prediction():
    """
    轻量级 AI 预测逻辑（不依赖 pandas）
    """
    # 模拟 3 组不同类型的预测
    predictions = [
        {
            "type": "热号追踪型",
            "numbers": "05 12 18 23 30 + 02 11"
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
