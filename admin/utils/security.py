import bcrypt

def hash_password(password: str) -> str:
    """
    对明文密码进行bcrypt加密
    :param password: 明文密码
    :return: 加密后的密码字符串
    """
    # 生成盐值（bcrypt自动处理盐值存储，无需单独保存）
    salt = bcrypt.gensalt()
    # 加密密码并转换为字符串返回（避免字节串存储问题）
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_pwd: str) -> bool:
    """
    验证明文密码是否匹配加密后的密码
    :param password: 用户输入的明文密码
    :param hashed_pwd: 数据库中存储的加密密码
    :return: 匹配返回True，否则返回False
    """
    try:
        # 注意：加密密码需转回字节串进行验证
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_pwd.encode('utf-8')
        )
    except Exception as e:
        # 密码格式错误/空值时返回验证失败
        print(f"密码验证失败：{str(e)}")
        return False