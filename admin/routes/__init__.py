from flask import Blueprint

# 欢迎页蓝图（根路径）
main_bp = Blueprint('main', __name__, template_folder='../templates')

# 普通用户蓝图（/user前缀）
user_bp = Blueprint('user', __name__, template_folder='../templates/user')

# 管理员蓝图（/admin前缀）
admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

# 导入子路由（必须在蓝图创建后）
from admin.routes import main, user, admin