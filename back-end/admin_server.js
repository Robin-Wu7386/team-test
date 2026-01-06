// admin.js
const express = require('express');
const mysql = require('mysql2');
const neo4j = require('neo4j-driver');
const cors = require('cors');
// 创建Express应用
const app = express();
// 跨域处理
app.use(cors());
// 解析JSON格式请求体
app.use(express.json());
// ------------------------------ 数据库配置 ------------------------------
// 1. MySQL配置（用户数据存储）
const mysqlDb = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'tcmdb',
  charset: 'utf8mb4'
});
// 2. Neo4j配置
const neo4jDriver = neo4j.driver(
  'bolt://localhost:7687',
  //  'bolt://10.128.179.130:7687',
  neo4j.auth.basic('neo4j', '12345678')
);
// 数据库连接测试（保持不变）
mysqlDb.connect((err) => {
  if (err) {
    console.error('❌ MySQL连接失败：', err.message);
    process.exit(1);
  }
  console.log('✅ MySQL连接成功');
});
async function testNeo4jConnection() {
  try {
    const session = neo4jDriver.session();
    await session.run('RETURN 1');
    session.close();
    console.log('✅ Neo4j连接成功');
  } catch (err) {
    console.error('❌ Neo4j连接失败：', err.message);
    process.exit(1);
  }
}
testNeo4jConnection();
// ------------------------------ 管理员权限校验 ------------------------------
const ADMIN_TOKEN = 'admin_fixed_token_123456';
function checkAdmin(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.json({ success: false, msg: '请携带管理员令牌' });
  }
  const token = authHeader.split(' ')[1];
  if (token !== ADMIN_TOKEN) {
    return res.json({ success: false, msg: '管理员令牌无效，无访问权限' });
  }
  next();
}
// ============================== 一、用户管理 ==============================
// 用户管理接口保持不变
app.get('/api/admin/users', checkAdmin, (req, res) => {
  const {
    search = '',
    page = 1,
    pageSize = 20
  } = req.query;
  const pageNum = parseInt(page) || 1;
  const pageSizeNum = parseInt(pageSize) || 20;
  const offset = (pageNum - 1) * pageSizeNum;
  let whereClause = 'WHERE is_deleted = 0';
  const queryParams = [];
  if (search.trim() !== '') {
    whereClause += ' AND (username LIKE ? OR phonenumber LIKE ?)';
    const searchParam = `%${search}%`;
    queryParams.push(searchParam, searchParam);
  }
  const countSql = `SELECT COUNT(*) as total FROM user ${whereClause}`;
  const dataSql = `
    SELECT id, username, phonenumber, email, is_deleted, created_at, updated_at
    FROM user
    ${whereClause}
    ORDER BY id DESC
    LIMIT ? OFFSET ?
  `;
  queryParams.push(pageSizeNum, offset);
  mysqlDb.query(countSql, queryParams.slice(0, queryParams.length - 2), (err, countResults) => {
    if (err) {
      console.error('获取用户总数失败：', err.message);
      return res.json({ success: false, msg: '获取用户列表失败：' + err.message });
    }
    const total = countResults[0]?.total || 0;
    mysqlDb.query(dataSql, queryParams, (err, results) => {
      if (err) {
        console.error('获取用户列表失败：', err.message);
        return res.json({ success: false, msg: '获取用户列表失败：' + err.message });
      }
      res.json({
        success: true,
        data: results,
        total: total,
        msg: '获取用户列表成功'
      });
    });
  });
});
app.put('/api/admin/users/:id/delete', checkAdmin, (req, res) => {
  const { id } = req.params;
  const sql = 'UPDATE user SET is_deleted = 1 WHERE id = ? AND is_deleted = 0';
  mysqlDb.query(sql, [id], (err, result) => {
    if (err) {
      console.error('❌ 逻辑删除用户失败：', err.message);
      return res.json({ success: false, msg: '删除用户失败：' + err.message });
    }
    if (result.affectedRows === 0) {
      return res.json({ success: false, msg: '该用户不存在或已被删除' });
    }
    res.json({
      success: true,
      msg: '用户删除成功'
    });
  });
});

// ============================== 二、药材管理（修正版，适应你的数据库结构） ==============================
// ============================== 二、药材管理（完整版） ==============================

