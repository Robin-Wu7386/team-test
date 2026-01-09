from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
import datetime
from functools import wraps

# JWT配置
SECRET_KEY = 'your-secret-key'  # 实际应用中应该使用环境变量
JWT_EXPIRATION = 3600  # 1小时过期

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置数据库连接池
pool = pooling.MySQLConnectionPool(
    pool_name="mysql_pool",
    pool_size=10,
    host="localhost",
    user="root",
    password="123456",
    database="tcmdb",
    charset="utf8mb4"
)

# JWT认证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1] if len(request.headers['Authorization'].split(' ')) > 1 else None
        
        if not token:
            return jsonify({"success": False, "msg": "需要登录"}), 401
        
        try:
            # 验证token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "msg": "登录已过期，请重新登录"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "msg": "无效的登录凭证"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/user/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        phonenumber = data.get('phonenumber')
        email = data.get('email')
        password = data.get('password')

        # 验证参数
        if not all([username, phonenumber, email, password]):
            return jsonify({"success": False, "msg": "参数不全"})

        # 检查用户是否已存在
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id FROM user WHERE (username=%s OR phonenumber=%s OR email=%s) AND is_deleted=0",
            (username, phonenumber, email)
        )
        if cursor.fetchone():
            return jsonify({"success": False, "msg": "用户已存在"})

        # 密码加密
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)

        # 插入新用户
        cursor.execute(
            "INSERT INTO user (username, phonenumber, email, password) VALUES (%s, %s, %s, %s)",
            (username, phonenumber, email, hashed_password)
        )
        connection.commit()

        return jsonify({"success": True, "msg": "注册成功"})

    except Exception as e:
        print(f"注册错误: {e}")
        return jsonify({"success": False, "msg": str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.json
        account = data.get('account')
        password = data.get('password')

        if not account or not password:
            return jsonify({"success": False, "msg": "参数不全"})

        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE (username=%s OR phonenumber=%s) AND is_deleted=0",
            (account, account)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "msg": "账号不存在"})

        if not check_password_hash(user['password'], password):
            return jsonify({"success": False, "msg": "密码错误"})

        # 移除密码字段
        user.pop('password')
        
        # 生成JWT令牌
        token = jwt.encode(
            {
                'user_id': user['id'],
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=JWT_EXPIRATION)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        return jsonify({"success": True, "msg": "登录成功", "data": user, "token": token})

    except Exception as e:
        print(f"登录错误: {e}")
        return jsonify({"success": False, "msg": str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 获取评论
@app.route('/comments', methods=['GET'])
@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 获取userId参数
        user_id = request.args.get('userId')
        print(f"[DEBUG] 获取评论，userId参数: {user_id}, 类型: {type(user_id)}")
        
        # 构建SQL查询
        sql = """
            SELECT c.id, c.content, c.created_at, c.parent_id, c.reply_to_username, c.is_top,
                   u.username, u.id as user_id
            FROM comments c
            LEFT JOIN user u ON c.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        # 如果提供了userId参数，添加到WHERE子句
        if user_id is not None:
            # 确保user_id是整数
            try:
                user_id = int(user_id)
                print(f"[DEBUG] 转换后的user_id: {user_id}")
                sql += " AND c.user_id = %s"
                params.append(user_id)
            except ValueError:
                print(f"[DEBUG] userId参数不是有效整数: {user_id}")
                return jsonify({"success": False, "msg": "userId参数无效"})
        
        sql += " ORDER BY c.is_top DESC, c.created_at DESC"
        cursor.execute(sql, params)
        print(f"[DEBUG] 执行的SQL: {sql}, 参数: {params}")
        
        rows = cursor.fetchall()
        print(f"[DEBUG] 查询结果数量: {len(rows)}")
        
        # 转换datetime对象为字符串
        for row in rows:
            if 'created_at' in row and row['created_at']:
                row['created_at'] = row['created_at'].isoformat()
        
        return jsonify({"success": True, "data": rows, "debug": {"userId": user_id, "query": sql, "params": params}})
        
    except Exception as e:
        print(f"获取评论错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "msg": str(e), "error": traceback.format_exc()})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/comments', methods=['POST'])
@app.route('/api/comments', methods=['POST'])
@token_required
def post_comment():
    try:
        data = request.json
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        content = data.get('content')
        parent_id = data.get('parentId')
        reply_to_username = data.get('replyToUsername')
        
        if not content:
            return jsonify({"success": False, "msg": "评论内容不能为空"})
        
        # 情感分析
        from snownlp import SnowNLP
        s = SnowNLP(content)
        score = s.sentiments
        # 计算情感标签
        if score >= 0.55:
            sentiment = 'positive'
        elif score <= 0.45:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        connection = pool.get_connection()
        cursor = connection.cursor()
        
        # 插入评论，包含情感分析字段
        insert_sql = """
            INSERT INTO comments (user_id, content, parent_id, reply_to_username, sentiment, sentiment_score) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, [
            user_id, content, parent_id, reply_to_username, sentiment, score
        ])
        connection.commit()
        
        # 查询新创建的评论
        new_comment_id = cursor.lastrowid
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, c.parent_id, c.reply_to_username,
                   u.username, u.id as user_id
            FROM comments c
            LEFT JOIN user u ON c.user_id = u.id
            WHERE c.id = %s
        """, [new_comment_id])
        new_comment = cursor.fetchone()
        
        # 转换为字典格式
        comment_dict = {
            'id': new_comment[0],
            'content': new_comment[1],
            'created_at': new_comment[2].isoformat() if new_comment[2] else None,
            'parent_id': new_comment[3],
            'reply_to_username': new_comment[4],
            'username': new_comment[5],
            'user_id': new_comment[6]
        }
        
        return jsonify({"success": True, "msg": "发布成功", "data": comment_dict})
        
    except Exception as e:
        print(f"发表评论错误: {e}")
        return jsonify({"success": False, "msg": str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 个人信息管理接口
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    try:
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 查询用户的个人信息
        sql = """
            SELECT * FROM user_profiles 
            WHERE user_id = %s
        """
        cursor.execute(sql, [user_id])
        profile = cursor.fetchone()
        
        if profile:
            # 转换datetime对象为字符串
            if 'created_at' in profile and profile['created_at']:
                profile['created_at'] = profile['created_at'].isoformat()
            if 'updated_at' in profile and profile['updated_at']:
                profile['updated_at'] = profile['updated_at'].isoformat()
        else:
            # 初始化空的个人信息
            profile = {
                'age': '',
                'sex': '',
                'height': '',
                'weight': ''
            }
        
        return jsonify({"success": True, "data": profile})
        
    except Exception as e:
        print(f"获取个人信息错误: {e}")
        return jsonify({"success": False, "msg": str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/api/profile', methods=['POST'])
@token_required
def save_profile():
    try:
        data = request.json
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        print(f"[DEBUG] 保存个人信息，用户ID: {user_id}, 请求数据: {data}")
        
        # 提取并验证数据
        age = data.get('age', 0)
        sex = data.get('sex', '')
        height = data.get('height', 0)
        weight = data.get('weight', 0)
        
        # 数据类型转换
        try:
            age = int(age) if age else 0
            height = float(height) if height else 0
            weight = float(weight) if weight else 0
        except (ValueError, TypeError) as e:
            print(f"[ERROR] 数据类型转换错误: {e}")
            return jsonify({"success": False, "msg": "数据格式错误: " + str(e)})
        
        print(f"[DEBUG] 转换后的数据: age={age}, sex={sex}, height={height}, weight={weight}")
        
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)  # 获取字典格式的结果
        
        # 先检查是否已存在记录
        check_sql = "SELECT id FROM user_profiles WHERE user_id = %s"
        cursor.execute(check_sql, [user_id])
        existing = cursor.fetchone()
        
        # 重新创建普通游标用于更新操作
        cursor_update = connection.cursor()
        
        if existing:
            # 更新现有记录
            update_sql = """
                UPDATE user_profiles 
                SET age = %s, sex = %s, height = %s, weight = %s
                WHERE user_id = %s
            """
            cursor_update.execute(update_sql, [age, sex, height, weight, user_id])
            print(f"[DEBUG] 更新个人信息，影响行数: {cursor_update.rowcount}")
        else:
            # 插入新记录
            insert_sql = """
                INSERT INTO user_profiles (user_id, age, sex, height, weight)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor_update.execute(insert_sql, [user_id, age, sex, height, weight])
            print(f"[DEBUG] 插入个人信息，新记录ID: {cursor_update.lastrowid}")
        
        connection.commit()
        cursor_update.close()
        
        # 返回更新后的个人信息
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = %s", [user_id])
        updated_profile = cursor.fetchone()
        
        if updated_profile:
            # 转换datetime对象为字符串
            if 'created_at' in updated_profile and updated_profile['created_at']:
                updated_profile['created_at'] = updated_profile['created_at'].isoformat()
            if 'updated_at' in updated_profile and updated_profile['updated_at']:
                updated_profile['updated_at'] = updated_profile['updated_at'].isoformat()
            
            return jsonify({"success": True, "msg": "个人信息保存成功", "data": updated_profile})
        else:
            return jsonify({"success": True, "msg": "个人信息保存成功"})
        
    except Exception as e:
        print(f"[ERROR] 保存个人信息失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "msg": "保存失败: " + str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile():
    try:
        data = request.json
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        age = data.get('age')
        sex = data.get('sex')
        height = data.get('height')
        weight = data.get('weight')
        
        connection = pool.get_connection()
        cursor = connection.cursor()
        
        # 更新用户的个人信息
        sql = """
            UPDATE user_profiles 
            SET age = %s, sex = %s, height = %s, weight = %s
            WHERE user_id = %s
        """
        cursor.execute(sql, [
            age or 0, sex, height or 0, weight or 0, user_id
        ])
        connection.commit()
        
        # 如果没有更新到记录，说明用户还没有个人信息，插入新记录
        if cursor.rowcount == 0:
            insert_sql = """
                INSERT INTO user_profiles (user_id, age, sex, height, weight)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, [
                user_id, age or 0, sex, height or 0, weight or 0
            ])
            connection.commit()
        
        return jsonify({"success": True, "msg": "个人信息更新成功"})
        
    except Exception as e:
        print(f"更新个人信息失败: {e}")
        return jsonify({"success": False, "msg": "服务器错误: " + str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/api/profile', methods=['DELETE'])
@token_required
def delete_profile():
    try:
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        
        connection = pool.get_connection()
        cursor = connection.cursor()
        
        # 删除用户的个人信息记录
        sql = "DELETE FROM user_profiles WHERE user_id = %s"
        cursor.execute(sql, [user_id])
        connection.commit()
        
        return jsonify({"success": True, "msg": "个人信息删除成功"})
        
    except Exception as e:
        print(f"删除个人信息失败: {e}")
        return jsonify({"success": False, "msg": "服务器错误: " + str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 删除评论
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    try:
        user_id = g.current_user_id  # 从g对象获取当前登录用户ID
        
        connection = pool.get_connection()
        cursor = connection.cursor()
        
        # 检查评论是否存在且属于当前用户
        cursor.execute("SELECT id, user_id FROM comments WHERE id = %s", [comment_id])
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"success": False, "msg": "评论不存在"})
        
        # 只有评论作者可以删除评论
        if comment[1] != user_id:
            return jsonify({"success": False, "msg": "无权删除该评论"})
        
        # 删除评论
        cursor.execute("DELETE FROM comments WHERE id = %s", [comment_id])
        connection.commit()
        
        return jsonify({"success": True, "msg": "评论删除成功"})
        
    except Exception as e:
        print(f"删除评论失败: {e}")
        return jsonify({"success": False, "msg": "服务器错误: " + str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
