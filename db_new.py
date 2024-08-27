import sqlite3

# 连接到数据库（如果不存在会自动创建）
conn = sqlite3.connect('app_database.db')
c = conn.cursor()

# 创建用户表
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    telegram_id INTEGER,
    twitter_id INTEGER,
    register_time TIMESTAMP,
    first_login_time TIMESTAMP,
    device_model TEXT,
    browser TEXT,
    login_location TEXT,
    login_count INTEGER,
    last_login_time TIMESTAMP,
    ip_address TEXT
)''')

# 创建邀请表
c.execute('''CREATE TABLE IF NOT EXISTS invitations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inviter_id INTEGER,
    invitee_id INTEGER,
    invite_time TIMESTAMP,
    invite_location TEXT,
    invite_device TEXT,
    invitee_login_time TIMESTAMP,
    invitee_device TEXT,
    invitee_location TEXT,
    invitee_ip_address TEXT,
    invitee_join_method TEXT,
    coins_earned DECIMAL(10, 2),
    FOREIGN KEY (inviter_id) REFERENCES users (id),
    FOREIGN KEY (invitee_id) REFERENCES users (id)
)''')

# 创建邀请排行榜表
c.execute('''CREATE TABLE IF NOT EXISTS invitation_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    time_period TEXT CHECK( time_period IN ('hourly', 'daily', 'weekly', 'monthly', 'yearly') ),
    ranking_time TIMESTAMP,
    invites_count INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

# 创建任务表
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task_type TEXT CHECK( task_type IN ('签到', '关注Twitter', '进入Telegram频道', '邀请朋友', 'Telegram付费用户', 'Twitter付费用户') ),
    completion_time TIMESTAMP,
    reward DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

# 创建总排行榜表
c.execute('''CREATE TABLE IF NOT EXISTS general_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    ranking_type TEXT CHECK( ranking_type IN ('任务次数', '邀请朋友', '代币数量') ),
    time_period TEXT CHECK( time_period IN ('hourly', 'daily', 'weekly', 'monthly', 'yearly') ),
    ranking_time TIMESTAMP,
    value DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

# 创建钱包表
c.execute('''CREATE TABLE IF NOT EXISTS wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    wallet_name TEXT,
    wallet_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

# 创建钱包代币表
c.execute('''CREATE TABLE IF NOT EXISTS wallet_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wallet_id INTEGER,
    token_name TEXT,
    token_quantity DECIMAL(20, 10),
    FOREIGN KEY (wallet_id) REFERENCES wallets (id)
)''')

# 创建木鱼游戏表
c.execute('''CREATE TABLE IF NOT EXISTS wooden_fish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    knock_count INTEGER,
    is_premium BOOLEAN,
    last_knock_time TIMESTAMP,
    daily_knock_status TEXT,  -- JSON格式，记录每天是否敲木鱼
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

# 提交事务
conn.commit()

# 关闭连接
conn.close()

print("数据库创建成功！")
