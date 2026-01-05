from flask import Flask
from admin.config import config
from admin.extensions import init_mysql
from admin.routes import main_bp, user_bp, admin_bp


# 创建Flask应用实例
def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates')
    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化MySQL数据库
    with app.app_context():
        init_mysql()

    # 注册蓝图（路由）
    app.register_blueprint(main_bp)  # 欢迎页：/
    app.register_blueprint(user_bp, url_prefix='/user')  # 普通用户：/user/*
    app.register_blueprint(admin_bp, url_prefix='/admin')  # 管理员：/admin/*

    return app