// admin_server.js
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
// const neo4j = require('neo4j-driver'); // 暂时屏蔽 Neo4j 防止报错
const { exec } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// --- 保持你队友的数据库连接配置不动 ---
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

// 1. 获取用户列表 (保持原样)
app.get('/api/admin/users', checkAdmin, async (req, res) => {
  try {
    const sql = 'SELECT id, username, phonenumber, email FROM user WHERE is_deleted = 0';
    const [rows] = await db.promise().query(sql);
    res.json({ success: true, data: rows });
  } catch (err) {
    console.error(err);
    res.json({ success: false, msg: err.message });
  }
});

// 2. 禁用用户 (保持原样)
app.put('/api/admin/users/:id/delete', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    await db.promise().query('UPDATE user SET is_deleted = 1 WHERE id = ?', [id]);
    res.json({ success: true, msg: '操作成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 3. 药材/药方 (保持原样)
app.get('/api/admin/herbs', checkAdmin, (req, res) => res.json({ success: true, data: [] }));
app.get('/api/admin/prescriptions', checkAdmin, (req, res) => res.json({ success: true, data: [] }));

// ==========================================
// 4. 评论管理 (这里进行了必要的更新以支持情感分析)
// ==========================================

// 获取评论列表 (修改了 SQL 以获取 sentiment 字段，但逻辑结构没变)
app.get('/api/admin/comments', checkAdmin, async (req, res) => {
  try {
    // 修改说明：为了支持情感分析展示，这里改成了联表查询
    // 这样能获取到 sentiment(情感标签), sentiment_score(分数) 以及最新的 username
    const sql = `
      SELECT c.*, u.username 
      FROM comments c
      LEFT JOIN user u ON c.user_id = u.id
      ORDER BY c.created_at DESC
    `;
    const [rows] = await db.promise().query(sql);
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// --- 以下是【新增】的接口，用于支持管理员的增删改查操作 ---
// --- 放在这里不会影响上面的原有代码逻辑 ---

// 新增评论
app.post('/api/admin/comments', checkAdmin, async (req, res) => {
  try {
    const { userId, content } = req.body;
    // 管理员添加的评论，默认给个中性评分
    const sql = `INSERT INTO comments (user_id, content, sentiment, sentiment_score) VALUES (?, ?, 'neutral', 0.5)`;
    await db.promise().query(sql, [userId, content]);
    res.json({ success: true, msg: '新增成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

// 编辑评论
// 3.3 管理员编辑评论 (修改内容 + 重新进行情感分析)
app.put('/api/admin/comments/:id', checkAdmin, async (req, res) => {
  const { content } = req.body;
  const { id } = req.params;

  if (!content) return res.json({ success: false, msg: '内容不能为空' });

  // ==========================================
  // 【重要修改 1】请在这里填入你刚才查到的 Python 绝对路径！
  // 注意：Windows路径的单斜杠 \ 必须写成双斜杠 \\
  // 例如：'E:\\python3.17.3\\python.exe'
  const PYTHON_PATH = 'E:\\python3.17.3\\python.exe'; // <--- 请根据第一步的结果修改这里！！
  // ==========================================

  const scriptPath = path.join(__dirname, 'analysis.py');

  // 【重要修改 2】去掉换行符，并转义双引号，防止命令崩溃
  const safeContent = content
    .replace(/[\r\n]/g, '') // 去掉回车换行
    .replace(/"/g, '\\"');  // 转义双引号

  // 使用绝对路径执行
  exec(`"${PYTHON_PATH}" "${scriptPath}" "${safeContent}"`, async (error, stdout, stderr) => {
    let score = 0.5;

    if (!error && stdout) {
      // 尝试解析分数
      const result = parseFloat(stdout.trim());
      if (!isNaN(result)) {
        score = result;
        console.log(`[编辑] 内容: "${safeContent}" => 新得分: ${score}`);
      }
    } else {
      // 即使报错也不要崩，把错误打出来看看
      console.error('情感分析脚本异常:', stderr || error.message);
      // 如果是因为编码问题报错，通常默认给个分继续跑
    }

    // 计算新标签
    let sentiment = 'neutral';
    if (score >= 0.6) sentiment = 'positive';
    else if (score <= 0.4) sentiment = 'negative';

    try {
      // 这里的 db 是队友代码里的数据库连接变量
      const sql = `UPDATE comments SET content = ?, sentiment_score = ?, sentiment = ? WHERE id = ?`;
      await db.promise().query(sql, [content, score, sentiment, id]);

      res.json({ success: true, msg: '修改成功' });
    } catch (err) {
      console.error(err);
      res.json({ success: false, msg: '数据库更新失败' });
    }
  });
});

// 删除评论
app.delete('/api/admin/comments/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    await db.promise().query('DELETE FROM comments WHERE id = ?', [id]);
    res.json({ success: true, msg: '删除成功' });
  } catch (err) {
    res.json({ success: false, msg: err.message });
  }
});

app.listen(3000, () => console.log('✅ 管理员服务运行在 3000 端口'));