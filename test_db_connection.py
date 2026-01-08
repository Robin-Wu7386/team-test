import pymysql

# 1. 数据库配置 (根据你提供的信息)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zhr131415.',  # 你的密码
    'database': 'tcmdb',  # 你的数据库名
    'charset': 'utf8mb4'
}


def test_workflow():
    print(">>> 1. 正在尝试连接数据库...")
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功！")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return

    try:
        with conn.cursor() as cursor:
            # 2. 测试查询表结构
            print("\n>>> 2. 正在检查 users 表是否存在...")
            try:
                cursor.execute("SELECT * FROM users LIMIT 1")
                print("✅ users 表存在，且能查询！")
                result = cursor.fetchone()
                print(f"   当前表里第一条数据: {result}")
            except Exception as e:
                print(f"❌ users 表查询失败 (请检查表名是否是 users): {e}")
                return

            # 3. 测试插入数据 (模拟注册)
            print("\n>>> 3. 正在测试插入数据 (模拟注册)...")
            import random
            # 生成随机测试账号，防止重复报错
            rand_suffix = str(random.randint(1000, 9999))
            test_user = f"test_{rand_suffix}"
            test_phone = f"1390000{rand_suffix}"
            test_email = f"test{rand_suffix}@qq.com"

            sql = """
                  INSERT INTO users (username, phonenumber, email, password, is_deleted)
                  VALUES (%s, %s, %s, 'test_pwd', 0) \
                  """
            try:
                cursor.execute(sql, (test_user, test_phone, test_email))
                conn.commit()
                print(f"✅ 插入成功！新用户: {test_user}")
            except Exception as e:
                print(f"❌ 插入失败: {e}")
                conn.rollback()

    except Exception as e:
        print(f"❌ 未知错误: {e}")
    finally:
        conn.close()
        print("\n>>> 测试结束")


if __name__ == '__main__':
    test_workflow()