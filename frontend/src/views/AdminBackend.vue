<template>
  <div class="admin-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="admin-logo">中医药智能平台 管理后台</span>
      </div>
      <nav class="sidebar-menu">
        <div class="menu-item" :class="{ active: activeMenu === 'user' }" @click="activeMenu = 'user'">
          <li class="menu-icon">👥</li>
          <span class="menu-text">用户管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'herb' }" @click="activeMenu = 'herb'">
          <li class="menu-icon">🌿</li>
          <span class="menu-text">中药材管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'prescription' }" @click="activeMenu = 'prescription'">
          <li class="menu-icon">📜</li>
          <span class="menu-text">药方管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'comment' }" @click="activeMenu = 'comment'">
          <li class="menu-icon">💬</li>
          <span class="menu-text">评论管理</span>
        </div>
      </nav>
      <button class="logout-btn" @click="navigate('/')">退出登录</button>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="content-header">
        <h1 class="page-title">
          {{ activeMenu === 'user' ? '用户管理' : activeMenu === 'herb' ? '中药材管理' : activeMenu === 'prescription' ? '药方管理' : '评论情感监控' }}
        </h1>
      </header>

      <!-- 用户管理模块 -->
      <div v-if="activeMenu === 'user'" class="content-module">
        <div class="module-header">
          <h2>用户列表</h2>
        </div>

        <div class="search-bar">
          <input
            v-model="userSearch"
            type="text"
            placeholder="搜索用户名/手机号"
            class="search-input"
          >
          <button class="search-btn" @click="fetchUsers">搜索</button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>手机号</th>
              <th>邮箱</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in userList" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.phonenumber }}</td>
              <td>{{ user.email }}</td>
              <td class="operation">
                <button
                  class="oper-btn delete-btn"
                  @click="handleUserDelete(user.id)"
                  :disabled="user.is_deleted"
                >
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="userList.length === 0 && !userLoading">
              <td colspan="5" class="empty-text">暂无用户数据</td>
            </tr>
            <tr v-if="userLoading">
              <td colspan="5" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 中药材管理模块 -->
      <div v-if="activeMenu === 'herb'" class="content-module">
        <div class="module-header">
          <h2>中药材列表</h2>
          <button class="add-btn" @click="openHerbModal('add')">新增中药材</button>
        </div>

        <div class="search-bar">
          <input
            v-model="herbSearch"
            type="text"
            placeholder="搜索药材名称"
            class="search-input"
          >
          <button class="search-btn" @click="fetchHerbs">搜索</button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>药材名称</th>
              <th>性味</th>
              <th>功效</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="herb in herbList" :key="herb.id">
              <td>{{ herb.id }}</td>
              <td>{{ herb.name }}</td>
              <td>{{ herb.property }}（{{ herb.taste }}）</td>
              <td>{{ herb.efficacy }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openHerbModal('edit', herb)">编辑</button>
                <button class="oper-btn delete-btn" @click="handleHerbDelete(herb.id)">删除</button>
              </td>
            </tr>
            <tr v-if="herbList.length === 0 && !herbLoading">
              <td colspan="5" class="empty-text">暂无中药材数据</td>
            </tr>
            <tr v-if="herbLoading">
              <td colspan="5" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 药方管理模块 -->
      <div v-if="activeMenu === 'prescription'" class="content-module">
        <div class="module-header">
          <h2>药方列表</h2>
          <button class="add-btn" @click="openPrescriptionModal('add')">新增药方</button>
        </div>

        <div class="search-bar">
          <input
            v-model="prescriptionSearch"
            type="text"
            placeholder="搜索药方名称"
            class="search-input"
          >
          <button class="search-btn" @click="fetchPrescriptions">搜索</button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>药方名称</th>
              <th>组成药材</th>
              <th>功效主治</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prescription in prescriptionList" :key="prescription.id">
              <td>{{ prescription.id }}</td>
              <td>{{ prescription.name }}</td>
              <td>
                <div class="herb-tags">
                  <span class="herb-tag" v-for="herb in prescription.herbs" :key="herb.id">{{ herb.name }}</span>
                </div>
              </td>
              <td>{{ prescription.efficacy }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openPrescriptionModal('edit', prescription)">编辑</button>
                <button class="oper-btn delete-btn" @click="handlePrescriptionDelete(prescription.id)">删除</button>
              </td>
            </tr>
            <tr v-if="prescriptionList.length === 0 && !prescriptionLoading">
              <td colspan="5" class="empty-text">暂无药方数据</td>
            </tr>
            <tr v-if="prescriptionLoading">
              <td colspan="5" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ==================== 评论管理模块 (集成情感分析) ==================== -->
      <div v-if="activeMenu === 'comment'" class="content-module">
        <div class="module-header">
          <h2>评论列表与情感分析</h2>
          <button class="add-btn" @click="openCommentModal('add')">新增评论</button>
        </div>

        <!-- 情感统计卡片 (新增) -->
        <div class="stats-row">
          <div class="stat-card positive">
            <h3>正面反馈 😊</h3>
            <div class="number">{{ commentStats.positive }}</div>
          </div>
          <div class="stat-card neutral">
            <h3>中性反馈 😐</h3>
            <div class="number">{{ commentStats.neutral }}</div>
          </div>
          <div class="stat-card negative">
            <h3>负面反馈 😡</h3>
            <div class="number">{{ commentStats.negative }}</div>
          </div>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th width="50">ID</th>
              <th width="100">用户名</th>
              <th>内容</th>
              <th width="120">情感得分</th>
              <th width="100">分析结果</th>
              <th width="160">创建时间</th>
              <th width="140">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in commentList" :key="comment.id">
              <td>{{ comment.id }}</td>
              <td>{{ comment.username }}</td>
              <td class="content-cell">{{ comment.content }}</td>

              <!-- 情感得分列 (新增) -->
              <td>
                <div class="score-container">
                  <div class="score-bar-bg">
                    <div class="score-bar-fill"
                         :style="{ width: ((comment.sentiment_score || 0.5) * 100) + '%', background: getScoreColor(comment.sentiment_score) }">
                    </div>
                  </div>
                  <span class="score-text">{{ comment.sentiment_score?.toFixed(2) || '0.50' }}</span>
                </div>
              </td>

              <!-- 分析结果标签列 (新增) -->
              <td>
                <span :class="['sentiment-badge', comment.sentiment || 'neutral']">
                  {{ getSentimentLabel(comment.sentiment) }}
                </span>
              </td>

              <td>{{ formatTime(comment.created_at) }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openCommentModal('edit', comment)">编辑</button>
                <button class="oper-btn delete-btn" @click="handleCommentDelete(comment.id)">删除</button>
              </td>
            </tr>
            <tr v-if="commentList.length === 0 && !commentLoading">
              <td colspan="7" class="empty-text">暂无评论数据</td>
            </tr>
            <tr v-if="commentLoading">
              <td colspan="7" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- 模态框组件 (保持不变) -->
    <el-dialog v-model="herbModalVisible" :title="herbModalType === 'add' ? '新增中药材' : '编辑中药材'">
      <el-form :model="herbForm" label-width="80px" class="modal-form">
        <el-form-item label="药材名称" required>
          <el-input v-model="herbForm.name" placeholder="请输入药材名称"></el-input>
        </el-form-item>
        <el-form-item label="性味" required>
          <el-select v-model="herbForm.property" placeholder="请选择性味">
            <el-option label="性平" value="性平"></el-option>
            <el-option label="性温" value="性温"></el-option>
            <el-option label="性寒" value="性寒"></el-option>
            <el-option label="性凉" value="性凉"></el-option>
            <el-option label="性热" value="性热"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="味道" required>
          <el-input v-model="herbForm.taste" placeholder="请输入味道（如：甘、甘辛）"></el-input>
        </el-form-item>
        <el-form-item label="功效" required>
          <el-input v-model="herbForm.efficacy" placeholder="请输入功效（如：养心安神、补血活血）"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="herbModalVisible = false">取消</el-button>
        <el-button type="primary" @click="submitHerbForm">{{ herbModalType === 'add' ? '新增' : '保存' }}</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="prescriptionModalVisible" :title="prescriptionModalType === 'add' ? '新增药方' : '编辑药方'">
      <el-form :model="prescriptionForm" label-width="80px" class="modal-form">
        <el-form-item label="药方名称" required>
          <el-input v-model="prescriptionForm.name" placeholder="请输入药方名称"></el-input>
        </el-form-item>
        <el-form-item label="组成药材" required>
          <el-select v-model="prescriptionForm.herbIds" multiple placeholder="请选择组成药材" style="width: 100%">
            <el-option v-for="herb in allHerbs" :key="herb.id" :label="herb.name" :value="herb.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="功效主治" required>
          <el-input v-model="prescriptionForm.efficacy" placeholder="请输入功效主治"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="prescriptionModalVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPrescriptionForm">{{ prescriptionModalType === 'add' ? '新增' : '保存' }}</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="commentModalVisible" :title="commentModalType === 'add' ? '新增评论' : '编辑评论'">
      <el-form :model="commentForm" label-width="80px" class="modal-form">
        <el-form-item label="用户ID" required>
          <el-input v-model="commentForm.user_id" placeholder="填写用户ID"></el-input>
        </el-form-item>
        <el-form-item label="用户名" required>
          <el-input v-model="commentForm.username" placeholder="填写用户名"></el-input>
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="commentForm.content" type="textarea" placeholder="填写评论内容" :autosize="{ minRows: 3, maxRows: 6 }"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="commentModalVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCommentForm">{{ commentModalType === 'add' ? '新增' : '保存' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' // 引入 computed
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElDialog, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton } from 'element-plus'
import 'element-plus/dist/index.css'

const router = useRouter()

// 状态管理
const activeMenu = ref('user')
const userList = ref([])
const herbList = ref([])
const prescriptionList = ref([])
const allHerbs = ref([])
const commentList = ref([])

// 加载状态
const userLoading = ref(false)
const herbLoading = ref(false)
const prescriptionLoading = ref(false)
const commentLoading = ref(false)

// 搜索条件
const userSearch = ref('')
const herbSearch = ref('')
const prescriptionSearch = ref('')

// 模态框状态 (herb, prescription, comment) ... 保持不变
const herbModalVisible = ref(false)
const herbModalType = ref('add')
const herbForm = ref({ id: '', name: '', property: '', taste: '', efficacy: '' })

const prescriptionModalVisible = ref(false)
const prescriptionModalType = ref('add')
const prescriptionForm = ref({ id: '', name: '', herbIds: [], efficacy: '' })

const commentModalVisible = ref(false)
const commentModalType = ref('add')
const commentForm = ref({ id: '', user_id: '', username: '', content: '' })

const ADMIN_TOKEN = 'admin_fixed_token_123456'

onMounted(() => {
  fetchUsers()
  fetchHerbs()
  fetchPrescriptions()
  fetchComments()
})

const handleLogout = () => {
  localStorage.removeItem('adminToken')
  router.push('/admin/login')
}

// ------------------------------ 情感分析逻辑 (新增) ------------------------------

// 计算评论统计数据
const commentStats = computed(() => {
  if (!commentList.value) return { positive: 0, neutral: 0, negative: 0 }
  return {
    positive: commentList.value.filter(c => c.sentiment === 'positive').length,
    neutral: commentList.value.filter(c => c.sentiment === 'neutral' || !c.sentiment).length,
    negative: commentList.value.filter(c => c.sentiment === 'negative').length,
  }
})

// 获取标签文本
const getSentimentLabel = (val) => {
  const map = { 'positive': '正面', 'neutral': '中性', 'negative': '负面' }
  return map[val] || '中性'
}

// 获取得分条颜色
const getScoreColor = (score) => {
  if (!score) return '#ffd93d' // 默认黄
  if (score >= 0.6) return '#42b983' // 绿
  if (score <= 0.4) return '#ff6b6b' // 红
  return '#ffd93d' // 黄
}

// ------------------------------ 下面是原有的数据获取逻辑 ------------------------------

// 用户管理
const fetchUsers = async () => {
  userLoading.value = true
  try {
    const res = await axios.get('/api/admin/users', {
      params: { search: userSearch.value },
      headers: { Authorization: `Bearer ${ADMIN_TOKEN}` }
    })
    if (res.data.success) userList.value = res.data.data
    else alert(res.data.msg)
  } catch (err) {
    console.error(err)
  } finally {
    userLoading.value = false
  }
}

const handleUserDelete = async (userId) => {
  if (!confirm('确定要删除该用户吗？')) return
  try {
    const res = await axios.put(`/api/admin/users/${userId}/delete`, {}, {
      headers: { Authorization: `Bearer ${ADMIN_TOKEN}` }
    })
    if (res.data.success) { alert('用户删除成功'); fetchUsers() }
    else alert(res.data.msg)
  } catch (err) { alert('操作失败') }
}

// 中药材管理
const fetchHerbs = async () => {
  herbLoading.value = true
  try {
    const res = await axios.get('/api/admin/herbs', { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { herbList.value = res.data.data; allHerbs.value = res.data.data }
  } catch (err) { console.error(err) }
  finally { herbLoading.value = false }
}

const openHerbModal = (type, herb = {}) => {
  herbModalType.value = type
  herbModalVisible.value = true
  herbForm.value = type === 'add' ? { id: '', name: '', property: '', taste: '', efficacy: '' } : { ...herb }
}

const submitHerbForm = async () => {
  if (!herbForm.value.name || !herbForm.value.efficacy) return alert('请填写完整')
  try {
    const url = '/api/admin/herbs'
    const method = herbModalType.value === 'add' ? 'post' : 'post' // 你的后端似乎没提供编辑接口，暂时都用add逻辑演示
    if (herbModalType.value !== 'add') return alert('暂不支持编辑')

    const res = await axios[method](url, { name: herbForm.value.name, efficacy: herbForm.value.efficacy }, { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { alert('操作成功'); herbModalVisible.value = false; fetchHerbs() }
    else alert(res.data.msg)
  } catch (err) { console.error(err) }
}

const handleHerbDelete = async (herbId) => {
  if (!confirm('确定删除？')) return
  try {
    const res = await axios.delete(`/api/admin/herbs/${herbId}`, { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { alert('删除成功'); fetchHerbs() }
  } catch (err) { console.error(err) }
}

// 药方管理
const fetchPrescriptions = async () => {
  prescriptionLoading.value = true
  try {
    const res = await axios.get('/api/admin/prescriptions', { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) prescriptionList.value = res.data.data
  } catch (err) { console.error(err) }
  finally { prescriptionLoading.value = false }
}

const openPrescriptionModal = (type, prescription = {}) => {
  prescriptionModalType.value = type
  prescriptionModalVisible.value = true
  if (type === 'add') {
    prescriptionForm.value = { id: '', name: '', herbIds: [], efficacy: '' }
  } else {
    const herbIds = prescription.herbs ? prescription.herbs.map(h => h.id || h.name) : []
    prescriptionForm.value = { id: prescription.id, name: prescription.name, herbIds, efficacy: prescription.efficacy || '' }
  }
}

const submitPrescriptionForm = async () => {
  if (prescriptionModalType.value !== 'add') return alert('暂不支持编辑')
  try {
    const res = await axios.post('/api/admin/prescriptions', { name: prescriptionForm.value.name, herbIds: prescriptionForm.value.herbIds }, { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { alert('操作成功'); prescriptionModalVisible.value = false; fetchPrescriptions() }
  } catch (err) { console.error(err) }
}

const handlePrescriptionDelete = async (id) => {
  if (!confirm('确定删除？')) return
  try {
    const res = await axios.delete(`/api/admin/prescriptions/${id}`, { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { alert('删除成功'); fetchPrescriptions() }
  } catch (err) { console.error(err) }
}

// 评论管理
const fetchComments = async () => {
  commentLoading.value = true
  try {
    const res = await axios.get('/api/admin/comments', { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) commentList.value = res.data.data
    else alert(res.data.msg)
  } catch (err) { console.error(err) }
  finally { commentLoading.value = false }
}

const openCommentModal = (type, comment = {}) => {
  commentModalType.value = type
  commentModalVisible.value = true
  commentForm.value = type === 'add' ? { id: '', user_id: '', username: '', content: '' } : { ...comment }
}

const submitCommentForm = async () => {
  // 1. 简单校验
  if (!commentForm.value.user_id || !commentForm.value.content) {
    alert('请填写用户ID和内容');
    return;
  }

  try {
    let res;
    // 2. 根据是新增还是编辑，发送不同请求
    if (commentModalType.value === 'add') {
      // 新增
      res = await axios.post(
        '/api/admin/comments',
        {
          userId: commentForm.value.user_id,
          // username 后端不需要存，后端是根据 userId 查的，或者在 admin 端不重要
          content: commentForm.value.content
        },
        {
          headers: { Authorization: `Bearer ${ADMIN_TOKEN}` }
        }
      );
    } else {
      // 编辑
      res = await axios.put(
        `/api/admin/comments/${commentForm.value.id}`,
        {
          // 编辑时只需要传 content 即可
          content: commentForm.value.content
        },
        {
          headers: { Authorization: `Bearer ${ADMIN_TOKEN}` }
        }
      );
    }

    // 3. 处理结果
    if (res.data.success) {
      alert('操作成功');
      commentModalVisible.value = false;
      fetchComments(); // 刷新列表
    } else {
      alert('操作失败: ' + res.data.msg);
    }
  } catch (err) {
    console.error(err);
    alert('请求出错');
  }
};

const handleCommentDelete = async (id) => {
  if (!confirm('确定删除？')) return
  try {
    const res = await axios.delete(`/api/admin/comments/${id}`, { headers: { Authorization: `Bearer ${ADMIN_TOKEN}` } })
    if (res.data.success) { alert('删除成功'); fetchComments() }
  } catch (err) { console.error(err) }
}

const navigate = (path) => router.push(path)
const formatTime = (val) => val ? new Date(val).toLocaleString() : ''
</script>

<style scoped>
/* 保持原有样式 */
.admin-container { display: flex; height: 100vh; background-color: #f5f5f5; }
.sidebar { width: 220px; background: #2d7d46; color: #fff; display: flex; flex-direction: column; }
.sidebar-header { padding: 25px 0; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
.admin-logo { font-size: 18px; font-weight: bold; letter-spacing: 1px; }
.sidebar-menu { flex: 1; padding: 20px 0; }
.menu-item { display: flex; align-items: center; padding: 15px 30px; cursor: pointer; transition: all 0.3s; }
.menu-item:hover { background: rgba(255, 255, 255, 0.1); }
.menu-item.active { background: #226338; border-left: 4px solid #5fb378; }
.menu-icon { margin-right: 12px; font-size: 16px; }
.logout-btn { margin: 20px; padding: 12px; background: #5fb378; color: #fff; border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
.logout-btn:hover { background: #4a9c66; }
.main-content { flex: 1; padding: 20px; overflow-y: auto; }
.content-header { margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.page-title { font-size: 24px; color: #333; font-weight: 600; }
.content-module { background: #fff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); padding: 25px; margin-bottom: 30px; }
.module-header { margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
.module-header h2 { font-size: 18px; color: #333; }
.search-bar { display: flex; margin-bottom: 25px; gap: 10px; }
.search-input { flex: 1; padding: 12px 15px; border: 1px solid #eee; border-radius: 8px; }
.search-btn, .add-btn { padding: 8px 20px; background: #2d7d46; color: #fff; border: none; border-radius: 8px; cursor: pointer; transition: 0.3s; }
.search-btn:hover, .add-btn:hover { background: #226338; }
.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th, .data-table td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
.data-table th { background: #fafafa; color: #333; font-weight: 600; }
.operation { display: flex; gap: 10px; }
.oper-btn { padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; transition: 0.3s; }
.edit-btn { background: #e8f4f8; color: #2d7d46; }
.edit-btn:hover { background: #d1e7dd; }
.delete-btn { background: #fdf2f8; color: #e53e3e; }
.delete-btn:hover { background: #fef7fb; }
.delete-btn:disabled { background: #f5f5f5; color: #ccc; cursor: not-allowed; }
.empty-text, .loading-text { text-align: center; color: #999; padding: 30px 0; }
.herb-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.herb-tag { padding: 4px 8px; background: #e8f4f8; color: #2d7d46; border-radius: 4px; font-size: 12px; }
.modal-form { margin-top: 20px; }

/* === 新增：情感分析样式 === */
.stats-row { display: flex; gap: 20px; margin-bottom: 24px; }
.stat-card { flex: 1; background: #f9f9f9; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #eee; }
.stat-card h3 { margin: 0 0 10px; font-size: 14px; color: #666; }
.stat-card .number { font-size: 28px; font-weight: bold; }
.positive .number { color: #42b983; }
.neutral .number { color: #ffd93d; }
.negative .number { color: #ff6b6b; }

.content-cell { max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.score-container { display: flex; align-items: center; gap: 8px; }
.score-bar-bg { width: 80px; height: 6px; background: #eee; border-radius: 3px; overflow: hidden; }
.score-bar-fill { height: 100%; transition: width 0.3s; }
.score-text { font-size: 12px; color: #999; width: 30px; }

.sentiment-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
.sentiment-badge.positive { background: #e8f5ef; color: #42b983; }
.sentiment-badge.neutral { background: #fff8e1; color: #f59f00; }
.sentiment-badge.negative { background: #ffeaea; color: #ff6b6b; }
</style>