// admin_server.js
const express = require('express');
const mysql = require('mysql2');
const neo4j = require('neo4j-driver');
const cors = require('cors');

const app = express();
// 解决跨域
app.use(cors());
// 解析JSON请求体
app.use(express.json());

// 1. 配置数据库连接
// MySQL连接（适配你的root/123456/tcmdb）
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'tcmdb',
  charset: 'utf8mb4'
});

// Neo4j连接（替换为你的本地配置）
const neo4jDriver = neo4j.driver(
  'bolt://10.138.238.141:7687',
  neo4j.auth.basic('neo4j', '12345678')
);

// 2. 测试MySQL连接
db.connect((err) => {
  if (err) {
    console.error('MySQL连接失败：', err.message);
    process.exit(1); // 连接失败则退出进程
  }
  console.log('✅ MySQL连接成功（tcmdb数据库）');
});

// 3. 管理员权限验证（固定Token） - 确保与前端完全一致
const ADMIN_TOKEN = 'admin_fixed_token_123456';  // 修改这里，与前端保持一致
console.log('✅ 管理员Token已设置:', ADMIN_TOKEN);  // 添加日志确认

function checkAdmin(req, res, next) {
  const authHeader = req.headers.authorization;
  console.log('🔑 收到的Authorization头:', authHeader);  // 添加调试日志

  if (!authHeader) {
    console.log('❌ 未提供Authorization头');
    return res.json({ success: false, msg: '未提供授权令牌' });
  }

  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    console.log('❌ Authorization格式错误，期望: "Bearer {token}"');
    return res.json({ success: false, msg: '授权格式错误，期望: Bearer {token}' });
  }

  const token = parts[1];
  console.log('🔑 提取的Token:', token);
  console.log('🔑 期望的Token:', ADMIN_TOKEN);
  console.log('🔑 Token匹配结果:', token === ADMIN_TOKEN);

  if (!token || token !== ADMIN_TOKEN) {
    console.log('❌ Token不匹配或为空');
    return res.json({ success: false, msg: '无管理员权限' });
  }

  console.log('✅ Token验证通过');
  next();
}

// 3. 核心功能1：用户管理
// 获取用户列表
// 获取用户列表（支持搜索）
app.get('/api/admin/users', checkAdmin, async (req, res) => {
  try {
    console.log('📋 获取用户列表请求');
    const { search } = req.query;
    console.log('搜索关键词:', search);

    let query = 'SELECT id, username, phonenumber, email FROM user WHERE is_deleted = 0';
    let params = [];

    if (search && search.trim() !== '') {
      query += ' AND (username LIKE ? OR phonenumber LIKE ?)';
      const searchTerm = `%${search}%`;
      params = [searchTerm, searchTerm];
    }

    console.log('执行查询:', query, '参数:', params);
    const [users] = await db.promise().query(query, params);
    console.log(`✅ 查询到 ${users.length} 个用户`);
    res.json({ success: true, data: users });
  } catch (err) {
    console.error('查询用户失败：', err.message);
    res.json({ success: false, msg: '获取用户失败：' + err.message });
  }
});

// 禁用用户（逻辑删除）
app.put('/api/admin/users/:id/delete', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`🔄 禁用用户ID: ${id}`);
    await db.promise().query('UPDATE user SET is_deleted = 1 WHERE id = ?', [id]);
    res.json({ success: true, msg: '用户禁用成功' });
  } catch (err) {
    console.error('禁用用户失败：', err.message);
    res.json({ success: false, msg: '禁用用户失败：' + err.message });
  }
});

// 4. 核心功能2：中药材管理
// 获取药材列表
app.get('/api/admin/herbs', checkAdmin, async (req, res) => {
  try {
    console.log('🌿 获取药材列表请求');
    const session = neo4jDriver.session();
    const result = await session.run('MATCH (h:Herb) RETURN h { .id, .name, .efficacy } AS herb');
    const herbs = result.records.map(r => r.get('herb'));
    session.close();
    console.log(`✅ 查询到 ${herbs.length} 种药材`);
    res.json({ success: true, data: herbs });
  } catch (err) {
    console.error('获取药材失败：', err.message);
    res.json({ success: false, msg: '获取药材失败：' + err.message });
  }
});

