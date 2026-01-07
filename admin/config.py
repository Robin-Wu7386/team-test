# MySQL数据库配置
class Config:
    # Flask核心配置
    SECRET_KEY = 'admin_2025_tcm_secure_key'  # 密钥，生产环境建议替换为环境变量
    # MySQL连接配置
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'               # 替换为你的MySQL用户名
    MYSQL_PASSWORD = 'zhr131415.'         # 替换为你的MySQL密码
    MYSQL_DB = 'tcmdb'            # 数据库名（自动创建）
    MYSQL_PORT = 3306
    MYSQL_CHARSET = 'utf8mb4'
    # 默认管理员账号（固定）
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

# 开发环境配置（仅开启DEBUG）
class DevelopmentConfig(Config):
    DEBUG = True

# 配置映射
config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig
}