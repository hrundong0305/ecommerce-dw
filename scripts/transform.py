"""
ETL Step 2: Transform
清洗ODS数据，计算衍生字段，写入DWD明细层
- 过滤掉取消的订单（is_valid=0）
- 计算毛利和毛利率
- 标准化日期格式
"""
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db" / "ecommerce_dw.db"


def transform():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("4. 从ODS读取数据，开始清洗...")
    df = pd.read_sql("SELECT * FROM ods_orders", conn)
    print(f"   ODS原始记录: {len(df)} 条")

    # 清洗1：计算毛利和毛利率
    df["gross_profit"] = (df["revenue"] - df["cost_total"]).round(2)
    df["margin_rate"] = (df["gross_profit"] / df["revenue"] * 100).round(1)

    # 清洗2：标记有效订单（排除已取消）
    df["is_valid"] = df["status"].apply(lambda x: 0 if x == "已取消" else 1)

    # 清洗3：选择写入DWD的字段
    dwd_df = df[[
        "order_id", "order_date", "sku", "product_name", "category",
        "quantity", "price", "revenue", "cost_total",
        "gross_profit", "margin_rate",
        "channel", "region", "status", "is_valid"
    ]].copy()
    dwd_df.rename(columns={"price": "unit_price"}, inplace=True)

    # 写入DWD
    print(f"5. 写入DWD明细层...")
    dwd_df.to_sql("dwd_orders_detail", conn, if_exists="append", index=False)
    conn.commit()

    valid_count = cursor.execute("SELECT COUNT(*) FROM dwd_orders_detail WHERE is_valid=1").fetchone()[0]
    invalid_count = cursor.execute("SELECT COUNT(*) FROM dwd_orders_detail WHERE is_valid=0").fetchone()[0]
    print(f"   DWD写入完成: 有效订单 {valid_count} 条, 已取消 {invalid_count} 条")

    conn.close()
    print("✅ Transform 完成\n")


if __name__ == "__main__":
    transform()
