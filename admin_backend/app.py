# admin_backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from neo4j import GraphDatabase, basic_auth
from functools import wraps
import logging
import os
import subprocess
import sys
from datetime import datetime
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # 启用CORS


# ============================== 数据库连接 ==============================

class Database:
    """数据库连接管理类"""

    def __init__(self):
        self.mysql_conn = None
        self.neo4j_driver = None
        self.connect()

    def connect(self):
        """连接MySQL和Neo4j数据库"""
        try:
            # MySQL连接
            self.mysql_conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DATABASE'],
                charset=app.config['MYSQL_CHARSET']
            )
            logger.info("✅ MySQL连接成功")

            # Neo4j连接
            self.neo4j_driver = GraphDatabase.driver(
                app.config['NEO4J_URI'],
                auth=basic_auth(
                    app.config['NEO4J_USER'],
                    app.config['NEO4J_PASSWORD']
                )
            )
            # 测试Neo4j连接
            with self.neo4j_driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Neo4j连接成功")

        except Error as e:
            logger.error(f"❌ MySQL连接失败: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Neo4j连接失败: {e}")
            raise

    def get_mysql_cursor(self):
        """获取MySQL游标"""
        if not self.mysql_conn or not self.mysql_conn.is_connected():
            self.connect()
        return self.mysql_conn.cursor(dictionary=True)

    def get_neo4j_session(self):
        """获取Neo4j会话"""
        if not self.neo4j_driver:
            self.connect()
        return self.neo4j_driver.session()

    def close(self):
        """关闭数据库连接"""
        if self.mysql_conn and self.mysql_conn.is_connected():
            self.mysql_conn.close()
            logger.info("✅ MySQL连接已关闭")

        if self.neo4j_driver:
            self.neo4j_driver.close()
            logger.info("✅ Neo4j连接已关闭")


# 全局数据库实例
db = Database()


# ============================== 装饰器和辅助函数 ==============================

def check_admin(f):
    """管理员权限校验装饰器"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'success': False, 'msg': '请携带管理员令牌'}), 401

        try:
            token = auth_header.split(' ')[1]
            if token != app.config['ADMIN_TOKEN']:
                return jsonify({'success': False, 'msg': '管理员令牌无效，无访问权限'}), 403
        except IndexError:
            return jsonify({'success': False, 'msg': '令牌格式错误'}), 400

        return f(*args, **kwargs)

    return decorated_function


def run_sentiment_analysis(content):
    """运行情感分析脚本"""
    try:
        # 获取当前目录路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'analysis.py')

        # 清理内容，防止命令行问题
        safe_content = content.replace('"', '\\"').replace('\n', ' ').replace('\r', ' ')

        # 执行Python脚本
        cmd = f'{app.config["PYTHON_PATH"]} "{script_path}" "{safe_content}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                score = float(result.stdout.strip())
                return score
            except ValueError:
                logger.error(f"无法解析情感分析结果: {result.stdout}")
                return 0.5
        else:
            logger.error(f"情感分析脚本执行失败: {result.stderr}")
            return 0.5
    except Exception as e:
        logger.error(f"运行情感分析时出错: {e}")
        return 0.5


# ============================== 用户管理 ==============================

@app.route('/api/admin/users', methods=['GET'])
@check_admin
def get_users():
    """获取用户列表"""
    try:
        search = request.args.get('search', '').strip()
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        offset = (page - 1) * page_size

        cursor = db.get_mysql_cursor()

        # 构建查询条件 - 只返回普通用户(role='user')
        where_clause = "WHERE is_deleted = 0 AND role = 'user'"
        params = []

        if search:
            where_clause += " AND (username LIKE %s OR phonenumber LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])

        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM user {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # 查询数据
        data_sql = f"""
            SELECT id, username, phonenumber, email, role, is_deleted, created_at, updated_at
            FROM user
            {where_clause}
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cursor.execute(data_sql, params)
        users = cursor.fetchall()

        cursor.close()

        return jsonify({
            'success': True,
            'data': users,
            'total': total,
            'msg': '获取用户列表成功'
        })

    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取用户列表失败: {str(e)}'}), 500


