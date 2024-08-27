from datetime import datetime

from flask import Flask, send_from_directory, request
import sqlite3
import webbrowser
from threading import Timer

app = Flask(__name__)

# 数据库连接函数
def connect_to_db():
    conn = sqlite3.connect('app_database.db')
    return conn

# 根路径路由：提供 index.html 页面
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# 路由：接收前端发送的用户信息并保存到数据库
@app.route('/save_user_info', methods=['POST'])
def save_user_info():
    user_data = request.json
    telegram_id = user_data.get('id')
    first_name = user_data.get('first_name')
    username = user_data.get('username')
    device_model = user_data.get('device')

    conn = connect_to_db()
    c = conn.cursor()

    # 保存用户信息到数据库（如之前的保存逻辑）
    register_time = datetime.now()

    c.execute('''
        INSERT OR IGNORE INTO users (telegram_id, uid, register_time, device_model, login_count, last_login_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (telegram_id, username, register_time, device_model, 1, register_time))

    # 更新登录计数和最后登录时间
    c.execute('''
        UPDATE users SET login_count = login_count + 1, last_login_time = ?
        WHERE telegram_id = ?
    ''', (register_time, telegram_id))

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "User info saved!"})

# 自动打开浏览器的函数
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # 定时器启动 Flask 服务器后自动打开浏览器
    Timer(1, open_browser).start()
    app.run(debug=True)
