// admin_server.js (管理员后端 - 端口 3000)
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 数据库连接池
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'zhr131415.', // 你的密码
  database: 'tcmdb',
  charset: 'utf8mb4',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// 固定Token验证中间件
const ADMIN_TOKEN = 'admin_fixed_token_123456';
function checkAdmin(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth || auth.split(' ')[1] !== ADMIN_TOKEN) {
    return res.json({ success: false, msg: '无管理员权限' });
  }
  next();
}

// =======================
// 1. 用户管理接口
// =======================
app.get('/api/admin/users', checkAdmin, async (req, res) => {
  try {
    const { search } = req.query;
    let sql = 'SELECT id, username, phonenumber, email, is_deleted FROM user WHERE is_deleted = 0';
    let params = [];

    if (search) {
      sql += ' AND (username LIKE ? OR phonenumber LIKE ?)';
      params = [`%${search}%`, `%${search}%`];
    }

    const [rows] = await pool.promise().query(sql, params);
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

app.put('/api/admin/users/:id/delete', checkAdmin, async (req, res) => {
  try {
    await pool.promise().query('UPDATE user SET is_deleted = 1 WHERE id = ?', [req.params.id]);
    res.json({ success: true, msg: '用户禁用成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// =======================
// 2. 中药材/药方 (Neo4j占位)
// =======================
app.get('/api/admin/herbs', checkAdmin, (req, res) => res.json({ success: true, data: [] }));
app.get('/api/admin/prescriptions', checkAdmin, (req, res) => res.json({ success: true, data: [] }));
app.post('/api/admin/herbs', checkAdmin, (req, res) => res.json({ success: true, msg: '演示模式: 新增成功' }));
app.delete('/api/admin/herbs/:id', checkAdmin, (req, res) => res.json({ success: true, msg: '演示模式: 删除成功' }));
app.post('/api/admin/prescriptions', checkAdmin, (req, res) => res.json({ success: true, msg: '演示模式: 新增成功' }));
app.delete('/api/admin/prescriptions/:id', checkAdmin, (req, res) => res.json({ success: true, msg: '演示模式: 删除成功' }));

// =======================
// 3. 评论管理接口 (核心修复部分)
// =======================

// 3.1 获取所有评论 (包含情感数据)
app.get('/api/admin/comments', checkAdmin, async (req, res) => {
  try {
    // 联表查询，获取用户名、情感得分等
    const sql = `
      SELECT c.id, c.user_id, c.content, c.created_at, 
             c.sentiment, c.sentiment_score,
             u.username 
      FROM comments c
      LEFT JOIN user u ON c.user_id = u.id
      ORDER BY c.created_at DESC
    `;
    const [rows] = await pool.promise().query(sql);
    res.json({ success: true, data: rows });
  } catch (err) {
    console.error(err);
    res.json({ success: false, msg: err.message });
  }
});

// 3.2 管理员新增评论 (模拟用户发言)
app.post('/api/admin/comments', checkAdmin, async (req, res) => {
  try {
    const { userId, content } = req.body;
    // 简单插入，管理员后台新增一般不做情感分析，或者设为默认值
    const sql = `
      INSERT INTO comments (user_id, content, sentiment, sentiment_score) 
      VALUES (?, ?, 'neutral', 0.5)
    `;
    await pool.promise().query(sql, [userId, content]);
    res.json({ success: true, msg: '评论添加成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 3.3 管理员编辑评论 (修改内容)
app.put('/api/admin/comments/:id', checkAdmin, async (req, res) => {
  try {
    const { content } = req.body;
    const { id } = req.params;

    // 更新内容，同时可以重置情感得分为中性（因为内容变了）
    const sql = `UPDATE comments SET content = ?, sentiment_score = 0.5, sentiment = 'neutral' WHERE id = ?`;
    await pool.promise().query(sql, [content, id]);

    res.json({ success: true, msg: '评论修改成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 3.4 管理员删除评论 (物理删除)
app.delete('/api/admin/comments/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    await pool.promise().query('DELETE FROM comments WHERE id = ?', [id]);
    res.json({ success: true, msg: '评论删除成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 启动服务
app.listen(3000, () => {
  console.log('✅ 管理员后端服务已启动: http://localhost:3000');
});