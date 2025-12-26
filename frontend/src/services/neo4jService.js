import neo4j from 'neo4j-driver'

const NEO4J_URI = 'bolt://10.138.238.141:7687'
const NEO4J_USER = 'neo4j'
const NEO4J_PASSWORD = '12345678'

let driver = null

const neo4jService = {
  // 连接到数据库
  connect() {
    try {
      driver = neo4j.driver(NEO4J_URI, neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD))
      console.log('Neo4j 连接成功')
      return driver
    } catch (error) {
      console.error('Neo4j 连接失败:', error)
      throw error
    }
  },

  // 断开连接
  disconnect() {
    if (driver) {
      driver.close()
      driver = null
    }
  },

  // 获取连接实例
  getDriver() {
    if (!driver) {
      this.connect()
    }
    return driver
  },

  // 精确查询药材或方剂
  async queryExact(name) {
    const session = this.getDriver().session()
    try {
      // 先查中药
      let result = await session.run(
        `
        MATCH (h:Herb {name: $name})
        OPTIONAL MATCH (h)-[:FROM_SOURCE]->(a:Attributes)
        RETURN h.name AS name, collect(a) AS attrs
        `,
        { name }
      )

      if (result.records.length > 0) {
        const record = result.records[0]
        const herbName = record.get('name')
        const attrs = record.get('attrs') || []
        return { type: 'herb', name: herbName, data: attrs }
      }

      // 再查方剂
      result = await session.run(
        `
        MATCH (f:Fangji {name: $name})
        RETURN f
        `,
        { name }
      )

      if (result.records.length > 0) {
        const fangjiNode = result.records[0].get('f')
        return { type: 'fangji', name: name, data: fangjiNode.properties }
      }

      return null
    } catch (error) {
      console.error('查询错误:', error)
      throw error
    } finally {
      await session.close()
    }
  },

  // 获取图谱数据
  async getGraphData(centerName, centerType, limit = 20) {
    const session = this.getDriver().session()
    try {
      let relatedNames = []

      if (centerType === 'herb') {
        const res = await session.run(
          `MATCH (h:Herb {name: $name})-[:HAS_HERB]-(f:Fangji) RETURN collect(f.name) AS names`,
          { name: centerName }
        )
        relatedNames = res.records[0]?.get('names') || []
      } else {
        const res = await session.run(
          `MATCH (f:Fangji {name: $name})-[:HAS_HERB]-(h:Herb) RETURN collect(h.name) AS names`,
          { name: centerName }
        )
        relatedNames = res.records[0]?.get('names') || []
      }

      // 随机打乱并限制数量
      const shuffled = relatedNames.sort(() => 0.5 - Math.random())
      const limitedRelated = shuffled.slice(0, limit)

      const nodes = [{ id: centerName, type: centerType === 'herb' ? 'herb' : 'prescription' }]
      const links = []

      limitedRelated.forEach(relName => {
        nodes.push({ id: relName, type: centerType === 'herb' ? 'prescription' : 'herb' })
        links.push({ source: centerName, target: relName })
      })

      return { nodes, links }
    } catch (error) {
      console.error('图谱查询错误:', error)
      throw error
    } finally {
      await session.close()
    }
  },

  // 获取搜索建议
  async getSuggestions(keyword) {
    if (keyword.trim().length < 2) {
      return []
    }

    const session = this.getDriver().session()
    try {
      const result = await session.run(
        `
        MATCH (n)
        WHERE (n:Herb OR n:Fangji) AND toLower(n.name) CONTAINS toLower($keyword)
        RETURN n.name AS name, labels(n) AS labels
        ORDER BY n.name
        LIMIT 10
        `,
        { keyword: keyword.trim() }
      )

      return result.records.map(record => ({
        name: record.get('name'),
        labels: record.get('labels')
      }))
    } catch (error) {
      console.error('建议查询错误:', error)
      return []
    } finally {
      await session.close()
    }
  }
}

export default neo4jService