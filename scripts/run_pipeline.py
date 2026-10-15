"""
主运行脚本：一键执行完整ETL流水线
用法：python run_pipeline.py
"""
import sys
from pathlib import Path

# 确保可以导入同目录模块
sys.path.insert(0, str(Path(__file__).parent))

from extract import extract
from transform import transform
from load import load


def run_pipeline():
    print("=" * 50)
    print("  电商数据仓库 ETL 流水线")
    print("  分层：ODS → DWD → DWS → ADS")
    print("=" * 50)
    print()

    # Step 1: Extract
    extract()

    # Step 2: Transform
    transform()

    # Step 3: Load
    load()

    print("\n" + "=" * 50)
    print("  🎉 数据仓库构建完成！")
    print("  数据库文件: db/ecommerce_dw.db")
    print("  可用 DB Browser for SQLite 打开查看")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
