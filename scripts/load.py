"""
ETL Step 3: Load
从DWD明细层汇总数据，写入DWS汇总层和ADS应用层
- DWS: 按日×品类、按渠道、按地区汇总
- ADS: 运营日报、品类排行
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db" / "ecommerce_dw.db"


def load():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ========== DWS层 ==========
    print("6. 汇总DWS层...")

    # 按日×品类汇总
    cursor.execute("""
        INSERT INTO dws_daily_category
        SELECT
            order_date AS dt,
            category,
            COUNT(*) AS order_count,
            SUM(quantity) AS total_qty,
            SUM(revenue) AS total_revenue,
            SUM(gross_profit) AS total_profit
        FROM dwd_orders_detail
        WHERE is_valid = 1
        GROUP BY order_date, category
    """)

    # 按渠道汇总
    cursor.execute("""
        INSERT INTO dws_channel_summary
        SELECT
            channel,
            COUNT(*) AS order_count,
            SUM(revenue) AS total_revenue,
            SUM(gross_profit) AS total_profit,
            ROUND(AVG(revenue), 2) AS avg_order_value
        FROM dwd_orders_detail
        WHERE is_valid = 1
        GROUP BY channel
    """)

    # 按地区汇总
    cursor.execute("""
        INSERT INTO dws_region_summary
        SELECT
            region,
            COUNT(*) AS order_count,
            SUM(revenue) AS total_revenue
        FROM dwd_orders_detail
        WHERE is_valid = 1
        GROUP BY region
    """)
    conn.commit()
    print("   DWS层写入完成（日品类×365行, 渠道×4行, 地区×10行）")

    # ========== ADS层 ==========
    print("7. 生成ADS应用层报表...")

    # 运营日报
    cursor.execute("""
        INSERT INTO ads_daily_report
        SELECT
            order_date AS dt,
            COUNT(*) AS total_orders,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(SUM(gross_profit), 2) AS total_profit,
            ROUND(SUM(gross_profit) / SUM(revenue) * 100, 1) AS gross_margin,
            (
                SELECT category FROM dwd_orders_detail d2
                WHERE d2.order_date = d1.order_date AND d2.is_valid = 1
                GROUP BY category ORDER BY SUM(revenue) DESC LIMIT 1
            ) AS top_category,
            (
                SELECT channel FROM dwd_orders_detail d3
                WHERE d3.order_date = d1.order_date AND d3.is_valid = 1
                GROUP BY channel ORDER BY SUM(revenue) DESC LIMIT 1
            ) AS top_channel
        FROM dwd_orders_detail d1
        WHERE is_valid = 1
        GROUP BY order_date
    """)

    # 品类排行
    cursor.execute("""
        INSERT INTO ads_category_rank
        SELECT
            category,
            ROUND(SUM(revenue), 2) AS revenue,
            ROUND(SUM(gross_profit), 2) AS profit,
            COUNT(*) AS order_count,
            RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
        FROM dwd_orders_detail
        WHERE is_valid = 1
        GROUP BY category
        ORDER BY revenue_rank
    """)
    conn.commit()
    print("   ADS层写入完成（日报+品类排行）")

    # 打印结果摘要
    print("\n📊 数据仓库汇总结果：")
    print("-" * 50)

    print("\n【品类排行】")
    for row in cursor.execute("SELECT * FROM ads_category_rank ORDER BY revenue_rank"):
        print(f"  {row[0]:<8}  营收:{row[1]:>10}  利润:{row[2]:>10}  订单:{row[3]}")

    print("\n【渠道汇总】")
    for row in cursor.execute("SELECT * FROM dws_channel_summary ORDER BY total_revenue DESC"):
        print(f"  {row[0]:<10}  订单:{row[1]:>5}  营收:{row[2]:>10}  客单价:{row[4]}")

    print(f"\n【总览】")
    total = cursor.execute("SELECT COUNT(*), ROUND(SUM(revenue),2), ROUND(SUM(gross_profit),2) FROM dwd_orders_detail WHERE is_valid=1").fetchone()
    print(f"  有效订单: {total[0]}  总营收: {total[1]}  总利润: {total[2]}")

    conn.close()
    print("\n✅ Load 完成")


if __name__ == "__main__":
    load()
