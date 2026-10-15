-- ============================================
-- 电商数据仓库建表脚本
-- 分层：ODS → DWD → DWS → ADS
-- 数据库：SQLite
-- ============================================

-- ========== ODS层（原始数据层） ==========
-- 原样存储CSV导入的数据，不做清洗
DROP TABLE IF EXISTS ods_orders;
CREATE TABLE ods_orders (
    order_id      INTEGER,
    order_date    TEXT,
    sku           TEXT,
    product_name  TEXT,
    category      TEXT,
    price         REAL,
    cost          REAL,
    quantity      INTEGER,
    revenue       REAL,
    cost_total    REAL,
    channel       TEXT,
    region        TEXT,
    status        TEXT
);

-- ========== DWD层（明细数据层） ==========
-- 清洗后的订单明细，一行一个有效订单
DROP TABLE IF EXISTS dwd_orders_detail;
CREATE TABLE dwd_orders_detail (
    order_id      INTEGER PRIMARY KEY,
    order_date    TEXT,
    sku           TEXT,
    product_name  TEXT,
    category      TEXT,
    quantity      INTEGER,
    unit_price    REAL,
    revenue       REAL,
    cost_total    REAL,
    gross_profit  REAL,
    margin_rate   REAL,
    channel       TEXT,
    region        TEXT,
    status        TEXT,
    is_valid      INTEGER
);

-- ========== DWS层（汇总数据层） ==========
-- 按日×品类汇总
DROP TABLE IF EXISTS dws_daily_category;
CREATE TABLE dws_daily_category (
    dt            TEXT,
    category      TEXT,
    order_count   INTEGER,
    total_qty     INTEGER,
    total_revenue REAL,
    total_profit  REAL
);

-- 按渠道汇总
DROP TABLE IF EXISTS dws_channel_summary;
CREATE TABLE dws_channel_summary (
    channel       TEXT,
    order_count   INTEGER,
    total_revenue REAL,
    total_profit  REAL,
    avg_order_value REAL
);

-- 按地区汇总
DROP TABLE IF EXISTS dws_region_summary;
CREATE TABLE dws_region_summary (
    region        TEXT,
    order_count   INTEGER,
    total_revenue REAL
);

-- ========== ADS层（应用数据层） ==========
-- 运营日报
DROP TABLE IF EXISTS ads_daily_report;
CREATE TABLE ads_daily_report (
    dt              TEXT PRIMARY KEY,
    total_orders    INTEGER,
    total_revenue   REAL,
    total_profit    REAL,
    gross_margin    REAL,
    top_category    TEXT,
    top_channel     TEXT
);

-- 品类排行
DROP TABLE IF EXISTS ads_category_rank;
CREATE TABLE ads_category_rank (
    category      TEXT,
    revenue       REAL,
    profit        REAL,
    order_count   INTEGER,
    revenue_rank  INTEGER
);
