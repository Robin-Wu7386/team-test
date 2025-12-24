from flask import render_template, redirect, url_for, session
from admin.routes import main_bp

# 欢迎页（核心：管理员/普通用户分流）
@main_bp.route('/')
def welcome():
    # 已登录则跳转对应页面
    if 'username' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.index'))
    return render_template('welcome.html')