const { spawn } = require('child_process');
const path = require('path');

// 启动 Node.js 后端 (Server)
const server = spawn('node', ['server.js'], {
  cwd: __dirname,
  stdio: 'inherit',
  shell: true
});

console.log('🚀 正在启动 Node.js 后端 (Port 3001)...');

// 启动 Python 管理员后台 (Admin)
// 假设 python 在环境变量中，且 admin 目录在上一级
const adminPath = path.join(__dirname, '../admin/run.py');
const adminDir = path.join(__dirname, '../admin');

console.log(`🚀 正在启动 Python 管理员后台 (Port 5000)...`);
console.log(`   脚本路径: ${adminPath}`);

const admin = spawn('python', ['run.py'], {
  cwd: adminDir,
  stdio: 'inherit',
  shell: true
});

// 监听关闭事件
process.on('SIGINT', () => {
  console.log('\n🛑 正在停止所有服务...');
  server.kill();
  admin.kill();
  process.exit();
});