// 1. 获取药材列表（包含基础字段）
app.get('/api/admin/herbs', checkAdmin, async (req, res) => {
  try {
    const { search = '', page = 1, pageSize = 20 } = req.query;
    const pageNum = parseInt(page, 10) || 1;
    const pageSizeNum = parseInt(pageSize, 10) || 20;
    const skip = Math.max(0, (pageNum - 1) * pageSizeNum);
    const limit = Math.max(1, pageSizeNum);
    const session = neo4jDriver.session();
    try {
      // 总数查询
      const countQuery = `
        MATCH (h:Herb)
        WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
        RETURN count(h) as total
      `;
      const countResult = await session.run(countQuery, { search });
      const total = countResult.records[0].get('total').low || 0;

      // 列表查询
      const listQuery = `
        MATCH (h:Herb)
        WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
        RETURN id(h) as id, h.herb_id as herb_id, h.name as name, h.source_list as source_list
        ORDER BY h.name
        SKIP $skip LIMIT $limit
      `;
      const listResult = await session.run(listQuery, {
        search,
        skip: neo4j.int(skip),
        limit: neo4j.int(limit)
      });

      const data = listResult.records.map(record => {
        const id = record.get('id');
        return {
          id: id.toNumber ? id.toNumber().toString() : id.toString(),
          herb_id: record.get('herb_id') || '',
          name: record.get('name') || '',
          source_list: record.get('source_list') || ''
        };
      });

      res.json({
        success: true,
        data: data,
        total: total,
        msg: '获取药材列表成功'
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药材列表失败：', err.message);
    res.json({ success: false, msg: '获取药材列表失败：' + err.message });
  }
});

// 2. 获取药材详情（用于编辑时显示）
app.get('/api/admin/herbs/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      const result = await session.run(
        `MATCH (h:Herb)
         WHERE id(h) = $id
         OPTIONAL MATCH (h)-[:FROM_SOURCE]->(a:Attributes)
         RETURN
           // Herb基础字段
           h.herb_id as herb_id,
           h.name as name,
           h.source_list as source_list,
           h.alias as alias,
           h.function as function,
           h.original_form as original_form,
           h.taste as taste,
           h.caution as caution,
           h.habitat as habitat,
           h.usage_dosage as usage_dosage,

           // 完整Attributes字段（使用COALESCE提供默认值）
           COALESCE(a.功能主治, '') as 功能主治,
           COALESCE(a.性味, '') as 性味,
           COALESCE(a.性味归经, '') as 性味归经,
           COALESCE(a.归经, '') as 归经,
           COALESCE(a.英文名, '') as 英文名,
           COALESCE(a.化学成分, '') as 化学成分,
           COALESCE(a.药理作用, '') as 药理作用,
           COALESCE(a.临床应用, '') as 临床应用,
           COALESCE(a.毒性, '') as 毒性,
           COALESCE(a.植物形态, '') as 植物形态,
           COALESCE(a.动物形态, '') as 动物形态,
           COALESCE(a.药用部位, '') as 药用部位,
           COALESCE(a.采收加工, '') as 采收加工,
           COALESCE(a.炮制, '') as 炮制,
           COALESCE(a.制剂, '') as 制剂,
           COALESCE(a.性状, '') as 性状,
           COALESCE(a.鉴别, '') as 鉴别,
           COALESCE(a.含量测定, '') as 含量测定,
           COALESCE(a.注意, '') as 注意,
           COALESCE(a.贮藏, '') as 贮藏,
           COALESCE(a.备注, '') as 备注,
           COALESCE(a.各家论述, '') as 各家论述,
           COALESCE(a.相关药方, '') as 相关药方,
           COALESCE(a.复方, '') as 复方,
           COALESCE(a.拼音注音, '') as 拼音注音,
           COALESCE(a.原形态, '') as 原形态,
           COALESCE(a.生境分布, '') as 生境分布,
           COALESCE(a.主要成分, '') as 主要成分,
           COALESCE(a.规格, '') as 规格,
           COALESCE(a.制法, '') as 制法,
           COALESCE(a.栽培, '') as 栽培
        `,
        { id: neo4j.int(id) }
      );

      if (result.records.length === 0) {
        return res.json({ success: false, msg: '药材不存在' });
      }

      const record = result.records[0];

      // 构建完整响应对象
      const herb = {
        id: id,
        // Herb基础信息
        herb_id: record.get('herb_id') || '',
        name: record.get('name') || '',
        source_list: record.get('source_list') || '',
        alias: record.get('alias') || '',
        function: record.get('function') || '',
        original_form: record.get('original_form') || '',
        taste: record.get('taste') || '',
        caution: record.get('caution') || '',
        habitat: record.get('habitat') || '',
        usage_dosage: record.get('usage_dosage') || '',

        // Attributes字段（中文字段名）
        '功能主治': record.get('功能主治') || '',
        '性味': record.get('性味') || '',
        '性味归经': record.get('性味归经') || '',
        '归经': record.get('归经') || '',
        '英文名': record.get('英文名') || '',
        '化学成分': record.get('化学成分') || '',
        '药理作用': record.get('药理作用') || '',
        '临床应用': record.get('临床应用') || '',
        '毒性': record.get('毒性') || '',
        '植物形态': record.get('植物形态') || '',
        '动物形态': record.get('动物形态') || '',
        '药用部位': record.get('药用部位') || '',
        '采收加工': record.get('采收加工') || '',
        '炮制': record.get('炮制') || '',
        '制剂': record.get('制剂') || '',
        '性状': record.get('性状') || '',
        '鉴别': record.get('鉴别') || '',
        '含量测定': record.get('含量测定') || '',
        '注意': record.get('注意') || '',
        '贮藏': record.get('贮藏') || '',
        '备注': record.get('备注') || '',
        '各家论述': record.get('各家论述') || '',
        '相关药方': record.get('相关药方') || '',
        '复方': record.get('复方') || '',
        '拼音注音': record.get('拼音注音') || '',
        '原形态': record.get('原形态') || '',
        '生境分布': record.get('生境分布') || '',
        '主要成分': record.get('主要成分') || '',
        '规格': record.get('规格') || '',
        '制法': record.get('制法') || '',
        '栽培': record.get('栽培') || ''
      };

      res.json({
        success: true,
        data: herb,
        msg: '获取药材详情成功'
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药材详情失败：', err.message);
    res.json({
      success: false,
      msg: '获取药材详情失败：' + err.message
    });
  }
});

// 3. 新增药材
app.post('/api/admin/herbs', checkAdmin, async (req, res) => {
  try {
    const {
      herb_id, name, source_list, alias = '', function: herbFunction = '', original_form = '',
      taste = '', caution = '', habitat = '', usage_dosage = '',
      // Attributes中文字段
      '功能主治': function_indications = '',
      '性味': nature_taste = '',
      '性味归经': nature_taste_channel = '',
      '归经': channel_tropism = '',
      '英文名': english_name = '',
      '化学成分': chemical_composition = '',
      '药理作用': pharmacological_effects = '',
      '临床应用': clinical_applications = '',
      '毒性': toxicity = '',
      '植物形态': plant_morphology = '',
      '动物形态': animal_morphology = '',
      '药用部位': medicinal_part = '',
      '采收加工': harvesting_processing = '',
      '炮制': processing = '',
      '制剂': preparation = '',
      '性状': character = '',
      '鉴别': identification = '',
      '含量测定': content_determination = '',
      '注意': caution_text = '',
      '贮藏': storage = '',
      '备注': note = '',
      '各家论述': discussions = '',
      '相关药方': related_prescriptions = '',
      '复方': compound = '',
      '拼音注音': pinyin = '',
      '原形态': original_morphology = '',
      '生境分布': habitat_distribution = '',
      '主要成分': main_components = '',
      '规格': specifications = '',
      '制法': manufacturing = '',
      '栽培': cultivation = ''
    } = req.body;

    if (!herb_id || !name || !source_list) {
      return res.json({ success: false, msg: '药材ID、名称、来源列表为必填项' });
    }

    const session = neo4jDriver.session();
    try {
      // 检查药材ID和名称是否已存在
      const idCheck = await session.run(
        'MATCH (h:Herb {herb_id: $herb_id}) RETURN h LIMIT 1',
        { herb_id }
      );
      if (idCheck.records.length > 0) {
        return res.json({ success: false, msg: '药材ID已存在' });
      }
      const nameCheck = await session.run(
        'MATCH (h:Herb {name: $name}) RETURN h LIMIT 1',
        { name }
      );
      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '药材名称已存在' });
      }

      // 1. 创建Herb节点
      const createHerbResult = await session.run(
        `CREATE (h:Herb {
          herb_id: $herb_id,
          name: $name,
          source_list: $source_list,
          alias: $alias,
          function: $function,
          original_form: $original_form,
          taste: $taste,
          caution: $caution,
          habitat: $habitat,
          usage_dosage: $usage_dosage
        }) RETURN id(h) as herbId`,
        { herb_id, name, source_list, alias, function: herbFunction, original_form, taste, caution, habitat, usage_dosage }
      );
      const herbId = createHerbResult.records[0]?.get('herbId');
      if (!herbId) {
        return res.json({ success: false, msg: '药材创建失败' });
      }

      // 2. 创建Attributes节点并通过FROM_SOURCE关系连接
      await session.run(
        `MATCH (h:Herb) WHERE id(h) = $herbId
         CREATE (a:Attributes {
          功能主治: $function_indications,
          性味: $nature_taste,
          性味归经: $nature_taste_channel,
          归经: $channel_tropism,
          英文名: $english_name,
          化学成分: $chemical_composition,
          药理作用: $pharmacological_effects,
          临床应用: $clinical_applications,
          毒性: $toxicity,
          植物形态: $plant_morphology,
          动物形态: $animal_morphology,
          药用部位: $medicinal_part,
          采收加工: $harvesting_processing,
          炮制: $processing,
          制剂: $preparation,
          性状: $character,
          鉴别: $identification,
          含量测定: $content_determination,
          注意: $caution_text,
          贮藏: $storage,
          备注: $note,
          各家论述: $discussions,
          相关药方: $related_prescriptions,
          复方: $compound,
          拼音注音: $pinyin,
          原形态: $original_morphology,
          生境分布: $habitat_distribution,
          主要成分: $main_components,
          规格: $specifications,
          制法: $manufacturing,
          栽培: $cultivation
        })
        CREATE (h)-[:FROM_SOURCE]->(a)`,
        {
          herbId,
          function_indications, nature_taste, nature_taste_channel, channel_tropism, english_name,
          chemical_composition, pharmacological_effects, clinical_applications, toxicity, plant_morphology,
          animal_morphology, medicinal_part, harvesting_processing, processing, preparation, character,
          identification, content_determination, caution_text, storage, note, discussions, related_prescriptions,
          compound, pinyin, original_morphology, habitat_distribution, main_components, specifications,
          manufacturing, cultivation
        }
      );

      res.json({
        success: true,
        msg: '药材新增成功',
        data: { id: herbId.toNumber().toString() }
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 新增药材失败：', err.message);
    res.json({ success: false, msg: '新增药材失败：' + err.message });
  }
});

// 4. 修改药材（这是你要的关键功能）
app.put('/api/admin/herbs/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const {
      herb_id, name, source_list, alias = '', function: herbFunction = '', original_form = '',
      taste = '', caution = '', habitat = '', usage_dosage = '',
      // Attributes中文字段
      '功能主治': function_indications = '',
      '性味': nature_taste = '',
      '性味归经': nature_taste_channel = '',
      '归经': channel_tropism = '',
      '英文名': english_name = '',
      '化学成分': chemical_composition = '',
      '药理作用': pharmacological_effects = '',
      '临床应用': clinical_applications = '',
      '毒性': toxicity = '',
      '植物形态': plant_morphology = '',
      '动物形态': animal_morphology = '',
      '药用部位': medicinal_part = '',
      '采收加工': harvesting_processing = '',
      '炮制': processing = '',
      '制剂': preparation = '',
      '性状': character = '',
      '鉴别': identification = '',
      '含量测定': content_determination = '',
      '注意': caution_text = '',
      '贮藏': storage = '',
      '备注': note = '',
      '各家论述': discussions = '',
      '相关药方': related_prescriptions = '',
      '复方': compound = '',
      '拼音注音': pinyin = '',
      '原形态': original_morphology = '',
      '生境分布': habitat_distribution = '',
      '主要成分': main_components = '',
      '规格': specifications = '',
      '制法': manufacturing = '',
      '栽培': cultivation = ''
    } = req.body;

    if (!herb_id || !name || !source_list) {
      return res.json({ success: false, msg: '药材ID、名称、来源列表为必填项' });
    }

    const session = neo4jDriver.session();
    try {
      // 检查药材是否存在
      const herbExist = await session.run(
        'MATCH (h:Herb) WHERE id(h) = $id RETURN h',
        { id: neo4j.int(id) }
      );
      if (herbExist.records.length === 0) {
        return res.json({ success: false, msg: '药材不存在' });
      }

      // 检查ID和名称唯一性
      const idCheck = await session.run(
        'MATCH (h:Herb {herb_id: $herb_id}) WHERE id(h) <> $id RETURN h LIMIT 1',
        { herb_id, id: neo4j.int(id) }
      );
      if (idCheck.records.length > 0) {
        return res.json({ success: false, msg: '药材ID已被占用' });
      }
      const nameCheck = await session.run(
        'MATCH (h:Herb {name: $name}) WHERE id(h) <> $id RETURN h LIMIT 1',
        { name, id: neo4j.int(id) }
      );
      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '药材名称已被占用' });
      }

      // 1. 更新Herb节点（显示本身的信息并修改）
      await session.run(
        `MATCH (h:Herb)
         WHERE id(h) = $id
         SET h.herb_id = $herb_id,
             h.name = $name,
             h.source_list = $source_list,
             h.alias = $alias,
             h.function = $function,
             h.original_form = $original_form,
             h.taste = $taste,
             h.caution = $caution,
             h.habitat = $habitat,
             h.usage_dosage = $usage_dosage`,
        { id: neo4j.int(id), herb_id, name, source_list, alias, function: herbFunction, original_form, taste, caution, habitat, usage_dosage }
      );

      // 2. 更新Attributes节点（通过FROM_SOURCE关系查找）
      const attrExist = await session.run(
        'MATCH (h:Herb)-[:FROM_SOURCE]->(a:Attributes) WHERE id(h) = $id RETURN a',
        { id: neo4j.int(id) }
      );

      if (attrExist.records.length > 0) {
        // 存在则更新
        await session.run(
          `MATCH (h:Herb)-[:FROM_SOURCE]->(a:Attributes)
           WHERE id(h) = $id
           SET a.功能主治 = $function_indications,
               a.性味 = $nature_taste,
               a.性味归经 = $nature_taste_channel,
               a.归经 = $channel_tropism,
               a.英文名 = $english_name,
               a.化学成分 = $chemical_composition,
               a.药理作用 = $pharmacological_effects,
               a.临床应用 = $clinical_applications,
               a.毒性 = $toxicity,
               a.植物形态 = $plant_morphology,
               a.动物形态 = $animal_morphology,
               a.药用部位 = $medicinal_part,
               a.采收加工 = $harvesting_processing,
               a.炮制 = $processing,
               a.制剂 = $preparation,
               a.性状 = $character,
               a.鉴别 = $identification,
               a.含量测定 = $content_determination,
               a.注意 = $caution_text,
               a.贮藏 = $storage,
               a.备注 = $note,
               a.各家论述 = $discussions,
               a.相关药方 = $related_prescriptions,
               a.复方 = $compound,
               a.拼音注音 = $pinyin,
               a.原形态 = $original_morphology,
               a.生境分布 = $habitat_distribution,
               a.主要成分 = $main_components,
               a.规格 = $specifications,
               a.制法 = $manufacturing,
               a.栽培 = $cultivation`,
          {
            id: neo4j.int(id), function_indications, nature_taste, nature_taste_channel, channel_tropism,
            english_name, chemical_composition, pharmacological_effects, clinical_applications, toxicity,
            plant_morphology, animal_morphology, medicinal_part, harvesting_processing, processing,
            preparation, character, identification, content_determination, caution_text, storage, note,
            discussions, related_prescriptions, compound, pinyin, original_morphology, habitat_distribution,
            main_components, specifications, manufacturing, cultivation
          }
        );
      } else {
        // 不存在则创建并关联
        await session.run(
          `MATCH (h:Herb)
           WHERE id(h) = $id
           CREATE (a:Attributes {
             功能主治: $function_indications,
             性味: $nature_taste,
             性味归经: $nature_taste_channel,
             归经: $channel_tropism,
             英文名: $english_name,
             化学成分: $chemical_composition,
             药理作用: $pharmacological_effects,
             临床应用: $clinical_applications,
             毒性: $toxicity,
             植物形态: $plant_morphology,
             动物形态: $animal_morphology,
             药用部位: $medicinal_part,
             采收加工: $harvesting_processing,
             炮制: $processing,
             制剂: $preparation,
             性状: $character,
             鉴别: $identification,
             含量测定: $content_determination,
             注意: $caution_text,
             贮藏: $storage,
             备注: $note,
             各家论述: $discussions,
             相关药方: $related_prescriptions,
             复方: $compound,
             拼音注音: $pinyin,
             原形态: $original_morphology,
             生境分布: $habitat_distribution,
             主要成分: $main_components,
             规格: $specifications,
             制法: $manufacturing,
             栽培: $cultivation
           })
           CREATE (h)-[:FROM_SOURCE]->(a)`,
          {
            id: neo4j.int(id), function_indications, nature_taste, nature_taste_channel, channel_tropism,
            english_name, chemical_composition, pharmacological_effects, clinical_applications, toxicity,
            plant_morphology, animal_morphology, medicinal_part, harvesting_processing, processing,
            preparation, character, identification, content_determination, caution_text, storage, note,
            discussions, related_prescriptions, compound, pinyin, original_morphology, habitat_distribution,
            main_components, specifications, manufacturing, cultivation
          }
        );
      }

      res.json({
        success: true,
        msg: '药材修改成功',
        data: { id: id }
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 修改药材失败：', err.message);
    res.json({ success: false, msg: '修改药材失败：' + err.message });
  }
});

