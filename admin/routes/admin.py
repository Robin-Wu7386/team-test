from flask import render_template, request, redirect, url_for, session, flash
from admin.routes import admin_bp
from admin.extensions import get_mysql_conn
from admin.utils.security import check_password


# 管理员登录验证装饰器（复用）
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session or session['role'] != 'admin':
            flash('请以管理员身份登录！', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)

    return decorated


# 管理员登录
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 已登录则跳后台首页
    if 'username' in session and session['role'] == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = get_mysql_conn()
        try:
            with conn.cursor() as cursor:
                # 仅查询管理员
                cursor.execute('''
                    SELECT id, username, password, role, status 
                    FROM users 
                    WHERE username = %s AND role = %s
                ''', (username, 'admin'))
                user = cursor.fetchone()

                if not user:
                    flash('管理员账号不存在！', 'danger')
                elif user['status'] != 1:
                    flash('管理员账号已被禁用！', 'danger')
                elif not check_password(password, user['password']):
                    flash('密码错误！', 'danger')
                else:
                    # 登录成功，设置session
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['user_id'] = user['id']
                    flash('管理员登录成功！', 'success')
                    return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'登录失败：{str(e)}', 'danger')
        finally:
            conn.close()

    return render_template('admin/login.html')


# 管理员后台首页（空白，仅占位）
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html', username=session['username'])


# 管理员-用户管理（核心：删除/禁用普通用户）
@admin_bp.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
    conn = get_mysql_conn()
    try:
        # 1. 删除普通用户（禁止删除管理员）
        if request.method == 'POST' and 'delete' in request.form:
            user_id = request.form['user_id']
            with conn.cursor() as cursor:
                # 验证是普通用户才删除
                cursor.execute('''
                    UPDATE users 
                    SET del = 0 
                    WHERE id = %s AND role = %s
                ''', (user_id, 'user'))
                conn.commit()
                flash('普通用户删除成功！', 'success')
            return redirect(url_for('admin.users'))

        # 2. 禁用/启用普通用户
        if request.method == 'POST' and 'change_status' in request.form:
            user_id = request.form['user_id']
            status = request.form['status']
            with conn.cursor() as cursor:
                cursor.execute('UPDATE users SET status = %s WHERE id = %s AND role = %s',
                               (status, user_id, 'user'))
                conn.commit()
                flash('用户状态修改成功！', 'success')
            return redirect(url_for('admin.users'))

        # 3. 查询所有普通用户（管理员仅1个，不展示）
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE role = %s AND del = 1  ORDER BY id DESC', ('user',))
            users = cursor.fetchall()
    except Exception as e:
        flash(f'操作失败：{str(e)}', 'danger')
        conn.rollback()
    finally:
        conn.close()

    return render_template('users.html', users=users)


# 管理员退出登录
@admin_bp.route('/logout')
@admin_required
def logout():
    session.clear()
    flash('管理员已退出登录！', 'info')
    return redirect(url_for('main.welcome'))