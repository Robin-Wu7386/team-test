# admin_backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'admin_secret_key_123456')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # MySQL配置（完全一致）
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'tcmdb')
    MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')

    # Neo4j配置（完全一致）
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', '12345678')

    # 管理员令牌（完全一致）
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'admin_fixed_token_123456')

    # Python路径（用于情感分析）
    PYTHON_PATH = os.getenv('PYTHON_PATH', 'D:\\Python\\python.exe')

    # 端口（完全一致）
    PORT = int(os.getenv('PORT', 8000))