// 5. 删除药材
app.delete('/api/admin/herbs/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      // 检查药材是否存在
      const existResult = await session.run(
        'MATCH (h:Herb) WHERE id(h) = $id RETURN h LIMIT 1',
        { id: neo4j.int(id) }
      );
      if (existResult.records.length === 0) {
        return res.json({ success: false, msg: '药材不存在' });
      }

      // 删除药材和关联的Attributes节点
      await session.run(
        'MATCH (h:Herb)-[r:FROM_SOURCE]->(a:Attributes) WHERE id(h) = $id DETACH DELETE h, a',
        { id: neo4j.int(id) }
      );

      res.json({ success: true, msg: '药材删除成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 删除药材失败：', err.message);
    res.json({ success: false, msg: '删除药材失败：' + err.message });
  }
});

// ============================== 三、药方管理（优化版，字段与图数据库一致） ==============================
// 获取药材选择列表（用于药方新增/编辑）
app.get('/api/admin/herbs/select', checkAdmin, async (req, res) => {
  try {
    const { search = '' } = req.query;
    const session = neo4jDriver.session();
    try {
      const result = await session.run(
        `MATCH (h:Herb)
         WHERE h.name CONTAINS $search OR h.herb_id CONTAINS $search
         RETURN id(h) as id, h.herb_id as herb_id, h.name as name
         ORDER BY h.name
         LIMIT 100`,
        { search }
      );
      const data = result.records.map(record => {
        const id = record.get('id');
        return {
          id: id.toNumber ? id.toNumber().toString() : id.toString(),
          herb_id: record.get('herb_id') || '',
          name: record.get('name') || '',
          label: `${record.get('name')} (${record.get('herb_id') || '无ID'})`,
          value: id.toNumber ? id.toNumber().toString() : id.toString()
        };
      });
      res.json({
        success: true,
        data: data,
        msg: '获取药材选择列表成功'
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药材选择列表失败：', err.message);
    res.json({ success: false, msg: '获取药材选择列表失败：' + err.message });
  }
});

// 新增药方（字段与图数据库示例一致）
app.post('/api/admin/fangji', checkAdmin, async (req, res) => {
  try {
    const {
      name, excerpt = '', function: fangjiFunction = '', prescription = '',
      usage = '', caution = '', preparation = '', herbIds = [], book = '', since = ''
    } = req.body;
    if (!name || !herbIds || herbIds.length === 0) {
      return res.json({ success: false, msg: '药方名称和药材组成为必填项' });
    }
    const session = neo4jDriver.session();
    try {
      // 检查药方名称是否已存在
      const nameCheck = await session.run(
        'MATCH (f:Fangji {name: $name}) RETURN f LIMIT 1',
        { name }
      );
      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '药方名称已存在' });
      }
      // 检查药材是否存在
      const herbIdsList = herbIds.map(item => neo4j.int(item.id));
      const herbCheckResult = await session.run(
        `MATCH (h:Herb) WHERE id(h) IN $herbIds RETURN collect(id(h)) as existIds`,
        { herbIds: herbIdsList }
      );
      if (herbCheckResult.records.length === 0) {
        return res.json({ success: false, msg: '药材ID列表为空' });
      }
      const existIds = herbCheckResult.records[0].get('existIds') || [];
      const existIdStrings = existIds.map(id => id.toString());
      const invalidIds = herbIdsList.filter(id => !existIdStrings.includes(id.toString()));
      if (invalidIds.length > 0) {
        return res.json({ success: false, msg: `以下药材不存在：${invalidIds.join(',')}，请从药材库选择` });
      }
      // 创建新药方（字段与示例一致：caution、excerpt、function等）
      const createResult = await session.run(
        `CREATE (f:Fangji {
          name: $name,
          excerpt: $excerpt, // 出处（如《御药院方》）
          function: $function, // 功能主治（如牙齿疼痛）
          prescription: $prescription, // 药方组成（如槐枝1两半、乳香2钱半）
          usage: $usage, // 用法（如水煎服）
          caution: $caution, // 禁忌（如忌甘甜之物）
          preparation: $preparation, // 制备方法
          book: $book,
          since: $since
        }) RETURN id(f) as id`,
        { name, excerpt, function: fangjiFunction, prescription, usage, caution, preparation, book, since }
      );
      const createdId = createResult.records[0]?.get('id');
      if (!createdId) {
        return res.json({ success: false, msg: '药方创建失败' });
      }
      // 创建药材关系（HAS_HERB）
      for (const herbItem of herbIds) {
        await session.run(
          `MATCH (f:Fangji), (h:Herb)
           WHERE id(f) = $fangjiId AND id(h) = $herbId
           CREATE (f)-[:HAS_HERB {dosage: $dosage}]->(h)`,
          {
            fangjiId: createdId,
            herbId: neo4j.int(herbItem.id),
            dosage: herbItem.dosage || ''
          }
        );
      }
      res.json({
        success: true,
        msg: '药方新增成功',
        data: { id: createdId.toNumber().toString() }
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 新增药方失败：', err.message);
    res.json({ success: false, msg: '新增药方失败：' + err.message });
  }
});

// 获取药方列表（包含完整字段）
app.get('/api/admin/fangji', checkAdmin, async (req, res) => {
  try {
    const { search = '', page = 1, pageSize = 20 } = req.query;
    const pageNum = parseInt(page, 10) || 1;
    const pageSizeNum = parseInt(pageSize, 10) || 20;
    const skip = Math.max(0, (pageNum - 1) * pageSizeNum);
    const limit = Math.max(1, pageSizeNum);
    const session = neo4jDriver.session();
    try {
      // 总数查询
      const countQuery = `MATCH (f:Fangji) WHERE f.name CONTAINS $search RETURN count(f) as total`;
      const countResult = await session.run(countQuery, { search });
      const total = countResult.records[0]?.get('total')?.low || 0;
      // 列表查询（包含caution、prescription等字段）
      const listQuery = `
        MATCH (f:Fangji)
        WHERE f.name CONTAINS $search
        RETURN id(f) AS id,
               f.name AS name,
               f.function AS function,
               f.excerpt AS excerpt,
               f.prescription AS prescription,
               f.usage AS usage,
               f.caution AS caution,
               f.preparation AS preparation,
               f.book AS book,
               f.since AS since
        ORDER BY f.name
        SKIP $skip LIMIT $limit
      `;
      const listResult = await session.run(listQuery, {
        search,
        skip: neo4j.int(skip),
        limit: neo4j.int(limit)
      });
      const data = listResult.records.map(record => {
        const id = record.get('id');
        return {
          id: id.toNumber ? id.toNumber().toString() : id.toString(),
          name: record.get('name') || '',
          function: record.get('function') || '',
          excerpt: record.get('excerpt') || '',
          prescription: record.get('prescription') || '',
          usage: record.get('usage') || '',
          caution: record.get('caution') || '',
          preparation: record.get('preparation') || '',
          book: record.get('book') || '',
          since: record.get('since') || ''
        };
      });
      res.json({
        success: true,
        data: data,
        total: total,
        msg: '获取药方列表成功'
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药方列表失败：', err.message);
    res.json({ success: false, msg: '获取药方列表失败：' + err.message });
  }
});

// 获取药方详情（包含药材关联）
app.get('/api/admin/fangji/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      const result = await session.run(
        `MATCH (f:Fangji)
         WHERE id(f) = $id
         OPTIONAL MATCH (f)-[r:HAS_HERB]->(h:Herb)
         RETURN f.name as name,
                f.excerpt as excerpt,
                f.function as function,
                f.prescription as prescription,
                f.usage as usage,
                f.caution as caution,
                f.preparation as preparation,
                f.book as book,
                f.since as since,
                collect({
                  id: id(h),
                  herb_id: h.herb_id,
                  name: h.name,
                  dosage: r.dosage
                }) as herbs`,
        { id: neo4j.int(id) }
      );
      if (result.records.length === 0) {
        return res.json({ success: false, msg: '药方不存在' });
      }
      const record = result.records[0];
      const fangji = {
        id: id,
        name: record.get('name') || '',
        excerpt: record.get('excerpt') || '', // 出处
        function: record.get('function') || '', // 功能主治
        prescription: record.get('prescription') || '', // 药方组成
        usage: record.get('usage') || '', // 用法
        caution: record.get('caution') || '', // 禁忌
        preparation: record.get('preparation') || '', // 制备
        book: record.get('book') || '',
        since: record.get('since') || '',
        herbs: record.get('herbs').map(herb => ({
          id: herb.id.toNumber ? herb.id.toNumber().toString() : herb.id.toString(),
          herb_id: herb.herb_id || '',
          name: herb.name || '',
          dosage: herb.dosage || ''
        })) || []
      };
      res.json({ success: true, data: fangji, msg: '获取药方详情成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药方详情失败：', err.message);
    res.json({ success: false, msg: '获取药方详情失败：' + err.message });
  }
});
// ========== 修改功能 ==========
// 修改药方
app.put('/api/admin/fangji/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const {
      name, excerpt = '', function: fangjiFunction = '', prescription = '',
      usage = '', caution = '', preparation = '', herbIds = [], book = '', since = ''
    } = req.body;

    if (!name) {
      return res.json({ success: false, msg: '药方名称为必填项' });
    }

    const session = neo4jDriver.session();
    try {
      // 检查药方是否存在
      const fangjiExist = await session.run(
        'MATCH (f:Fangji) WHERE id(f) = $id RETURN f LIMIT 1',
        { id: neo4j.int(id) }
      );
      if (fangjiExist.records.length === 0) {
        return res.json({ success: false, msg: '药方不存在' });
      }

      // 检查药方名称是否被其他药方使用
      const nameCheck = await session.run(
        'MATCH (f:Fangji {name: $name}) WHERE id(f) <> $id RETURN f LIMIT 1',
        { name, id: neo4j.int(id) }
      );
      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '药方名称已被占用' });
      }

      // 1. 更新药方基本信息
      await session.run(
        `MATCH (f:Fangji)
         WHERE id(f) = $id
         SET f.name = $name,
             f.excerpt = $excerpt,
             f.function = $function,
             f.prescription = $prescription,
             f.usage = $usage,
             f.caution = $caution,
             f.preparation = $preparation,
             f.book = $book,
             f.since = $since`,
        {
          id: neo4j.int(id),
          name,
          excerpt,
          function: fangjiFunction,
          prescription,
          usage,
          caution,
          preparation,
          book,
          since
        }
      );

      // 2. 如果有药材信息，更新药材关系
      if (herbIds && herbIds.length > 0) {
        // 检查药材是否存在
        const herbIdsList = herbIds.map(item => neo4j.int(item.id));
        const herbCheckResult = await session.run(
          `MATCH (h:Herb) WHERE id(h) IN $herbIds RETURN collect(id(h)) as existIds`,
          { herbIds: herbIdsList }
        );
        if (herbCheckResult.records.length > 0) {
          const existIds = herbCheckResult.records[0].get('existIds') || [];
          const existIdStrings = existIds.map(id => id.toString());
          const invalidIds = herbIdsList.filter(id => !existIdStrings.includes(id.toString()));

          if (invalidIds.length === 0) {
            // 删除旧的药材关系
            await session.run(
              'MATCH (f:Fangji)-[r:HAS_HERB]->(:Herb) WHERE id(f) = $id DELETE r',
              { id: neo4j.int(id) }
            );

            // 创建新的药材关系
            for (const herbItem of herbIds) {
              await session.run(
                `MATCH (f:Fangji), (h:Herb)
                 WHERE id(f) = $fangjiId AND id(h) = $herbId
                 CREATE (f)-[:HAS_HERB {dosage: $dosage}]->(h)`,
                {
                  fangjiId: neo4j.int(id),
                  herbId: neo4j.int(herbItem.id),
                  dosage: herbItem.dosage || ''
                }
              );
            }
          } else {
            console.warn(`部分药材不存在：${invalidIds.join(',')}`);
          }
        }
      }

      res.json({
        success: true,
        msg: '药方修改成功',
        data: { id: id }
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 修改药方失败：', err.message);
    res.json({ success: false, msg: '修改药方失败：' + err.message });
  }
});

// ========== 删除功能 ==========
// 删除药方
app.delete('/api/admin/fangji/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      // 检查药方是否存在
      const existResult = await session.run(
        'MATCH (f:Fangji) WHERE id(f) = $id RETURN f LIMIT 1',
        { id: neo4j.int(id) }
      );
      if (existResult.records.length === 0) {
        return res.json({ success: false, msg: '药方不存在' });
      }

      // 删除药方及其所有关系
      await session.run(
        'MATCH (f:Fangji) WHERE id(f) = $id DETACH DELETE f',
        { id: neo4j.int(id) }
      );

      res.json({ success: true, msg: '药方删除成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 删除药方失败：', err.message);
    res.json({ success: false, msg: '删除药方失败：' + err.message });
  }
});
// ============================== 四、来源管理 ==============================
// 获取来源列表
app.get('/api/admin/sources', checkAdmin, async (req, res) => {
  try {
    const { search = '', page = 1, pageSize = 20 } = req.query;
    const pageNum = parseInt(page, 10) || 1;
    const pageSizeNum = parseInt(pageSize, 10) || 20;
    const skip = Math.max(0, (pageNum - 1) * pageSizeNum);
    const limit = Math.max(1, pageSizeNum);

    const session = neo4jDriver.session();
    try {
      // 总数查询
      const countQuery = `MATCH (s:Source) WHERE s.name CONTAINS $search RETURN count(s) as total`;
      const countResult = await session.run(countQuery, { search });
      const total = countResult.records[0]?.get('total')?.low || 0;

      // 列表查询
      const listQuery = `
        MATCH (s:Source)
        WHERE s.name CONTAINS $search
        RETURN id(s) as id, s.name as name
        ORDER BY s.name
        SKIP $skip LIMIT $limit
      `;

      const listResult = await session.run(listQuery, {
        search,
        skip: neo4j.int(skip),
        limit: neo4j.int(limit)
      });

      const data = listResult.records.map(record => {
        const id = record.get('id');
        return {
          id: id.toNumber ? id.toNumber().toString() : id.toString(),
          name: record.get('name') || ''
        };
      });

      res.json({
        success: true,
        data: data,
        total: total,
        msg: '获取来源列表成功'
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取来源列表失败：', err.message);
    res.json({ success: false, msg: '获取来源列表失败：' + err.message });
  }
});

// 获取单个来源详情
app.get('/api/admin/sources/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      const result = await session.run(
        'MATCH (s:Source) WHERE id(s) = $id RETURN s.name as name',
        { id: neo4j.int(id) }
      );

      if (result.records.length === 0) {
        return res.json({ success: false, msg: '来源不存在' });
      }

      const record = result.records[0];
      const source = {
        id: id,
        name: record.get('name') || ''
      };

      res.json({ success: true, data: source, msg: '获取来源详情成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取来源详情失败：', err.message);
    res.json({ success: false, msg: '获取来源详情失败：' + err.message });
  }
});

// 新增来源
app.post('/api/admin/sources', checkAdmin, async (req, res) => {
  try {
    const { name } = req.body;

    if (!name || name.trim() === '') {
      return res.json({ success: false, msg: '来源名称不能为空' });
    }

    const session = neo4jDriver.session();
    try {
      // 检查来源名称是否已存在
      const nameCheck = await session.run(
        'MATCH (s:Source {name: $name}) RETURN s LIMIT 1',
        { name }
      );

      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '来源名称已存在' });
      }

      // 创建来源节点
      const createResult = await session.run(
        'CREATE (s:Source {name: $name}) RETURN id(s) as id',
        { name }
      );

      const sourceId = createResult.records[0]?.get('id');
      if (!sourceId) {
        return res.json({ success: false, msg: '来源创建失败' });
      }

      res.json({
        success: true,
        msg: '来源新增成功',
        data: { id: sourceId.toNumber().toString() }
      });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 新增来源失败：', err.message);
    res.json({ success: false, msg: '新增来源失败：' + err.message });
  }
});

