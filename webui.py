from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 查询汇率数据
def get_rates():
    conn = sqlite3.connect("exchange_rate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT currency, rate,timestamp FROM rates")
    rates = cursor.fetchall()
    conn.close()
    return rates

# API 返回汇率数据
@app.route("/api/rates")
def api_rates():
    rate = get_rates()
    return jsonify(rate)

# 显示折线图
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
