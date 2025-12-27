const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const cors = require('cors');

const app = express();
// 解决跨域
app.use(cors());
// 解析JSON请求体
app.use(express.json());

// 1. 配置MySQL连接（适配你的root/123456/tcmdb）
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'tcmdb',
  charset: 'utf8mb4'
});

// 2. 测试数据库连接
db.connect((err) => {
  if (err) {
    console.error('MySQL连接失败：', err.message);
    process.exit(1); // 连接失败则退出进程
  }
  console.log('✅ MySQL连接成功（tcmdb数据库）');
});

// 3. 注册接口（新增用户，默认is_deleted=0）
app.post('/register', async (req, res) => {
  try {
    const { username, phonenumber, email, password } = req.body;

    // 校验必填字段
    if (!username || !phonenumber || !email || !password) {
      return res.json({ success: false, msg: '用户名、手机号、邮箱、密码不能为空' });
    }

    // 校验手机号格式（简单校验）
    const phoneReg = /^1[3-9]\d{9}$/;
    if (!phoneReg.test(phonenumber)) {
      return res.json({ success: false, msg: '手机号格式错误' });
    }

    // 校验邮箱格式
    const emailReg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailReg.test(email)) {
      return res.json({ success: false, msg: '邮箱格式错误' });
    }

    // 检查用户名/手机号/邮箱是否已存在（排除逻辑删除的用户）
    const checkSql = `
      SELECT * FROM user
      WHERE (username = ? OR phonenumber = ? OR email = ?)
      AND is_deleted = 0
    `;
    const [checkResult] = await db.promise().query(checkSql, [username, phonenumber, email]);
    if (checkResult.length > 0) {
      return res.json({ success: false, msg: '用户名/手机号/邮箱已存在' });
    }

    // 密码加密（bcrypt，加盐值10）
    const salt = await bcrypt.genSalt(10);
    const hashedPwd = await bcrypt.hash(password, salt);

    // 插入用户数据（逻辑删除默认0）
    const insertSql = `
      INSERT INTO user (username, phonenumber, email, password)
      VALUES (?, ?, ?, ?)
    `;
    await db.promise().query(insertSql, [username, phonenumber, email, hashedPwd]);

    res.json({ success: true, msg: '注册成功' });
  } catch (err) {
    console.error('注册接口异常：', err.message);
    res.json({ success: false, msg: '注册失败：' + err.message });
  }
});

// 4. 登录接口（排除逻辑删除的用户）
app.post('/login', async (req, res) => {
  try {
    const { account, password } = req.body;

    // 校验必填字段
    if (!account || !password) {
      return res.json({ success: false, msg: '账号/密码不能为空' });
    }

    // 按用户名/手机号查询（排除已删除用户）
    const querySql = `
      SELECT * FROM user
      WHERE (username = ? OR phonenumber = ?)
      AND is_deleted = 0
    `;
    const [userList] = await db.promise().query(querySql, [account, account]);

    // 检查用户是否存在
    if (userList.length === 0) {
      return res.json({ success: false, msg: '账号不存在' });
    }
    const user = userList[0];

    // 验证密码
    const isPwdValid = await bcrypt.compare(password, user.password);
    if (!isPwdValid) {
      return res.json({ success: false, msg: '密码错误' });
    }

    // 返回用户信息（隐藏密码）
    const { password: _, ...userInfo } = user;
    res.json({
      success: true,
      msg: '登录成功',
      data: userInfo
    });
  } catch (err) {
    console.error('登录接口异常：', err.message);
    res.json({ success: false, msg: '登录失败：' + err.message });
  }
});

// 5. 启动服务（端口3001）
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`✅ 后端服务已启动：http://localhost:${PORT}`);
});

// 6. 优雅关闭数据库连接
process.on('SIGINT', () => {
  db.end(() => {
    console.log('\n❌ MySQL连接已关闭');
    process.exit(0);
  });
});