// 编辑来源
app.put('/api/admin/sources/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const { name } = req.body;

    if (!name || name.trim() === '') {
      return res.json({ success: false, msg: '来源名称不能为空' });
    }

    const session = neo4jDriver.session();
    try {
      // 检查来源是否存在
      const sourceExist = await session.run(
        'MATCH (s:Source) WHERE id(s) = $id RETURN s',
        { id: neo4j.int(id) }
      );

      if (sourceExist.records.length === 0) {
        return res.json({ success: false, msg: '来源不存在' });
      }

      // 检查名称是否被其他来源使用
      const nameCheck = await session.run(
        'MATCH (s:Source {name: $name}) WHERE id(s) <> $id RETURN s LIMIT 1',
        { name, id: neo4j.int(id) }
      );

      if (nameCheck.records.length > 0) {
        return res.json({ success: false, msg: '来源名称已被占用' });
      }

      // 更新来源
      await session.run(
        'MATCH (s:Source) WHERE id(s) = $id SET s.name = $name',
        { id: neo4j.int(id), name }
      );

      res.json({ success: true, msg: '来源编辑成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 编辑来源失败：', err.message);
    res.json({ success: false, msg: '编辑来源失败：' + err.message });
  }
});

// 删除来源
app.delete('/api/admin/sources/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      // 检查来源是否存在
      const existResult = await session.run(
        'MATCH (s:Source) WHERE id(s) = $id RETURN s LIMIT 1',
        { id: neo4j.int(id) }
      );

      if (existResult.records.length === 0) {
        return res.json({ success: false, msg: '来源不存在' });
      }

      // 检查是否有药材引用此来源
      const herbRefCheck = await session.run(
        'MATCH (h:Herb)-[:FROM_SOURCE]->(s:Source) WHERE id(s) = $id RETURN h LIMIT 1',
        { id: neo4j.int(id) }
      );

      if (herbRefCheck.records.length > 0) {
        return res.json({
          success: false,
          msg: '无法删除该来源，已有药材引用此来源，请先修改相关药材的来源引用'
        });
      }

      // 删除来源
      await session.run(
        'MATCH (s:Source) WHERE id(s) = $id DETACH DELETE s',
        { id: neo4j.int(id) }
      );

      res.json({ success: true, msg: '来源删除成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 删除来源失败：', err.message);
    res.json({ success: false, msg: '删除来源失败：' + err.message });
  }
});

