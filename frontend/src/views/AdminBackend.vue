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
          {{ activeMenu === 'user' ? '用户管理' : activeMenu === 'herb' ? '中药材管理' : '药方管理' }}
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
                  {{'删除' }}
                </button>
              </td>
            </tr>
            <tr v-if="userList.length === 0 && !userLoading">
              <td colspan="6" class="empty-text">暂无用户数据</td>
            </tr>
            <tr v-if="userLoading">
              <td colspan="6" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 中药材管理模块（Neo4j） -->
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

      <!-- 药方管理模块（Neo4j） -->
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

      <!-- 评论管理模块 -->
      <div v-if="activeMenu === 'comment'" class="content-module">
        <div class="module-header">
          <h2>评论列表</h2>
          <button class="add-btn" @click="openCommentModal('add')">新增评论</button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户ID</th>
              <th>用户名</th>
              <th>内容</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in commentList" :key="comment.id">
              <td>{{ comment.id }}</td>
              <td>{{ comment.user_id }}</td>
              <td>{{ comment.username }}</td>
              <td>{{ comment.content }}</td>
              <td>{{ formatTime(comment.created_at) }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openCommentModal('edit', comment)">编辑</button>
                <button class="oper-btn delete-btn" @click="handleCommentDelete(comment.id)">删除</button>
              </td>
            </tr>
            <tr v-if="commentList.length === 0 && !commentLoading">
              <td colspan="6" class="empty-text">暂无评论数据</td>
            </tr>
            <tr v-if="commentLoading">
              <td colspan="6" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- 中药材模态框 -->
    <el-dialog
      v-model="herbModalVisible"
      title="">{{ herbModalType === 'add' ? '新增中药材' : '编辑中药材' }}
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

    <!-- 药方模态框 -->
    <el-dialog
      v-model="prescriptionModalVisible"
      title="">{{ prescriptionModalType === 'add' ? '新增药方' : '编辑药方' }}
      <el-form :model="prescriptionForm" label-width="80px" class="modal-form">
        <el-form-item label="药方名称" required>
          <el-input v-model="prescriptionForm.name" placeholder="请输入药方名称"></el-input>
        </el-form-item>
        <el-form-item label="组成药材" required>
          <el-select
            v-model="prescriptionForm.herbIds"
            multiple
            placeholder="请选择组成药材"
            style="width: 100%"
          >
            <el-option
              v-for="herb in allHerbs"
              :key="herb.id"
              :label="herb.name"
              :value="herb.id"
            ></el-option>
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

    <!-- 评论模态框 -->
    <el-dialog
      v-model="commentModalVisible"
      title="">{{ commentModalType === 'add' ? '新增评论' : '编辑评论' }}
      <el-form :model="commentForm" label-width="80px" class="modal-form">
        <el-form-item label="用户ID" required>
          <el-input v-model="commentForm.user_id" placeholder="填写用户ID"></el-input>
        </el-form-item>
        <el-form-item label="用户名" required>
          <el-input v-model="commentForm.username" placeholder="填写用户名"></el-input>
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input
            v-model="commentForm.content"
            type="textarea"
            placeholder="填写评论内容"
            :autosize="{ minRows: 3, maxRows: 6 }"
          ></el-input>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
// 引入Element Plus组件（需安装：npm install element-plus）
import { ElDialog, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton } from 'element-plus'
import 'element-plus/dist/index.css'

const router = useRouter()

// 状态管理
const activeMenu = ref('user') // 当前激活菜单：user/herb/prescription
const userList = ref([]) // 用户列表
const herbList = ref([]) // 中药材列表
const prescriptionList = ref([]) // 药方列表
const allHerbs = ref([]) // 所有中药材（用于药方选择）
const commentList = ref([]) // 评论列表

// 加载状态
const userLoading = ref(false)
const herbLoading = ref(false)
const prescriptionLoading = ref(false)
const commentLoading = ref(false)

// 搜索条件
const userSearch = ref('')
const herbSearch = ref('')
const prescriptionSearch = ref('')

// 模态框状态
const herbModalVisible = ref(false)
const herbModalType = ref('add') // add/edit
const herbForm = ref({
  id: '',
  name: '',
  property: '',
  taste: '',
  efficacy: ''
})

const prescriptionModalVisible = ref(false)
const prescriptionModalType = ref('add')
const prescriptionForm = ref({
  id: '',
  name: '',
  herbIds: [],
  efficacy: ''
})

const commentModalVisible = ref(false)
const commentModalType = ref('add')
const commentForm = ref({
  id: '',
  user_id: '',
  username: '',
  content: ''
})

// 常量定义
const ADMIN_TOKEN = 'admin_fixed_token_123456'

// 页面加载时初始化数据
onMounted(() => {
  fetchUsers()
  fetchHerbs()
  fetchPrescriptions()
  fetchComments()
})

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('adminToken')
  router.push('/admin/login')
}

