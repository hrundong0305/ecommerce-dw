"""
ETL Step 1: Extract
从CSV抽取原始数据，写入ODS层（原样存储，不做清洗）
"""
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db" / "ecommerce_dw.db"
RAW_CSV = BASE_DIR / "data" / "raw" / "orders.csv"
SQL_FILE = BASE_DIR / "sql" / "create_tables.sql"


def extract():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 执行建表SQL
    print("1. 创建表结构...")
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()

    # 读取CSV
    print("2. 读取CSV原始数据...")
    df = pd.read_csv(RAW_CSV, encoding="utf-8-sig")
    print(f"   读取到 {len(df)} 条记录")

    # 写入ODS层
    print("3. 写入ODS层（原始数据）...")
    df.to_sql("ods_orders", conn, if_exists="append", index=False)
    conn.commit()

    # 验证
    count = cursor.execute("SELECT COUNT(*) FROM ods_orders").fetchone()[0]
    print(f"   ODS层写入完成，共 {count} 条记录")

    conn.close()
    print("✅ Extract 完成\n")


if __name__ == "__main__":
    extract()