// 修改药材查询接口，修复字段映射问题
// 在原有的药材详情查询中，确保字段正确映射
// 这是原来的药材详情查询，需要确保字段正确返回
// 问题可能在于：查询返回的是中文字段名，但前端使用的是普通字段名
// 建议修改查询，同时返回两种格式

// 修改药材详情查询（替代原来的查询）
app.get('/api/admin/herbs/:id', checkAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const session = neo4jDriver.session();
    try {
      const result = await session.run(
        `MATCH (h:Herb)
         WHERE id(h) = $id
         OPTIONAL MATCH (h)-[:FROM_SOURCE]->(s:Source)
         OPTIONAL MATCH (h)-[:HAS_ATTRIBUTES]->(a:Attributes)
         RETURN h.herb_id as herb_id, h.name as name, h.source_list as source_list,
                h.alias as alias, h.function as function, h.original_form as original_form,
                h.taste as taste, h.caution as caution, h.habitat as habitat, h.usage_dosage as usage_dosage,
                collect(DISTINCT s.id) as source_ids, collect(DISTINCT s.name) as source_names,
                // 返回Attributes的所有属性
                properties(a) as attributes`,
        { id: neo4j.int(id) }
      );

      if (result.records.length === 0) {
        return res.json({ success: false, msg: '药材不存在' });
      }

      const record = result.records[0];
      const attributes = record.get('attributes') || {};

      const herb = {
        id: id,
        herb_id: record.get('herb_id') || '',
        name: record.get('name') || '',
        source_list: record.get('source_list') || '',
        alias: record.get('alias') || '',
        function: record.get('function') || '',
        original_form: record.get('original_form') || '',
        taste: record.get('taste') || '',
        caution: record.get('caution') || '',
        habitat: record.get('habitat') || '',
        usage_dosage: record.get('usage_dosage') || '',
        source_ids: record.get('source_ids').map(id => id.toNumber ? id.toNumber().toString() : id.toString()) || [],
        source_names: record.get('source_names') || [],
        // 直接使用Attributes的所有属性
        ...attributes
      };

      res.json({ success: true, data: herb, msg: '获取药材详情成功' });
    } finally {
      await session.close();
    }
  } catch (err) {
    console.error('❌ 获取药材详情失败：', err.message);
    res.json({ success: false, msg: '获取药材详情失败：' + err.message });
  }
});
// ============================== 启动服务 ==============================
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`🚀 管理员后端服务启动成功：http://localhost:${PORT}`);
  console.log(`🔐 管理员Token：${ADMIN_TOKEN}`);
  console.log(`📌 支持接口列表：`);
  console.log(`  用户管理: GET/PUT /api/admin/users`);
  console.log(`  药材管理: GET/POST/PUT/DELETE /api/admin/herbs`);
  console.log(`  药方管理: GET/POST/PUT/DELETE /api/admin/fangji`);
  console.log(`  来源管理: GET/POST/PUT/DELETE /api/admin/sources`);
  console.log(`  药材选择: GET /api/admin/herbs/select (用于药方新增)`);
  console.log(`  属性字段: GET /api/admin/attributes/fields`);
});
// 优雅关闭
process.on('SIGINT', async () => {
  console.log('\n📤 正在关闭数据库连接...');
  mysqlDb.end((err) => {
    if (err) console.error('❌ MySQL关闭失败：', err.message);
    else console.log('✅ MySQL连接已关闭');
  });
  await neo4jDriver.close();
  console.log('✅ Neo4j连接已关闭');
  process.exit(0);
});