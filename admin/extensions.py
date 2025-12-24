import pymysql
from flask import current_app


# 初始化MySQL数据库（仅创建用户表）
def init_mysql():
    """创建数据库+用户表，初始化默认管理员"""
    conn = get_mysql_conn()
    try:
        with conn.cursor() as cursor:
            # 1. 创建数据库（不存在则创建）
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {current_app.config['MYSQL_DB']} DEFAULT CHARACTER SET {current_app.config['MYSQL_CHARSET']}")
            cursor.execute(f"USE {current_app.config['MYSQL_DB']}")

            # 2. 创建用户表（核心：区分管理员/普通用户）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
                    username VARCHAR(50) NOT NULL UNIQUE COMMENT '账号',
                    password VARCHAR(255) NOT NULL COMMENT '加密密码',
                    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
                    role ENUM('admin', 'user') DEFAULT 'user' COMMENT '角色：admin-管理员，user-普通用户',
                    status INT DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
            ''')

            # 3. 创建默认管理员（从配置读取账号密码）
            from admin.utils.security import hash_password
            admin_pwd = hash_password(current_app.config['ADMIN_PASSWORD'])
            cursor.execute('SELECT * FROM users WHERE username = %s AND role = %s',
                           (current_app.config['ADMIN_USERNAME'], 'admin'))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO users (username, password, email, role, status)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    current_app.config['ADMIN_USERNAME'],
                    admin_pwd,
                    'admin@tcm.com',
                    'admin',
                    1
                ))

        conn.commit()
        print(
            f"MySQL初始化成功！数据库：{current_app.config['MYSQL_DB']}，默认管理员：{current_app.config['ADMIN_USERNAME']}/{current_app.config['ADMIN_PASSWORD']}")
    except Exception as e:
        print(f"MySQL初始化失败：{str(e)}")
        conn.rollback()
    finally:
        conn.close()


# 获取MySQL连接
def get_mysql_conn():
    """获取数据库连接（每次请求独立连接）"""
    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB'],
        port=current_app.config['MYSQL_PORT'],
        charset=current_app.config['MYSQL_CHARSET'],
        cursorclass=pymysql.cursors.DictCursor  # 返回字典格式数据
    )