// ------------------------------ MySQL用户管理（逻辑删除）------------------------------
// 获取用户列表
const fetchUsers = async () => {
  userLoading.value = true
  try {
    const res = await axios.get('/api/admin/users', {
      params: { search: userSearch.value }, // 传递搜索参数
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })

    if (res.data.success) {
      userList.value = res.data.data
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('获取用户列表失败：' + (err.response?.data?.msg || err.message))
    console.error('请求详情：', err.response?.data || err.message)
  } finally {
    userLoading.value = false
  }
}

// 逻辑删除用户（isDeleted=1）
const handleUserDelete = async (userId) => {
  if (!confirm('确定要删除该用户吗？')) return

  try {
    const res = await axios.put(
      `/api/admin/users/${userId}/delete`,
      {},
      {
        headers: {
          Authorization: `Bearer ${ADMIN_TOKEN}`
        }
      }
    )

    if (res.data.success) {
      alert('用户删除成功')
      fetchUsers() // 刷新列表
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('用户删除失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  }
}

// ------------------------------ Neo4j中药材管理（增删改查）------------------------------
// 获取中药材列表
const fetchHerbs = async () => {
  herbLoading.value = true
  try {
    const res = await axios.get('/api/admin/herbs', {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })
    if (res.data.success) {
      herbList.value = res.data.data
      allHerbs.value = res.data.data // 同步到药方选择列表
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('获取中药材列表失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  } finally {
    herbLoading.value = false
  }
}

// 打开中药材模态框
const openHerbModal = (type, herb = {}) => {
  herbModalType.value = type
  herbModalVisible.value = true

  if (type === 'add') {
    herbForm.value = { id: '', name: '', property: '', taste: '', efficacy: '' }
  } else {
    herbForm.value = { ...herb }
  }
}

// 提交中药材表单（新增）
const submitHerbForm = async () => {
  if (!herbForm.value.name || !herbForm.value.efficacy) {
    alert('请填写药材名称和功效')
    return
  }

  try {
    let res
    if (herbModalType.value === 'add') {
      // 新增中药材 - 根据后端API，只需要name和efficacy
      res = await axios.post(
        '/api/admin/herbs',
        {
          name: herbForm.value.name,
          efficacy: herbForm.value.efficacy
        },
        {
          headers: {
            Authorization: `Bearer ${ADMIN_TOKEN}`
          }
        }
      )
    } else {
      // 编辑中药材 - 注意：后端没有提供编辑API！
      alert('抱歉，后端暂未提供编辑药材的API接口')
      herbModalVisible.value = false
      return
    }

    if (res.data.success) {
      alert(herbModalType.value === 'add' ? '中药材新增成功' : '中药材编辑成功')
      herbModalVisible.value = false
      fetchHerbs() // 刷新列表
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert(herbModalType.value === 'add' ? '中药材新增失败' : '中药材编辑失败')
    console.error(err)
  }
}

// 删除中药材
const handleHerbDelete = async (herbId) => {
  if (!confirm('确定要删除该中药材吗？')) return

  try {
    const res = await axios.delete(`/api/admin/herbs/${herbId}`, {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })

    if (res.data.success) {
      alert('中药材删除成功')
      fetchHerbs()
      fetchPrescriptions() // 刷新药方列表
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('中药材删除失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  }
}

// ------------------------------ Neo4j药方管理（增删改查）------------------------------
// 获取药方列表
const fetchPrescriptions = async () => {
  prescriptionLoading.value = true
  try {
    const res = await axios.get('/api/admin/prescriptions', {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })
    if (res.data.success) {
      prescriptionList.value = res.data.data
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('获取药方列表失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  } finally {
    prescriptionLoading.value = false
  }
}

// 打开药方模态框
const openPrescriptionModal = (type, prescription = {}) => {
  prescriptionModalType.value = type
  prescriptionModalVisible.value = true

  if (type === 'add') {
    prescriptionForm.value = { id: '', name: '', herbIds: [], efficacy: '' }
  } else {
    // 注意：后端API返回的prescription没有herbs属性，只有herbs数组
    const herbIds = prescription.herbs ? prescription.herbs.map(herb => herb.id || herb.name) : []
    prescriptionForm.value = {
      id: prescription.id,
      name: prescription.name,
      herbIds,
      efficacy: prescription.efficacy || ''
    }
  }
}

// 提交药方表单（新增）
const submitPrescriptionForm = async () => {
  if (!prescriptionForm.value.name || prescriptionForm.value.herbIds.length === 0) {
    alert('请填写药方名称并选择组成药材')
    return
  }

  try {
    let res
    if (prescriptionModalType.value === 'add') {
      // 新增药方 - 根据后端API，只需要name和herbIds
      res = await axios.post(
        '/api/admin/prescriptions',
        {
          name: prescriptionForm.value.name,
          herbIds: prescriptionForm.value.herbIds
        },
        {
          headers: {
            Authorization: `Bearer ${ADMIN_TOKEN}`
          }
        }
      )
    } else {
      // 编辑药方 - 注意：后端没有提供编辑API！
      alert('抱歉，后端暂未提供编辑药方的API接口')
      prescriptionModalVisible.value = false
      return
    }

    if (res.data.success) {
      alert(prescriptionModalType.value === 'add' ? '药方新增成功' : '药方编辑成功')
      prescriptionModalVisible.value = false
      fetchPrescriptions() // 刷新列表
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert(prescriptionModalType.value === 'add' ? '药方新增失败' : '药方编辑失败')
    console.error(err)
  }
}

// 删除药方
const handlePrescriptionDelete = async (prescriptionId) => {
  if (!confirm('确定要删除该药方吗？')) return

  try {
    const res = await axios.delete(`/api/admin/prescriptions/${prescriptionId}`, {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })

    if (res.data.success) {
      alert('药方删除成功')
      fetchPrescriptions()
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('药方删除失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  }
}

// ------------------------------ 评论管理（增删改查）------------------------------
const formatTime = (val) => (val ? new Date(val).toLocaleString() : '')

const fetchComments = async () => {
  commentLoading.value = true
  try {
    const res = await axios.get('/api/admin/comments', {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })
    if (res.data.success) {
      commentList.value = res.data.data
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('获取评论列表失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  } finally {
    commentLoading.value = false
  }
}

const openCommentModal = (type, comment = {}) => {
  commentModalType.value = type
  commentModalVisible.value = true
  if (type === 'add') {
    commentForm.value = { id: '', user_id: '', username: '', content: '' }
  } else {
    commentForm.value = { ...comment }
  }
}

const submitCommentForm = async () => {
  if (!commentForm.value.user_id || !commentForm.value.username || !commentForm.value.content) {
    alert('请完整填写用户ID、用户名与内容')
    return
  }

  try {
    let res
    if (commentModalType.value === 'add') {
      res = await axios.post(
        '/api/admin/comments',
        {
          userId: commentForm.value.user_id,
          username: commentForm.value.username,
          content: commentForm.value.content
        },
        {
          headers: {
            Authorization: `Bearer ${ADMIN_TOKEN}`
          }
        }
      )
    } else {
      res = await axios.put(
        `/api/admin/comments/${commentForm.value.id}`,
        {
          userId: commentForm.value.user_id,
          username: commentForm.value.username,
          content: commentForm.value.content
        },
        {
          headers: {
            Authorization: `Bearer ${ADMIN_TOKEN}`
          }
        }
      )
    }

    if (res.data.success) {
      alert(commentModalType.value === 'add' ? '评论新增成功' : '评论更新成功')
      commentModalVisible.value = false
      fetchComments()
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert(commentModalType.value === 'add' ? '评论新增失败' : '评论更新失败')
    console.error(err)
  }
}

const handleCommentDelete = async (id) => {
  if (!confirm('确定删除该评论吗？')) return
  try {
    const res = await axios.delete(`/api/admin/comments/${id}`, {
      headers: {
        Authorization: `Bearer ${ADMIN_TOKEN}`
      }
    })
    if (res.data.success) {
      alert('删除成功')
      fetchComments()
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('删除失败：' + (err.response?.data?.msg || err.message))
    console.error(err)
  }
}

// 添加退出登录导航函数
const navigate = (path) => {
  router.push(path)
}
</script>

<style scoped>
/* 布局样式 */
.admin-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

/* 侧边栏样式（匹配深绿色主题） */
.sidebar {
  width: 220px;
  background: #2d7d46;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 25px 0;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-logo {
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 1px;
}

.sidebar-menu {
  flex: 1;
  padding: 20px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px 30px;
  cursor: pointer;
  transition: all 0.3s;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background: #226338;
  border-left: 4px solid #5fb378;
}

.menu-icon {
  margin-right: 12px;
  font-size: 16px;
}

.menu-text {
  font-size: 15px;
}

/* 退出按钮样式 */
.logout-btn {
  margin: 20px;
  padding: 12px;
  background: #5fb378;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: #4a9c66;
}

/* 主内容区样式 */
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.content-header {
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.page-title {
  font-size: 24px;
  color: #333;
  font-weight: 600;
}

/* 模块样式 */
.content-module {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 25px;
  margin-bottom: 30px;
}

.module-header {
  margin-bottom: 20px;
}

.module-header h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 8px;
}

.tip {
  font-size: 13px;
  color: #999;
}

/* 搜索栏样式 */
.search-bar {
  display: flex;
  margin-bottom: 25px;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 14px;
}

.search-btn {
  padding: 0 20px;
  background: #2d7d46;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn:hover {
  background: #226338;
}

.add-btn {
  padding: 8px 16px;
  background: #2d7d46;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.add-btn:hover {
  background: #226338;
}

/* 表格样式 */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.data-table th, .data-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background: #fafafa;
  color: #333;
  font-weight: 600;
}

.status-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.status-normal {
  background: #e8f4f8;
  color: #2d7d46;
}

.status-disabled {
  background: #fdf2f8;
  color: #e53e3e;
}

.operation {
  display: flex;
  gap: 10px;
}

.oper-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.edit-btn {
  background: #e8f4f8;
  color: #2d7d46;
}

.edit-btn:hover {
  background: #d1e7dd;
}

.delete-btn {
  background: #fdf2f8;
  color: #e53e3e;
}

.delete-btn:hover {
  background: #fef7fb;
}

.delete-btn:disabled {
  background: #f5f5f5;
  color: #ccc;
  cursor: not-allowed;
}

.empty-text, .loading-text {
  text-align: center;
  color: #999;
  padding: 30px 0;
}

/* 药方药材标签 */
.herb-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.herb-tag {
  display: inline-block;
  padding: 4px 8px;
  background: #e8f4f8;
  color: #2d7d46;
  border-radius: 4px;
  font-size: 12px;
}

/* 模态框样式 */
.modal-form {
  margin-top: 20px;
}
</style>
