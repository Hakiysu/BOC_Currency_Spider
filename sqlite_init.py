import sqlite3

# 初始化数据库
def init_db():
    conn = sqlite3.connect("exchange_rate.db")
    cursor = conn.cursor()
    # 创建表
    # id: 主键，自增
    # currency: 货币名称
    # rate: 汇率
    # timestamp: 时间戳, 默认为UTC+8时间
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency TEXT NOT NULL,
            rate REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
