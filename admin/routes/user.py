import re

from flask import render_template, request, redirect, url_for, session, flash
from admin.routes import user_bp
from admin.extensions import get_mysql_conn
from admin.utils.security import hash_password, check_password


# 普通用户登录
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 已登录则跳转主页
    if 'username' in session and session['role'] == 'user':
        return redirect(url_for('user.index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = get_mysql_conn()
        try:
            with conn.cursor() as cursor:
                # 仅查询普通用户
                cursor.execute('''
                    SELECT id, username, password,phonenumber,role, status,del 
                    FROM users 
                    WHERE username = %s AND role = %s AND del = 1
                ''', (username, 'user'))
                user = cursor.fetchone()

                if not user:
                    flash('普通用户账号不存在！', 'danger')
                elif user['status'] != 1:
                    flash('账号已被禁用！', 'danger')
                elif not check_password(password, user['password']):
                    flash('密码错误！', 'danger')
                elif user['del'] != 1:
                    flash('账号已被删除！', 'danger')
                else:
                    # 登录成功，设置session
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['user_id'] = user['id']
                    flash('普通用户登录成功！', 'success')
                    return redirect(url_for('user.profile', user_id=user['id']))
        except Exception as e:
            flash(f'登录失败：{str(e)}', 'danger')
        finally:
            conn.close()

    return render_template('login.html')


# 普通用户注册
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        phonenumber = request.form['phonenumber'].strip()
        email = request.form['email'].strip()
        confirm_pwd = request.form['confirm_pwd'].strip()

        # 基础验证
        if password != confirm_pwd:
            flash('两次密码不一致！', 'danger')
            return render_template('register.html')
        if len(password) < 6:
            flash('密码长度不少于6位！', 'danger')
            return render_template('register.html')
        if not re.match(r'^\d{11}$', phonenumber):
            flash('手机号必须为11位数字！', 'danger')
            return render_template('user/register.html')


        conn = get_mysql_conn()
        try:
            with conn.cursor() as cursor:
                # 检查用户名/邮箱是否已存在
                cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username, email))
                if cursor.fetchone():
                    flash('用户名或邮箱已存在！', 'danger')
                    return render_template('register.html')

                # 插入普通用户（固定role=user）
                hashed_pwd = hash_password(password)
                cursor.execute('''
                    INSERT INTO users (username, password, phonenumber,email, role)
                    VALUES (%s, %s, %s, %s,%s)
                ''', (username, hashed_pwd,phonenumber, email, 'user'))
                conn.commit()
                flash('注册成功！请登录', 'success')
                return redirect(url_for('user.login'))
        except Exception as e:
            flash(f'注册失败：{str(e)}', 'danger')
            conn.rollback()
        finally:
            conn.close()

    return render_template('register.html')


# 普通用户主页（空白，仅占位）
@user_bp.route('/index')
def index():
    """保持兼容：跳转到当前用户个人页"""
    if 'username' not in session or session['role'] != 'user':
        flash('请先登录普通用户账号！', 'warning')
        return redirect(url_for('user.login'))
    return redirect(url_for('user.profile', user_id=session['user_id']))


@user_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id: int):
    """普通用户个人主页 + 评论提交"""
    if 'username' not in session or session['role'] != 'user':
        flash('请先登录普通用户账号！', 'warning')
        return redirect(url_for('user.login'))
    if session.get('user_id') != user_id:
        flash('无权访问其他用户的主页！', 'danger')
        return redirect(url_for('user.profile', user_id=session['user_id']))

    conn = get_mysql_conn()
    comments = []
    user = None
    try:
        with conn.cursor() as cursor:
            # 获取用户信息
            cursor.execute('SELECT id, username, phonenumber, email, created_at FROM users WHERE id = %s AND del = 1',
                           (user_id,))
            user = cursor.fetchone()
            if not user:
                flash('用户不存在或已被删除！', 'danger')
                return redirect(url_for('user.logout'))

            # 新增评论
            if request.method == 'POST':
                content = request.form.get('content', '').strip()
                if not content:
                    flash('评论内容不能为空！', 'warning')
                else:
                    cursor.execute('INSERT INTO comments (user_id, content) VALUES (%s, %s)', (user_id, content))
                    conn.commit()
                    flash('评论提交成功！', 'success')
                    return redirect(url_for('user.profile', user_id=user_id))

            # 查询用户评论
            cursor.execute('''
                SELECT id, content, created_at, updated_at 
                FROM comments 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            ''', (user_id,))
            comments = cursor.fetchall()
    except Exception as e:
        flash(f'操作失败：{str(e)}', 'danger')
        conn.rollback()
    finally:
        conn.close()

    return render_template('index.html', user=user, comments=comments)


# 普通用户退出登录
@user_bp.route('/logout')
def logout():
    session.clear()
    flash('已退出登录！', 'info')
    return redirect(url_for('main.welcome'))