// 新增药材
app.post('/api/admin/herbs', checkAdmin, async (req, res) => {
  try {
    const { name, efficacy } = req.body;
    console.log(`➕ 新增药材: ${name}, 功效: ${efficacy}`);
    const session = neo4jDriver.session();
    await session.run('CREATE (h:Herb { id: $id, name: $name, efficacy: $efficacy })', {
      id: Date.now().toString(),
      name,
      efficacy
    });
    session.close();
    res.json({ success: true, msg: '药材新增成功' });
  } catch (err) {
    console.error('新增药材失败：', err.message);
    res.json({ success: false, msg: '新增药材失败：' + err.message });
  }
});

// 删除药材
app.delete('/api/admin/herbs/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`🗑️ 删除药材ID: ${id}`);
    const session = neo4jDriver.session();
    await session.run('MATCH (h:Herb { id: $id }) DELETE h', { id });
    session.close();
    res.json({ success: true, msg: '药材删除成功' });
  } catch (err) {
    console.error('删除药材失败：', err.message);
    res.json({ success: false, msg: '删除药材失败：' + err.message });
  }
});

// 5. 核心功能3：药方管理
// 获取药方列表
app.get('/api/admin/prescriptions', checkAdmin, async (req, res) => {
  try {
    console.log('📜 获取药方列表请求');
    const session = neo4jDriver.session();
    const result = await session.run(`
      MATCH (p:Prescription)
      OPTIONAL MATCH (p)<-[r:INCLUDE_IN]-(h:Herb)
      RETURN p { .id, .name, herbs: collect(h { .name }) } AS prescription
    `);
    const prescriptions = result.records.map(r => r.get('prescription'));
    session.close();
    console.log(`✅ 查询到 ${prescriptions.length} 个药方`);
    res.json({ success: true, data: prescriptions });
  } catch (err) {
    console.error('获取药方失败：', err.message);
    res.json({ success: false, msg: '获取药方失败：' + err.message });
  }
});

// 新增药方
app.post('/api/admin/prescriptions', checkAdmin, async (req, res) => {
  try {
    const { name, herbIds } = req.body;
    console.log(`➕ 新增药方: ${name}, 药材IDs: ${herbIds}`);
    const session = neo4jDriver.session();
    const pid = Date.now().toString();
    // 创建药方
    await session.run('CREATE (p:Prescription { id: $pid, name: $name })', { pid, name });
    // 关联药材
    for (const hid of herbIds) {
      await session.run(`MATCH (h:Herb { id: $hid }), (p:Prescription { id: $pid }) CREATE (h)-[:INCLUDE_IN]->(p)`, { hid, pid });
    }
    session.close();
    res.json({ success: true, msg: '药方新增成功' });
  } catch (err) {
    console.error('新增药方失败：', err.message);
    res.json({ success: false, msg: '新增药方失败：' + err.message });
  }
});

// 删除药方
app.delete('/api/admin/prescriptions/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`🗑️ 删除药方ID: ${id}`);
    const session = neo4jDriver.session();
    await session.run('MATCH (p:Prescription { id: $id }) DETACH DELETE p', { id });
    session.close();
    res.json({ success: true, msg: '药方删除成功' });
  } catch (err) {
    console.error('删除药方失败：', err.message);
    res.json({ success: false, msg: '删除药方失败：' + err.message });
  }
});

// 6. 启动服务（端口3000）
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`\n🚀 管理员后端服务已启动：http://localhost:${PORT}`);
  console.log(`🔑 管理员Token：${ADMIN_TOKEN}`);
  console.log('📋 可用API端点：');
  console.log('  GET  /api/admin/users          - 获取用户列表');
  console.log('  PUT  /api/admin/users/:id/delete - 禁用用户');
  console.log('  GET  /api/admin/herbs          - 获取药材列表');
  console.log('  POST /api/admin/herbs          - 新增药材');
  console.log('  DELETE /api/admin/herbs/:id    - 删除药材');
  console.log('  GET  /api/admin/prescriptions  - 获取药方列表');
  console.log('  POST /api/admin/prescriptions  - 新增药方');
  console.log('  DELETE /api/admin/prescriptions/:id - 删除药方');
});

// 7. 优雅关闭连接
process.on('SIGINT', () => {
  db.end(() => {
    console.log('\n❌ MySQL连接已关闭');
  });
  neo4jDriver.close().then(() => {
    console.log('❌ Neo4j连接已关闭');
    process.exit(0);
  });
});