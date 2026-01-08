const mysql = require('mysql2');

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'zhr131415.',
  database: 'tcmdb',
  charset: 'utf8mb4'
});

db.connect((err) => {
  if (err) {
    console.error('连接失败:', err.message);
    process.exit(1);
  }
  console.log('连接成功');
  
  db.query('DESC users', (err, rows) => {
    if (err) {
      console.error('查询 users 表结构失败:', err.message);
    } else {
      console.log('=== users 表结构 ===');
      console.table(rows.map(r => ({ Field: r.Field, Type: r.Type, Null: r.Null })));
    }
    
    db.query('DESC comments', (err, rows) => {
      if (err) {
        console.error('查询 comments 表结构失败:', err.message);
      } else {
        console.log('\n=== comments 表结构 ===');
        console.table(rows.map(r => ({ Field: r.Field, Type: r.Type, Null: r.Null })));
      }
      db.end();
    });
  });
});