@app.route('/api/admin/users/<int:user_id>/delete', methods=['PUT'])
@check_admin
def delete_user(user_id):
    """逻辑删除用户"""
    try:
        cursor = db.get_mysql_cursor()
        
        # 1. 检查要删除的用户是否是admin用户
        cursor.execute("SELECT username FROM user WHERE id = %s AND is_deleted = 0", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            return jsonify({'success': False, 'msg': '该用户不存在或已被删除'}), 404
        
        # 2. 防止删除admin用户
        if user['username'] == 'admin':
            cursor.close()
            return jsonify({'success': False, 'msg': '管理员用户不能被删除'}), 403
        
        # 3. 执行删除操作
        sql = "UPDATE user SET is_deleted = 1 WHERE id = %s AND is_deleted = 0"
        cursor.execute(sql, (user_id,))
        db.mysql_conn.commit()

        cursor.close()
        return jsonify({'success': True, 'msg': '用户删除成功'})

    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        return jsonify({'success': False, 'msg': f'删除用户失败: {str(e)}'}), 500


# ============================== 药材管理 ==============================

@app.route('/api/admin/herbs', methods=['GET'])
@check_admin
def get_herbs():
    """获取药材列表"""
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        skip = max(0, (page - 1) * page_size)
        limit = max(1, page_size)

        session = db.get_neo4j_session()

        # 总数查询
        count_query = """
            MATCH (h:Herb)
            WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
            RETURN count(h) as total
        """
        count_result = session.run(count_query, {'search': search})
        count_record = count_result.single()
        total = count_record['total'] if count_record else 0

        # 列表查询
        list_query = """
            MATCH (h:Herb)
            WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
            RETURN id(h) as id, h.herb_id as herb_id, h.name as name, h.source_list as source_list
            ORDER BY h.name
            SKIP $skip LIMIT $limit
        """
        list_result = session.run(list_query, {
            'search': search,
            'skip': skip,
            'limit': limit
        })

        data = []
        for record in list_result:
            data.append({
                'id': record['id'],
                'herb_id': record.get('herb_id', ''),
                'name': record.get('name', ''),
                'source_list': record.get('source_list', '')
            })

        session.close()

        return jsonify({
            'success': True,
            'data': data,
            'total': total,
            'msg': '获取药材列表成功'
        })

    except Exception as e:
        logger.error(f"获取药材列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取药材列表失败: {str(e)}'}), 500


@app.route('/api/admin/herbs/<int:herb_id>', methods=['GET'])
@check_admin
def get_herb_detail(herb_id):
    """获取药材详情"""
    try:
        session = db.get_neo4j_session()

        query = """
            MATCH (h:Herb)
            WHERE id(h) = $id
            OPTIONAL MATCH (h)-[:FROM_SOURCE]->(a:Attributes)
            RETURN
                h.herb_id as herb_id,
                h.name as name,
                h.source_list as source_list,
                h.alias as alias,
                h.function as function,
                h.original_form as original_form,
                h.taste as taste,
                h.caution as caution,
                h.habitat as habitat,
                h.usage_dosage as usage_dosage,

                COALESCE(a.功能主治, '') as 功能主治,
                COALESCE(a.性味, '') as 性味,
                COALESCE(a.性味归经, '') as 性味归经,
                COALESCE(a.归经, '') as 归经,
                COALESCE(a.英文名, '') as 英文名,
                COALESCE(a.化学成分, '') as 化学成分,
                COALESCE(a.药理作用, '') as 药理作用,
                COALESCE(a.临床应用, '') as 临床应用,
                COALESCE(a.毒性, '') as 毒性,
                COALESCE(a.植物形态, '') as 植物形态,
                COALESCE(a.动物形态, '') as 动物形态,
                COALESCE(a.药用部位, '') as 药用部位,
                COALESCE(a.采收加工, '') as 采收加工,
                COALESCE(a.炮制, '') as 炮制,
                COALESCE(a.制剂, '') as 制剂,
                COALESCE(a.性状, '') as 性状,
                COALESCE(a.鉴别, '') as 鉴别,
                COALESCE(a.含量测定, '') as 含量测定,
                COALESCE(a.注意, '') as 注意,
                COALESCE(a.贮藏, '') as 贮藏,
                COALESCE(a.备注, '') as 备注,
                COALESCE(a.各家论述, '') as 各家论述,
                COALESCE(a.相关药方, '') as 相关药方,
                COALESCE(a.复方, '') as 复方,
                COALESCE(a.拼音注音, '') as 拼音注音,
                COALESCE(a.原形态, '') as 原形态,
                COALESCE(a.生境分布, '') as 生境分布,
                COALESCE(a.主要成分, '') as 主要成分,
                COALESCE(a.规格, '') as 规格,
                COALESCE(a.制法, '') as 制法,
                COALESCE(a.栽培, '') as 栽培
        """

        result = session.run(query, {'id': herb_id})
        record = result.single()

        if not record:
            session.close()
            return jsonify({'success': False, 'msg': '药材不存在'}), 404

        # 构建响应数据
        herb = {
            'id': herb_id,
            'herb_id': record.get('herb_id', ''),
            'name': record.get('name', ''),
            'source_list': record.get('source_list', ''),
            'alias': record.get('alias', ''),
            'function': record.get('function', ''),
            'original_form': record.get('original_form', ''),
            'taste': record.get('taste', ''),
            'caution': record.get('caution', ''),
            'habitat': record.get('habitat', ''),
            'usage_dosage': record.get('usage_dosage', ''),

            # Attributes字段
            '功能主治': record.get('功能主治', ''),
            '性味': record.get('性味', ''),
            '性味归经': record.get('性味归经', ''),
            '归经': record.get('归经', ''),
            '英文名': record.get('英文名', ''),
            '化学成分': record.get('化学成分', ''),
            '药理作用': record.get('药理作用', ''),
            '临床应用': record.get('临床应用', ''),
            '毒性': record.get('毒性', ''),
            '植物形态': record.get('植物形态', ''),
            '动物形态': record.get('动物形态', ''),
            '药用部位': record.get('药用部位', ''),
            '采收加工': record.get('采收加工', ''),
            '炮制': record.get('炮制', ''),
            '制剂': record.get('制剂', ''),
            '性状': record.get('性状', ''),
            '鉴别': record.get('鉴别', ''),
            '含量测定': record.get('含量测定', ''),
            '注意': record.get('注意', ''),
            '贮藏': record.get('贮藏', ''),
            '备注': record.get('备注', ''),
            '各家论述': record.get('各家论述', ''),
            '相关药方': record.get('相关药方', ''),
            '复方': record.get('复方', ''),
            '拼音注音': record.get('拼音注音', ''),
            '原形态': record.get('原形态', ''),
            '生境分布': record.get('生境分布', ''),
            '主要成分': record.get('主要成分', ''),
            '规格': record.get('规格', ''),
            '制法': record.get('制法', ''),
            '栽培': record.get('栽培', '')
        }

        session.close()
        return jsonify({'success': True, 'data': herb, 'msg': '获取药材详情成功'})

    except Exception as e:
        logger.error(f"获取药材详情失败: {e}")
        return jsonify({'success': False, 'msg': f'获取药材详情失败: {str(e)}'}), 500


@app.route('/api/admin/herbs', methods=['POST'])
@check_admin
def create_herb():
    """新增药材"""
    try:
        data = request.json

        # 验证必填字段
        required_fields = ['herb_id', 'name', 'source_list']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'msg': f'{field}为必填项'}), 400

        session = db.get_neo4j_session()

        # 检查药材ID和名称是否已存在
        id_check = session.run(
            'MATCH (h:Herb {herb_id: $herb_id}) RETURN h LIMIT 1',
            {'herb_id': data['herb_id']}
        )
        if id_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材ID已存在'}), 400

        name_check = session.run(
            'MATCH (h:Herb {name: $name}) RETURN h LIMIT 1',
            {'name': data['name']}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材名称已存在'}), 400

        # 创建Herb节点（使用MERGE确保唯一性）
        create_query = """
            MERGE (h:Herb {herb_id: $herb_id})
            SET h.name = $name,
                h.source_list = $source_list,
                h.alias = $alias,
                h.function = $function,
                h.original_form = $original_form,
                h.taste = $taste,
                h.caution = $caution,
                h.habitat = $habitat,
                h.usage_dosage = $usage_dosage
            RETURN id(h) as herbId
        """

        herb_params = {
            'herb_id': data['herb_id'],
            'name': data['name'],
            'source_list': data['source_list'],
            'alias': data.get('alias', ''),
            'function': data.get('function', ''),
            'original_form': data.get('original_form', ''),
            'taste': data.get('taste', ''),
            'caution': data.get('caution', ''),
            'habitat': data.get('habitat', ''),
            'usage_dosage': data.get('usage_dosage', '')
        }

        herb_result = session.run(create_query, herb_params)
        herb_record = herb_result.single()

        if not herb_record:
            session.close()
            return jsonify({'success': False, 'msg': '药材创建失败'}), 500

        herb_id = herb_record['herbId']

        # 获取来源书籍，默认使用source_list的第一个值
        source_book = data.get('source_list', '').split(',')[0] if data.get('source_list') else '未知来源'

        # 创建来源节点和Attributes节点并建立关系
        attr_query = """
            MATCH (h:Herb) WHERE id(h) = $herbId
            MERGE (source:Source {name: $source_book})
            CREATE (h)-[:FROM_SOURCE {book: $source_book}]->(attrs:Attributes)
            SET attrs += $properties
        """

        attr_params = {
            'herbId': herb_id,
            'source_book': source_book,
            'properties': {
                '临床应用': data.get('临床应用', ''),
                '主要成分': data.get('主要成分', ''),
                '出处': data.get('出处', ''),
                '别名': data.get('别名', ''),
                '制剂': data.get('制剂', ''),
                '制法': data.get('制法', ''),
                '功能主治': data.get('功能主治', ''),
                '动物形态': data.get('动物形态', ''),
                '化学成分': data.get('化学成分', ''),
                '原形态': data.get('原形态', ''),
                '各家论述': data.get('各家论述', ''),
                '含量测定': data.get('含量测定', ''),
                '备注': data.get('备注', ''),
                '复方': data.get('复方', ''),
                '归经': data.get('归经', ''),
                '性味': data.get('性味', ''),
                '性味归经': data.get('性味归经', ''),
                '性状': data.get('性状', ''),
                '拼音注音': data.get('拼音注音', ''),
                '摘录': data.get('摘录', ''),
                '来源': data.get('来源', ''),
                '栽培': data.get('栽培', ''),
                '植物形态': data.get('植物形态', ''),
                '毒性': data.get('毒性', ''),
                '注意': data.get('注意', ''),
                '炮制': data.get('炮制', ''),
                '生境分布': data.get('生境分布', ''),
                '用法用量': data.get('用法用量', ''),
                '相关药方': data.get('相关药方', ''),
                '英文名': data.get('英文名', ''),
                '药理作用': data.get('药理作用', ''),
                '药用部位': data.get('药用部位', ''),
                '规格': data.get('规格', ''),
                '贮藏': data.get('贮藏', ''),
                '采收加工': data.get('采收加工', ''),
                '鉴别': data.get('鉴别', '')
            }
        }

        session.run(attr_query, attr_params)
        session.close()

        return jsonify({
            'success': True,
            'msg': '药材新增成功',
            'data': {'id': herb_id}
        })

    except Exception as e:
        logger.error(f"新增药材失败: {e}")
        return jsonify({'success': False, 'msg': f'新增药材失败: {str(e)}'}), 500


@app.route('/api/admin/herbs/<int:herb_id>', methods=['PUT'])
@check_admin
def update_herb(herb_id):
    """修改药材"""
    try:
        data = request.json

        # 验证必填字段
        required_fields = ['herb_id', 'name', 'source_list']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'msg': f'{field}为必填项'}), 400

        session = db.get_neo4j_session()

        # 检查药材是否存在
        herb_exist = session.run(
            'MATCH (h:Herb) WHERE id(h) = $id RETURN h',
            {'id': herb_id}
        )
        if not herb_exist.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材不存在'}), 404

        # 检查ID和名称唯一性
        id_check = session.run(
            'MATCH (h:Herb {herb_id: $herb_id}) WHERE id(h) <> $id RETURN h LIMIT 1',
            {'herb_id': data['herb_id'], 'id': herb_id}
        )
        if id_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材ID已被占用'}), 400

        name_check = session.run(
            'MATCH (h:Herb {name: $name}) WHERE id(h) <> $id RETURN h LIMIT 1',
            {'name': data['name'], 'id': herb_id}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材名称已被占用'}), 400

        # 更新Herb节点
        update_herb_query = """
            MATCH (h:Herb)
            WHERE id(h) = $id
            SET h.herb_id = $herb_id,
                h.name = $name,
                h.source_list = $source_list,
                h.alias = $alias,
                h.function = $function,
                h.original_form = $original_form,
                h.taste = $taste,
                h.caution = $caution,
                h.habitat = $habitat,
                h.usage_dosage = $usage_dosage
        """

        herb_params = {
            'id': herb_id,
            'herb_id': data['herb_id'],
            'name': data['name'],
            'source_list': data['source_list'],
            'alias': data.get('alias', ''),
            'function': data.get('function', ''),
            'original_form': data.get('original_form', ''),
            'taste': data.get('taste', ''),
            'caution': data.get('caution', ''),
            'habitat': data.get('habitat', ''),
            'usage_dosage': data.get('usage_dosage', '')
        }

        session.run(update_herb_query, herb_params)

        # 获取来源书籍，默认使用source_list的第一个值
        source_book = data.get('source_list', '').split(',')[0] if data.get('source_list') else '未知来源'

        # 构建Attributes属性字典
        attr_properties = {
            '临床应用': data.get('临床应用', ''),
            '主要成分': data.get('主要成分', ''),
            '出处': data.get('出处', ''),
            '别名': data.get('别名', ''),
            '制剂': data.get('制剂', ''),
            '制法': data.get('制法', ''),
            '功能主治': data.get('功能主治', ''),
            '动物形态': data.get('动物形态', ''),
            '化学成分': data.get('化学成分', ''),
            '原形态': data.get('原形态', ''),
            '各家论述': data.get('各家论述', ''),
            '含量测定': data.get('含量测定', ''),
            '备注': data.get('备注', ''),
            '复方': data.get('复方', ''),
            '归经': data.get('归经', ''),
            '性味': data.get('性味', ''),
            '性味归经': data.get('性味归经', ''),
            '性状': data.get('性状', ''),
            '拼音注音': data.get('拼音注音', ''),
            '摘录': data.get('摘录', ''),
            '来源': data.get('来源', ''),
            '栽培': data.get('栽培', ''),
            '植物形态': data.get('植物形态', ''),
            '毒性': data.get('毒性', ''),
            '注意': data.get('注意', ''),
            '炮制': data.get('炮制', ''),
            '生境分布': data.get('生境分布', ''),
            '用法用量': data.get('用法用量', ''),
            '相关药方': data.get('相关药方', ''),
            '英文名': data.get('英文名', ''),
            '药理作用': data.get('药理作用', ''),
            '药用部位': data.get('药用部位', ''),
            '规格': data.get('规格', ''),
            '贮藏': data.get('贮藏', ''),
            '采收加工': data.get('采收加工', ''),
            '鉴别': data.get('鉴别', '')
        }

        # 检查并更新Attributes节点
        attr_exist = session.run(
            'MATCH (h:Herb)-[r:FROM_SOURCE]->(a:Attributes) WHERE id(h) = $id RETURN a',
            {'id': herb_id}
        )

        if attr_exist.single():
            # 更新现有Attributes节点
            update_attr_query = """
                MATCH (h:Herb)-[r:FROM_SOURCE]->(a:Attributes)
                WHERE id(h) = $id
                SET r.book = $source_book,
                    a += $properties
            """
            session.run(update_attr_query, {
                'id': herb_id,
                'source_book': source_book,
                'properties': attr_properties
            })
        else:
            # 创建新的Source节点和Attributes节点并建立关系
            create_attr_query = """
                MATCH (h:Herb)
                WHERE id(h) = $id
                MERGE (source:Source {name: $source_book})
                CREATE (h)-[:FROM_SOURCE {book: $source_book}]->(a:Attributes)
                SET a += $properties
            """
            session.run(create_attr_query, {
                'id': herb_id,
                'source_book': source_book,
                'properties': attr_properties
            })
        session.close()

        return jsonify({
            'success': True,
            'msg': '药材修改成功',
            'data': {'id': herb_id}
        })

    except Exception as e:
        logger.error(f"修改药材失败: {e}")
        return jsonify({'success': False, 'msg': f'修改药材失败: {str(e)}'}), 500


@app.route('/api/admin/herbs/<int:herb_id>', methods=['DELETE'])
@check_admin
def delete_herb(herb_id):
    """删除药材"""
    try:
        session = db.get_neo4j_session()

        # 检查药材是否存在
        exist_result = session.run(
            'MATCH (h:Herb) WHERE id(h) = $id RETURN h LIMIT 1',
            {'id': herb_id}
        )
        if not exist_result.single():
            session.close()
            return jsonify({'success': False, 'msg': '药材不存在'}), 404

        # 删除药材节点（会自动删除所有关联关系）
        session.run('MATCH (h:Herb) WHERE id(h) = $id DETACH DELETE h', {'id': herb_id})
        # 删除可能存在的Attributes节点（使用更通用的查询）
        session.run('MATCH (a:Attributes) WHERE NOT (a)<-[:FROM_SOURCE]-(:Herb) DETACH DELETE a', {})
        session.close()

        return jsonify({'success': True, 'msg': '药材删除成功'})

    except Exception as e:
        logger.error(f"删除药材失败: {e}")
        return jsonify({'success': False, 'msg': f'删除药材失败: {str(e)}'}), 500


# ============================== 药方管理 ==============================

@app.route('/api/admin/fangji', methods=['GET'])
@check_admin
def get_fangji_list():
    """获取药方列表"""
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        skip = max(0, (page - 1) * page_size)
        limit = max(1, page_size)

        session = db.get_neo4j_session()

        # 总数查询
        count_query = """
            MATCH (f:Fangji)
            WHERE f.name CONTAINS $search
            RETURN count(f) as total
        """
        count_result = session.run(count_query, {'search': search})
        count_record = count_result.single()
        total = count_record['total'] if count_record else 0

        # 列表查询
        list_query = """
            MATCH (f:Fangji)
            WHERE f.name CONTAINS $search
            RETURN id(f) AS id,
                   f.name AS name,
                   f.excerpt AS excerpt,
                   f.prescription AS prescription,
                   f.function AS function,
                   f.usage AS usage,
                   f.caution AS caution
            ORDER BY f.name
            SKIP $skip LIMIT $limit
        """

        list_result = session.run(list_query, {
            'search': search,
            'skip': skip,
            'limit': limit
        })

        data = []
        for record in list_result:
            data.append({
                'id': record['id'],
                'name': record.get('name', ''),
                'function': record.get('function', ''),
                'excerpt': record.get('excerpt', ''),
                'prescription': record.get('prescription', ''),
                'usage': record.get('usage', ''),
                'caution': record.get('caution', '')
            })

        session.close()

        return jsonify({
            'success': True,
            'data': data,
            'total': total,
            'msg': '获取药方列表成功'
        })

    except Exception as e:
        logger.error(f"获取药方列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取药方列表失败: {str(e)}'}), 500


@app.route('/api/admin/fangji', methods=['POST'])
@check_admin
def create_fangji():
    """新增药方"""
    try:
        data = request.json

        # 验证必填字段
        if not data.get('name'):
            return jsonify({'success': False, 'msg': '药方名称为必填项'}), 400

        if not data.get('herbIds') or len(data['herbIds']) == 0:
            return jsonify({'success': False, 'msg': '药材组成为必填项'}), 400

        session = db.get_neo4j_session()

        # 检查药方名称是否已存在
        name_check = session.run(
            'MATCH (f:Fangji {name: $name}) RETURN f LIMIT 1',
            {'name': data['name']}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药方名称已存在'}), 400

        # 检查药材是否存在
        herb_ids = [herb['id'] for herb in data['herbIds']]
        herb_check_query = """
            MATCH (h:Herb)
            WHERE id(h) IN $herbIds
            RETURN collect(id(h)) as existIds
        """
        herb_check_result = session.run(herb_check_query, {'herbIds': herb_ids})
        exist_record = herb_check_result.single()

        if not exist_record or not exist_record['existIds']:
            session.close()
            return jsonify({'success': False, 'msg': '药材ID列表为空'}), 400

        exist_ids = set(str(id) for id in exist_record['existIds'])
        invalid_ids = [herb_id for herb_id in herb_ids if str(herb_id) not in exist_ids]

        if invalid_ids:
            session.close()
            return jsonify({'success': False, 'msg': f'以下药材不存在：{invalid_ids}，请从药材库选择'}), 400

        # 创建新药方（使用MERGE确保唯一性）
        create_query = """
            MERGE (f:Fangji {name: $name})
            SET f.excerpt = $excerpt,
                f.function = $function,
                f.prescription = $prescription,
                f.usage = $usage,
                f.caution = $caution,
                f.preparation = $preparation,
                f.book = $book,
                f.since = $since
            RETURN id(f) as id
        """

        create_params = {
            'name': data['name'],
            'excerpt': data.get('excerpt', ''),
            'function': data.get('function', ''),
            'prescription': data.get('prescription', ''),
            'usage': data.get('usage', ''),
            'caution': data.get('caution', ''),
            'preparation': data.get('preparation', ''),
            'book': data.get('book', ''),
            'since': data.get('since', '')
        }

        create_result = session.run(create_query, create_params)
        created_record = create_result.single()

        if not created_record:
            session.close()
            return jsonify({'success': False, 'msg': '药方创建失败'}), 500

        fangji_id = created_record['id']

        # 创建药材关系
        for herb_item in data['herbIds']:
            relation_query = """
                MATCH (f:Fangji), (h:Herb)
                WHERE id(f) = $fangjiId AND id(h) = $herbId
                CREATE (f)-[:HAS_HERB {dosage: $dosage}]->(h)
            """
            session.run(relation_query, {
                'fangjiId': fangji_id,
                'herbId': herb_item['id'],
                'dosage': herb_item.get('dosage', '')
            })

        session.close()

        return jsonify({
            'success': True,
            'msg': '药方新增成功',
            'data': {'id': fangji_id}
        })

    except Exception as e:
        logger.error(f"新增药方失败: {e}")
        return jsonify({'success': False, 'msg': f'新增药方失败: {str(e)}'}), 500


@app.route('/api/admin/fangji/<int:fangji_id>', methods=['GET'])
@check_admin
def get_fangji_detail(fangji_id):
    """获取药方详情"""
    try:
        session = db.get_neo4j_session()

        query = """
            MATCH (f:Fangji)
            WHERE id(f) = $id
            OPTIONAL MATCH (f)-[r:HAS_HERB]->(h:Herb)
            RETURN f.name as name,
                   f.excerpt as excerpt,
                   f.function as function,
                   f.prescription as prescription,
                   f.usage as usage,
                   f.caution as caution,
                   f.preparation as preparation,
                   f.book as book,
                   f.since as since,
                   collect({
                     id: id(h),
                     herb_id: h.herb_id,
                     name: h.name,
                     dosage: r.dosage
                   }) as herbs
        """

        result = session.run(query, {'id': fangji_id})
        record = result.single()

        if not record:
            session.close()
            return jsonify({'success': False, 'msg': '药方不存在'}), 404

        herbs = []
        if record['herbs']:
            herbs = [{
                'id': herb['id'],
                'herb_id': herb.get('herb_id', ''),
                'name': herb.get('name', ''),
                'dosage': herb.get('dosage', '')
            } for herb in record['herbs']]

        fangji = {
            'id': fangji_id,
            'name': record.get('name', ''),
            'excerpt': record.get('excerpt', ''),
            'function': record.get('function', ''),
            'prescription': record.get('prescription', ''),
            'usage': record.get('usage', ''),
            'caution': record.get('caution', ''),
            'preparation': record.get('preparation', ''),
            'book': record.get('book', ''),
            'since': record.get('since', ''),
            'herbs': herbs
        }

        session.close()
        return jsonify({'success': True, 'data': fangji, 'msg': '获取药方详情成功'})

    except Exception as e:
        logger.error(f"获取药方详情失败: {e}")
        return jsonify({'success': False, 'msg': f'获取药方详情失败: {str(e)}'}), 500


@app.route('/api/admin/fangji/<int:fangji_id>', methods=['PUT'])
@check_admin
def update_fangji(fangji_id):
    """修改药方"""
    try:
        data = request.json

        if not data.get('name'):
            return jsonify({'success': False, 'msg': '药方名称为必填项'}), 400

        session = db.get_neo4j_session()

        # 检查药方是否存在
        fangji_exist = session.run(
            'MATCH (f:Fangji) WHERE id(f) = $id RETURN f LIMIT 1',
            {'id': fangji_id}
        )
        if not fangji_exist.single():
            session.close()
            return jsonify({'success': False, 'msg': '药方不存在'}), 404

        # 检查药方名称是否被其他药方使用
        name_check = session.run(
            'MATCH (f:Fangji {name: $name}) WHERE id(f) <> $id RETURN f LIMIT 1',
            {'name': data['name'], 'id': fangji_id}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '药方名称已被占用'}), 400

        # 更新药方基本信息
        update_query = """
            MATCH (f:Fangji)
            WHERE id(f) = $id
            SET f.name = $name,
                f.excerpt = $excerpt,
                f.function = $function,
                f.prescription = $prescription,
                f.usage = $usage,
                f.caution = $caution,
                f.preparation = $preparation,
                f.book = $book,
                f.since = $since
        """

        update_params = {
            'id': fangji_id,
            'name': data['name'],
            'excerpt': data.get('excerpt', ''),
            'function': data.get('function', ''),
            'prescription': data.get('prescription', ''),
            'usage': data.get('usage', ''),
            'caution': data.get('caution', ''),
            'preparation': data.get('preparation', ''),
            'book': data.get('book', ''),
            'since': data.get('since', '')
        }

        session.run(update_query, update_params)

        # 如果有药材信息，更新药材关系
        if data.get('herbIds') and len(data['herbIds']) > 0:
            # 检查药材是否存在
            herb_ids = [herb['id'] for herb in data['herbIds']]
            herb_check_query = """
                MATCH (h:Herb)
                WHERE id(h) IN $herbIds
                RETURN collect(id(h)) as existIds
            """
            herb_check_result = session.run(herb_check_query, {'herbIds': herb_ids})
            exist_record = herb_check_result.single()

            if exist_record and exist_record['existIds']:
                exist_ids = set(str(id) for id in exist_record['existIds'])
                invalid_ids = [herb_id for herb_id in herb_ids if str(herb_id) not in exist_ids]

                if not invalid_ids:
                    # 删除旧的药材关系
                    delete_relations_query = """
                        MATCH (f:Fangji)-[r:HAS_HERB]->(:Herb)
                        WHERE elementId(f) = $id
                        DELETE r
                    """
                    session.run(delete_relations_query, {'id': fangji_id})

                    # 创建新的药材关系
                    for herb_item in data['herbIds']:
                        relation_query = """
                            MATCH (f:Fangji), (h:Herb)
                        WHERE id(f) = $fangjiId AND id(h) = $herbId
                        CREATE (f)-[:HAS_HERB {dosage: $dosage}]->(h)
                        """
                        session.run(relation_query, {
                            'fangjiId': fangji_id,
                            'herbId': herb_item['id'],
                            'dosage': herb_item.get('dosage', '')
                        })

        session.close()

        return jsonify({
            'success': True,
            'msg': '药方修改成功',
            'data': {'id': fangji_id}
        })

    except Exception as e:
        logger.error(f"修改药方失败: {e}")
        return jsonify({'success': False, 'msg': f'修改药方失败: {str(e)}'}), 500


@app.route('/api/admin/fangji/<int:fangji_id>', methods=['DELETE'])
@check_admin
def delete_fangji(fangji_id):
    """删除药方"""
    try:
        session = db.get_neo4j_session()

        # 检查药方是否存在
        exist_result = session.run(
            'MATCH (f:Fangji) WHERE id(f) = $id RETURN f LIMIT 1',
            {'id': fangji_id}
        )
        if not exist_result.single():
            session.close()
            return jsonify({'success': False, 'msg': '药方不存在'}), 404

        # 删除药方及其所有关系
        delete_query = """
            MATCH (f:Fangji)
            WHERE id(f) = $id
            DETACH DELETE f
        """
        session.run(delete_query, {'id': fangji_id})
        session.close()

        return jsonify({'success': True, 'msg': '药方删除成功'})

    except Exception as e:
        logger.error(f"删除药方失败: {e}")
        return jsonify({'success': False, 'msg': f'删除药方失败: {str(e)}'}), 500
# ============================== 来源管理 ==============================

@app.route('/api/admin/sources', methods=['GET'])
@check_admin
def get_sources():
    """获取来源列表"""
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        skip = max(0, (page - 1) * page_size)
        limit = max(1, page_size)

        session = db.get_neo4j_session()

        # 总数查询
        count_query = "MATCH (s:Source) WHERE s.name CONTAINS $search RETURN count(s) as total"
        count_result = session.run(count_query, {'search': search})
        count_record = count_result.single()
        total = count_record['total'] if count_record else 0

        # 列表查询
        list_query = """
            MATCH (s:Source)
            WHERE s.name CONTAINS $search
            RETURN id(s) as id, s.name as name
            ORDER BY s.name
            SKIP $skip LIMIT $limit
        """

        list_result = session.run(list_query, {
            'search': search,
            'skip': skip,
            'limit': limit
        })

        data = []
        for record in list_result:
            data.append({
                'id': record['id'],
                'name': record.get('name', '')
            })

        session.close()

        return jsonify({
            'success': True,
            'data': data,
            'total': total,
            'msg': '获取来源列表成功'
        })

    except Exception as e:
        logger.error(f"获取来源列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取来源列表失败: {str(e)}'}), 500





@app.route('/api/admin/sources', methods=['POST'])
@check_admin
def create_source():
    """新增来源"""
    try:
        data = request.json
        name = data.get('name', '').strip()

        if not name:
            return jsonify({'success': False, 'msg': '来源名称不能为空'}), 400

        session = db.get_neo4j_session()

        # 检查来源名称是否已存在
        name_check = session.run(
            'MATCH (s:Source {name: $name}) RETURN s LIMIT 1',
            {'name': name}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '来源名称已存在'}), 400

        # 创建来源节点
        create_result = session.run(
            'CREATE (s:Source {name: $name}) RETURN id(s) as id',
            {'name': name}
        )

        source_record = create_result.single()
        if not source_record:
            session.close()
            return jsonify({'success': False, 'msg': '来源创建失败'}), 500

        source_id = source_record['id']
        session.close()

        return jsonify({
            'success': True,
            'msg': '来源新增成功',
            'data': {'id': source_id}
        })

    except Exception as e:
        logger.error(f"新增来源失败: {e}")
        return jsonify({'success': False, 'msg': f'新增来源失败: {str(e)}'}), 500


@app.route('/api/admin/sources/<int:source_id>', methods=['PUT'])
@check_admin
def update_source(source_id):
    """修改来源"""
    try:
        data = request.json
        name = data.get('name', '').strip()

        if not name:
            return jsonify({'success': False, 'msg': '来源名称不能为空'}), 400

        session = db.get_neo4j_session()

        # 检查来源是否存在
        source_exist = session.run(
            'MATCH (s:Source) WHERE id(s) = $id RETURN s',
            {'id': source_id}
        )
        if not source_exist.single():
            session.close()
            return jsonify({'success': False, 'msg': '来源不存在'}), 404

        # 检查名称是否被其他来源使用
        name_check = session.run(
            'MATCH (s:Source {name: $name}) WHERE id(s) <> $id RETURN s LIMIT 1',
            {'name': name, 'id': source_id}
        )
        if name_check.single():
            session.close()
            return jsonify({'success': False, 'msg': '来源名称已被占用'}), 400

        # 更新来源
        session.run(
            'MATCH (s:Source) WHERE id(s) = $id SET s.name = $name',
            {'id': source_id, 'name': name}
        )
        session.close()

        return jsonify({'success': True, 'msg': '来源修改成功'})

    except Exception as e:
        logger.error(f"修改来源失败: {e}")
        return jsonify({'success': False, 'msg': f'修改来源失败: {str(e)}'}), 500


@app.route('/api/admin/sources/<int:source_id>', methods=['DELETE'])
@check_admin
def delete_source(source_id):
    """删除来源"""
    try:
        session = db.get_neo4j_session()

        # 检查来源是否存在
        exist_result = session.run(
            'MATCH (s:Source) WHERE id(s) = $id RETURN s LIMIT 1',
            {'id': source_id}
        )
        if not exist_result.single():
            session.close()
            return jsonify({'success': False, 'msg': '来源不存在'}), 404

        # 检查是否有药材引用此来源
        herb_ref_check = session.run(
            'MATCH (h:Herb)-[:FROM_SOURCE]->(s:Source) WHERE id(s) = $id RETURN h LIMIT 1',
            {'id': source_id}
        )
        if herb_ref_check.single():
            session.close()
            return jsonify({
                'success': False,
                'msg': '无法删除该来源，已有药材引用此来源，请先修改相关药材的来源引用'
            }), 400

        # 删除来源
        session.run(
            'MATCH (s:Source) WHERE id(s) = $id DETACH DELETE s',
            {'id': source_id}
        )
        session.close()

        return jsonify({'success': True, 'msg': '来源删除成功'})

    except Exception as e:
        logger.error(f"删除来源失败: {e}")
        return jsonify({'success': False, 'msg': f'删除来源失败: {str(e)}'}), 500

# ============================== 评论管理 ==============================

@app.route('/api/admin/comments', methods=['GET'])
@check_admin
def get_comments():
    """获取评论列表"""
    try:
        cursor = db.get_mysql_cursor()
        
        # 检查comments表是否有is_top字段，如果没有则添加
        cursor.execute("SHOW COLUMNS FROM comments LIKE 'is_top'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE comments ADD COLUMN is_top INT DEFAULT 0 COMMENT '是否置顶：1-置顶，0-不置顶'")
            db.mysql_conn.commit()

        sql = """
            SELECT c.*, u.username
            FROM comments c
            LEFT JOIN user u ON c.user_id = u.id
            ORDER BY c.is_top DESC, c.created_at DESC
        """
        cursor.execute(sql)
        comments = cursor.fetchall()
        cursor.close()

        return jsonify({'success': True, 'data': comments})

    except Exception as e:
        logger.error(f"获取评论列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取评论列表失败: {str(e)}'}), 500

@app.route('/api/admin/comments', methods=['POST'])
@check_admin
def create_comment():
    """创建评论，默认管理员发布"""
    try:
        data = request.json
        content = data.get('content')
        
        if not content:
            return jsonify({'success': False, 'msg': '内容不能为空'}), 400
        
        # 运行情感分析
        score = run_sentiment_analysis(content)
        
        # 计算情感标签
        if score >= 0.55:
            sentiment = 'positive'
        elif score <= 0.45:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        cursor = db.get_mysql_cursor()
        
        # 检查comments表是否有is_top字段，如果没有则添加
        cursor.execute("SHOW COLUMNS FROM comments LIKE 'is_top'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE comments ADD COLUMN is_top INT DEFAULT 0 COMMENT '是否置顶：1-置顶，0-不置顶'")
        
        # 获取管理员用户ID（使用用户名'admin'的用户）
        cursor.execute("SELECT id FROM user WHERE username = 'admin' AND is_deleted = 0 LIMIT 1")
        admin_user = cursor.fetchone()
        
        if not admin_user:
            # 如果admin用户不存在，创建一个
            admin_password = '21232f297a57a5a743894a0e4a801fc3'  # admin123的MD5值
            try:
                # 使用唯一的电话号码创建admin用户
                cursor.execute("""
                    INSERT INTO user (username, password, phonenumber, email, is_deleted)
                    VALUES ('admin', %s, '13800000000', 'admin@example.com', 0)
                """, (admin_password,))
                db.mysql_conn.commit()
                # 获取新创建的admin用户ID
                cursor.execute("SELECT id FROM user WHERE username = 'admin' AND is_deleted = 0 LIMIT 1")
                admin_user = cursor.fetchone()
            except Exception as e:
                # 如果创建失败，尝试更新现有用户名为admin的记录
                cursor.execute("""
                    UPDATE user 
                    SET password = %s, is_deleted = 0 
                    WHERE username = 'admin'
                """, (admin_password,))
                db.mysql_conn.commit()
                # 再次尝试获取admin用户
                cursor.execute("SELECT id FROM user WHERE username = 'admin' AND is_deleted = 0 LIMIT 1")
                admin_user = cursor.fetchone()
            
            if not admin_user:
                # 如果还是获取不到admin用户，使用ID为1的用户
                cursor.execute("SELECT id FROM user WHERE is_deleted = 0 ORDER BY id LIMIT 1")
                admin_user = cursor.fetchone()
                
                if not admin_user:
                    return jsonify({'success': False, 'msg': '系统中没有可用用户'}), 500
        
        # 插入评论，默认管理员发布，且管理员评论自动置顶
        sql = """
            INSERT INTO comments (user_id, content, sentiment, sentiment_score, is_top)
            VALUES (%s, %s, %s, %s, 1)
        """
        cursor.execute(sql, (admin_user['id'], content, sentiment, score))
        db.mysql_conn.commit()
        cursor.close()
        
        return jsonify({'success': True, 'msg': '评论创建成功'})
        
    except Exception as e:
        logger.error(f"创建评论失败: {e}")
        return jsonify({'success': False, 'msg': f'创建评论失败: {str(e)}'}), 500








@app.route('/api/admin/comments/<int:comment_id>', methods=['DELETE'])
@check_admin
def delete_comment(comment_id):
    """删除评论"""
    try:
        cursor = db.get_mysql_cursor()
        cursor.execute('DELETE FROM comments WHERE id = %s', (comment_id,))
        db.mysql_conn.commit()
        cursor.close()

        return jsonify({'success': True, 'msg': '删除成功'})

    except Exception as e:
        logger.error(f"删除评论失败: {e}")
        return jsonify({'success': False, 'msg': f'删除评论失败: {str(e)}'}), 500


# ============================== 其他接口 ==============================

@app.route('/api/admin/herbs/select', methods=['GET'])
@check_admin
def get_herbs_select():
    """获取药材选择列表"""
    try:
        search = request.args.get('search', '')

        session = db.get_neo4j_session()

        query = """
            MATCH (h:Herb)
            WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
            RETURN id(h) as id, h.herb_id as herb_id, h.name as name
            ORDER BY h.name
            LIMIT 100
        """

        result = session.run(query, {'search': search})

        data = []
        for record in result:
            data.append({
                'id': record['id'],
                'herb_id': record.get('herb_id', ''),
                'name': record.get('name', ''),
                'label': f"{record.get('name', '')} ({record.get('herb_id', '无ID')})",
                'value': record['id']
            })

        session.close()

        return jsonify({
            'success': True,
            'data': data,
            'msg': '获取药材选择列表成功'
        })

    except Exception as e:
        logger.error(f"获取药材选择列表失败: {e}")
        return jsonify({'success': False, 'msg': f'获取药材选择列表失败: {str(e)}'}), 500


# ============================== 启动应用 ==============================

@app.route('/')
def index():
    return jsonify({
        'message': '中医药管理系统管理员后端API',
        'version': '1.0.0',
        'status': '运行中'
    })


@app.route('/health')
def health_check():
    """健康检查端点"""
    try:
        # 检查MySQL连接
        cursor = db.get_mysql_cursor()
        cursor.execute('SELECT 1')
        cursor.close()

        # 检查Neo4j连接
        session = db.get_neo4j_session()
        session.run('RETURN 1')
        session.close()

        return jsonify({
            'status': 'healthy',
            'mysql': 'connected',
            'neo4j': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


def shutdown_handler(signum=None, frame=None):
    """优雅关闭处理"""
    logger.info("📤 正在关闭数据库连接...")
    db.close()
    logger.info("✅ 服务已安全关闭")
    sys.exit(0)


if __name__ == '__main__':
    import signal
    from datetime import datetime

    # 注册优雅关闭信号
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    logger.info("✅ 管理员服务启动中...")
    logger.info(f"✅ 服务运行在 http://localhost:{app.config.get('PORT', 8000)}")

    app.run(
        host='0.0.0.0',
        port=app.config.get('PORT', 8000),
        debug=app.config['DEBUG']
    )