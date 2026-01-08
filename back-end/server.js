// server.js (终极稳定版 - 使用连接池)
const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');

const app = express();

// 1. 允许跨域 (允许前端直接访问)
app.use(cors());
app.use(express.json());

// 2. 使用连接池 (Pool) 而不是单个连接
// 连接池会自动管理连接，不会出现"连接已关闭"的问题
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

// 测试数据库连接
pool.getConnection((err, connection) => {
  if (err) {
    console.error('❌ 严重错误: 数据库连接失败!', err.message);
  } else {
    console.log('✅ 数据库连接池已就绪 (TCMDB)');
    connection.release(); // 释放连接回池子
  }
});

// =======================
// 接口区域
// =======================

// 1. 注册
app.post('/user/register', async (req, res) => {
  try {
    const { username, phonenumber, email, password } = req.body;
    // 使用 pool.promise()
    const [exists] = await pool.promise().query(
      'SELECT id FROM user WHERE (username=? OR phonenumber=? OR email=?) AND is_deleted=0',
      [username, phonenumber, email]
    );
    if (exists.length > 0) return res.json({ success: false, msg: '用户已存在' });

    const salt = await bcrypt.genSalt(10);
    const hashedPwd = await bcrypt.hash(password, salt);

    await pool.promise().query(
      'INSERT INTO user (username, phonenumber, email, password) VALUES (?, ?, ?, ?)',
      [username, phonenumber, email, hashedPwd]
    );
    res.json({ success: true, msg: '注册成功' });
  } catch (err) {
    console.error(err);
    res.json({ success: false, msg: err.message });
  }
});

// 2. 登录
app.post('/user/login', async (req, res) => {
  try {
    const { account, password } = req.body;
    const [rows] = await pool.promise().query(
      'SELECT * FROM user WHERE (username=? OR phonenumber=?) AND is_deleted=0',
      [account, account]
    );
    if (rows.length === 0) return res.json({ success: false, msg: '账号不存在' });

    const user = rows[0];
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.json({ success: false, msg: '密码错误' });

    const { password: _, ...userInfo } = user;
    res.json({ success: true, msg: '登录成功', data: userInfo });
  } catch (err) {
    console.error(err);
    res.json({ success: false, msg: err.message });
  }
});

// 3. 获取评论 (同时支持 /comments 和 /api/comments)
app.get(['/comments', '/api/comments'], async (req, res) => {
  console.log(`收到获取评论请求: ${req.url}`); // 添加日志
  try {
    const sql = `
      SELECT c.id, c.content, c.created_at, c.parent_id, c.reply_to_username,
             u.username, u.id as user_id
      FROM comments c
      LEFT JOIN user u ON c.user_id = u.id
      ORDER BY c.created_at DESC
    `;
    const [rows] = await pool.promise().query(sql);
    res.json({ success: true, data: rows });
  } catch (err) {
    console.error('获取评论出错:', err);
    res.json({ success: false, msg: err.message });
  }
});

// =======================
// 4. 发表评论 (含情感分析功能)
// =======================
app.post(['/comments', '/api/comments'], async (req, res) => {
  console.log('收到发表评论请求:', req.body);
  try {
    const { userId, content, parentId, replyToUsername } = req.body;
    if (!userId || !content) return res.json({ success: false, msg: '参数不全' });

    // --- 情感分析核心逻辑开始 ---
    // 定义 Python 脚本路径
    const scriptPath = path.join(__dirname, 'analysis.py');
    // 处理评论内容中的特殊字符（防止命令行报错）
    const safeContent = content.replace(/"/g, '\\"');

    // 调用 Python 脚本
    exec(`python "${scriptPath}" "${safeContent}"`, async (error, stdout, stderr) => {
      let score = 0.5; // 默认中性

      if (!error && stdout) {
        // 获取 Python 输出的分数 (去掉换行符)
        score = parseFloat(stdout.trim());
        console.log(`情感分析结果: ${content} => 得分: ${score}`);
      } else {
        console.error('情感分析脚本出错，使用默认值:', error || stderr);
      }

      // 根据分数判断标签
      let sentiment = 'neutral'; // 中性
      if (score >= 0.6) sentiment = 'positive'; // 正面
      else if (score <= 0.4) sentiment = 'negative'; // 负面

      // --- 存入数据库 ---
      try {
        const insertSql = `
          INSERT INTO comments (user_id, content, parent_id, reply_to_username, sentiment, sentiment_score) 
          VALUES (?, ?, ?, ?, ?, ?)
        `;
        const [result] = await pool.promise().query(insertSql, [
          userId, content, parentId || null, replyToUsername || null, sentiment, score
        ]);

        // 查回新数据
        const [newComment] = await pool.promise().query(`
          SELECT c.*, u.username 
          FROM comments c
          LEFT JOIN user u ON c.user_id = u.id
          WHERE c.id = ?
        `, [result.insertId]);

        res.json({ success: true, msg: '发布成功', data: newComment[0] });
      } catch (dbErr) {
        console.error(dbErr);
        res.json({ success: false, msg: '数据库存入失败' });
      }
    });
    // --- 情感分析逻辑结束 ---

  } catch (err) {
    console.error('发表评论出错:', err);
    res.json({ success: false, msg: err.message });
  }
});

// =======================
// 5. 提交问诊信息接口
// =======================
app.post('/api/consultations', async (req, res) => {
  try {
    const { userId, age, sex, height, weight, symptoms } = req.body;

    // 1. 校验登录
    if (!userId) {
      return res.json({ success: false, msg: '请先登录' });
    }

    // 2. 校验必填项
    if (!age || !sex || !symptoms) {
      return res.json({ success: false, msg: '请填写完整的必要信息（年龄、性别、症状）' });
    }

    // 3. 插入数据库
    const sql = `
      INSERT INTO consultation_records (user_id, age, sex, height, weight, symptoms)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    // 使用连接池执行
    const [result] = await pool.promise().query(sql, [
      userId, age, sex, height || 0, weight || 0, symptoms
    ]);

    res.json({ success: true, msg: '提交成功，信息已入库', data: { id: result.insertId } });

  } catch (err) {
    console.error('问诊提交失败:', err);
    res.json({ success: false, msg: '服务器错误: ' + err.message });
  }
});

// 获取我的问诊历史 (可选功能，方便你以后查看)
app.get('/api/consultations', async (req, res) => {
  try {
    const { userId } = req.query;
    if (!userId) return res.json({ success: false, msg: '未提供用户ID' });

    const [rows] = await pool.promise().query(
      'SELECT * FROM consultation_records WHERE user_id = ? ORDER BY created_at DESC',
      [userId]
    );
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});



// 启动监听
app.listen(3001, () => {
  console.log('✅ 后端服务稳定运行中: http://localhost:3001');
  console.log('⏳ 等待前端连接...');
});