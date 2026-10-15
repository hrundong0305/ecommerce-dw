"""
生成模拟玩具电商订单数据
用于数据仓库项目演示
"""
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# 产品列表
products = [
    {"sku": "TOY-001", "name": "积木拼装城堡", "category": "积木玩具", "price": 89.9, "cost": 35.0},
    {"sku": "TOY-002", "name": "儿童拼图100片", "category": "拼图", "price": 29.9, "cost": 8.0},
    {"sku": "TOY-003", "name": "遥控赛车", "category": "电动玩具", "price": 129.0, "cost": 55.0},
    {"sku": "TOY-004", "name": "毛绒玩具熊", "category": "毛绒玩具", "price": 49.9, "cost": 18.0},
    {"sku": "TOY-005", "name": "彩色蜡笔套装", "category": "美术用品", "price": 19.9, "cost": 6.0},
    {"sku": "TOY-006", "name": "磁力片积木", "category": "积木玩具", "price": 159.0, "cost": 65.0},
    {"sku": "TOY-007", "name": "泡泡机", "category": "电动玩具", "price": 39.9, "cost": 15.0},
    {"sku": "TOY-008", "name": "绘本故事书", "category": "图书", "price": 35.0, "cost": 12.0},
]

# 渠道
channels = ["小红书商城", "唯品会", "B站会员购", "淘宝C店"]
regions = ["广东", "浙江", "江苏", "上海", "北京", "四川", "湖北", "福建", "湖南", "山东"]
platforms = ["国内电商", "跨境电商"]

# 生成订单
orders = []
start_date = datetime(2026, 1, 1)
order_id = 100001

for i in range(1500):
    order_date = start_date + timedelta(days=random.randint(0, 270))
    product = random.choice(products)
    channel = random.choice(channels)
    region = random.choice(regions)
    qty = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
    revenue = round(product["price"] * qty, 2)
    cost = round(product["cost"] * qty, 2)
    status = random.choices(["已完成", "已完成", "已完成", "已退款", "已取消"], weights=[70, 15, 8, 4, 3])[0]

    orders.append({
        "order_id": order_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "sku": product["sku"],
        "product_name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "cost": product["cost"],
        "quantity": qty,
        "revenue": revenue,
        "cost_total": cost,
        "channel": channel,
        "region": region,
        "status": status,
    })
    order_id += 1

df = pd.DataFrame(orders)
df.to_csv("E:/岗位问询/ecommerce-dw/data/raw/orders.csv", index=False, encoding="utf-8-sig")
print(f"Generated {len(df)} orders")
print(df.head(10))
print(f"\nCategories: {df['category'].value_counts().to_dict()}")
print(f"Channels: {df['channel'].value_counts().to_dict()}")
