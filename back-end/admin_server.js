// admin_server.js
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
// const neo4j = require('neo4j-driver'); // 暂时屏蔽 Neo4j 防止报错

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'zhr131415.',
  database: 'tcmdb', // 确保库名正确
  charset: 'utf8mb4'
});

db.connect((err) => {
  if (err) console.error('MySQL连接失败', err.message);
  else console.log('✅ admin_server.js: MySQL连接成功');
});

// 固定Token验证
const ADMIN_TOKEN = 'admin_fixed_token_123456';
function checkAdmin(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth || auth.split(' ')[1] !== ADMIN_TOKEN) {
    return res.json({ success: false, msg: '无管理员权限' });
  }
  next();
}

// 1. 获取用户列表 (适配你的 user 表)
app.get('/api/admin/users', checkAdmin, async (req, res) => {
  try {
    // 重点修改：表名 user (单数)，逻辑删除 is_deleted=0
    const sql = 'SELECT id, username, phonenumber, email FROM user WHERE is_deleted = 0';
    const [rows] = await db.promise().query(sql);
    res.json({ success: true, data: rows });
  } catch (err) {
    console.error(err);
    res.json({ success: false, msg: err.message });
  }
});

// 2. 禁用用户 (逻辑删除)
app.put('/api/admin/users/:id/delete', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    // 重点修改：表名 user，字段 is_deleted 置为 1
    await db.promise().query('UPDATE user SET is_deleted = 1 WHERE id = ?', [id]);
    res.json({ success: true, msg: '操作成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 3. 药材/药方 (暂时返回空，防止 Neo4j 报错)
app.get('/api/admin/herbs', checkAdmin, (req, res) => res.json({ success: true, data: [] }));
app.get('/api/admin/prescriptions', checkAdmin, (req, res) => res.json({ success: true, data: [] }));

// 4. 评论管理
app.get('/api/admin/comments', checkAdmin, async (req, res) => {
  try {
    // 这里的 username 是我们第一步手动加上去的
    const [rows] = await db.promise().query('SELECT * FROM comments ORDER BY created_at DESC');
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

app.listen(3000, () => console.log('✅ 管理员服务运行在 3000 端口'));