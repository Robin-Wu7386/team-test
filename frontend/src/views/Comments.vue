<template>
  <div class="comments-page">
    <!-- 头部区域 -->
    <div class="hero">
      <div>
        <p class="sub-title">社区留言</p>
        <h1>与岐黄同行，分享你的想法</h1>
        <p class="desc">登录后可发布评论，管理员负责维护内容质量。</p>
      </div>
      <!-- 登录状态 -->
      <div class="user-status" v-if="isLoggedIn">
        <div class="avatar">{{ (currentUser.username || 'U').slice(0, 1).toUpperCase() }}</div>
        <div>
          <div class="name">{{ currentUser.username }}</div>
          <div class="phone">{{ currentUser.phonenumber }}</div>
        </div>
        <button class="logout" @click="handleLogout">退出</button>
      </div>
      <!-- 未登录状态 -->
      <div class="user-status guest" v-else>
        <span>需要登录后才能发表评论</span>
        <button class="primary" @click="router.push('/login')">去登录</button>
      </div>
    </div>

    <div class="content">
      <!-- 1. 主评论发布框 -->
      <section class="card mb-4">
        <header class="card-header">
          <h3>发布评论</h3>
          <span class="tip">文明发言，共建和谐社区。</span>
        </header>
        <div v-if="isLoggedIn" class="editor">
          <textarea v-model="draft" placeholder="想和大家分享些什么？"></textarea>
          <div class="editor-actions">
            <span class="counter">{{ draft.length }} / 300</span>
            <button class="primary" :disabled="draftDisabled" @click="submitComment">发布</button>
          </div>
        </div>
        <div v-else class="editor-disabled">
          请先登录后再发表评论。
        </div>
      </section>

      <!-- 2. 评论列表区域 -->
      <section class="card">
        <header class="card-header">
          <div class="tabs">
            <button :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">全部评论</button>
            <button :class="{ active: activeTab === 'mine' }" @click="activeTab = 'mine'">我的评论</button>
          </div>
          <button class="ghost" @click="fetchComments">刷新</button>
        </header>

        <!-- 加载状态 -->
        <div v-if="loading" class="empty">加载中...</div>
        <div v-else-if="rootComments.length === 0" class="empty">暂无评论，快来抢沙发！</div>

        <!-- 评论列表 -->
        <div class="comment-list" v-else>
          <!-- 循环渲染每一个根评论 -->
          <div v-for="comment in rootComments" :key="comment.id" class="comment-item">
            <!-- 根评论头像 -->
            <div class="comment-avatar">{{ (comment.username || 'U').slice(0, 1).toUpperCase() }}</div>

            <div class="comment-body">
              <!-- 根评论信息 -->
              <div class="meta">
                <span class="author">{{ comment.username }}</span>
                <span class="time">{{ formatTime(comment.created_at) }}</span>
              </div>
              <p class="content-text">{{ comment.content }}</p>

              <!-- 根评论操作栏 -->
              <div class="actions">
                <button class="action-btn" @click="initReply(comment)">
                  <i class="ri-chat-1-line"></i> 回复
                </button>
                <span v-if="comment.user_id === currentUser.id" class="badge">我的</span>
              </div>

              <!-- 根评论下的回复输入框 (仅当点击回复时显示) -->
              <div v-if="replyingTo && replyingTo.id === comment.id" class="reply-editor">
                <textarea
                  v-model="replyDraft"
                  :placeholder="`回复 @${replyingTo.username}...`"
                  ref="replyInput"
                ></textarea>
                <div class="reply-actions">
                  <button class="cancel-btn" @click="cancelReply">取消</button>
                  <button class="submit-btn" :disabled="!replyDraft.trim()" @click="submitReply(comment.id)">发送</button>
                </div>
              </div>

              <!-- 子评论（楼中楼）列表 -->
              <div class="replies" v-if="getReplies(comment.id).length > 0">
                <div v-for="reply in getReplies(comment.id)" :key="reply.id" class="reply-item">
                  <div class="reply-avatar">{{ (reply.username || 'U').slice(0, 1).toUpperCase() }}</div>
                  <div class="reply-content">
                    <div class="meta">
                      <span class="author">{{ reply.username }}</span>
                      <span class="reply-tag" v-if="reply.reply_to_username">
                        回复 <span class="at-name">@{{ reply.reply_to_username }}</span>
                      </span>
                      <span class="time">{{ formatTime(reply.created_at) }}</span>
                    </div>
                    <p class="content-text">{{ reply.content }}</p>

                    <div class="actions">
                      <!-- 点击这里，也是在当前根评论下回复，但标记回复了谁 -->
                      <button class="action-btn" @click="initReply(reply, comment.id)">
                        <i class="ri-chat-1-line"></i> 回复
                      </button>
                    </div>

                    <!-- 子评论下的回复输入框 -->
                    <div v-if="replyingTo && replyingTo.id === reply.id" class="reply-editor">
                      <textarea
                        v-model="replyDraft"
                        :placeholder="`回复 @${replyingTo.username}...`"
                      ></textarea>
                      <div class="reply-actions">
                        <button class="cancel-btn" @click="cancelReply">取消</button>
                        <button class="submit-btn" :disabled="!replyDraft.trim()" @click="submitReply(comment.id)">发送</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 结束子评论 -->

            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 数据状态
const comments = ref([])
const loading = ref(false)
const draft = ref('')
const activeTab = ref(route.query.tab === 'mine' ? 'mine' : 'all')

// 回复状态
const replyingTo = ref(null) // 当前正在回复的对象 { id, username, rootId }
const replyDraft = ref('')   // 回复框的内容

// 计算属性
const isLoggedIn = computed(() => !!userStore.userInfo)
const currentUser = computed(() => userStore.userInfo || {})
const draftDisabled = computed(() => draft.value.trim().length === 0 || draft.value.length > 300)

// 1. 获取所有“根评论” (parent_id 为 null 的评论)
const rootComments = computed(() => {
  let list = comments.value.filter(c => !c.parent_id)

  if (activeTab.value === 'mine' && isLoggedIn.value) {
    // 筛选只看我发的
    list = list.filter(c => c.user_id === currentUser.value.id)
  }

  // 按时间倒序，最新的在上面
  return list.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

// 2. 获取某个根评论下的所有“子回复”
const getReplies = (rootId) => {
  // 找出 parent_id 等于该 rootId 的所有评论
  return comments.value
    .filter(c => c.parent_id === rootId)
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at)) // 回复按时间正序
}

// 格式化时间
const formatTime = (val) => {
  if (!val) return ''
  return new Date(val).toLocaleString()
}

// 3. 从后端拉取评论列表
const fetchComments = async () => {
  loading.value = true
  try {
    // 【关键修改】直接使用完整后端地址，绕过代理
    const res = await axios.get('http://localhost:3001/comments')
    if (res.data.success) {
      comments.value = res.data.data
    } else {
      console.error(res.data.msg)
    }
  } catch (err) {
    console.error('获取评论失败', err)
    // alert('连接服务器失败，请确认 node server.js 已启动')
  } finally {
    loading.value = false
  }
}

// 4. 提交主评论
const submitComment = async () => {
  if (!isLoggedIn.value) return router.push('/login')
  if (draftDisabled.value) return

  try {
    const payload = {
      userId: currentUser.value.id,
      content: draft.value.trim()
    }

    // 【关键修改】直接使用完整后端地址，绕过代理
    const res = await axios.post('http://localhost:3001/comments', payload)

    if (res.data.success) {
      draft.value = ''
      // 后端返回了新创建的评论完整数据，直接插入列表头部
      comments.value.unshift(res.data.data)
      alert('发布成功！')
    } else {
      alert('发布失败: ' + res.data.msg)
    }
  } catch (err) {
    console.error(err)
    alert('发布失败，请检查网络')
  }
}

// 5. 点击“回复”按钮，初始化回复框
const initReply = (comment, rootId = null) => {
  if (!isLoggedIn.value) return router.push('/login')

  // 设置正在回复的状态
  replyingTo.value = {
    id: comment.id,
    username: comment.username,
    // 如果传入了 rootId，说明是在回复子评论；如果没有，说明是在回复根评论本身
    rootId: rootId || comment.id
  }
  replyDraft.value = ''
}

// 取消回复
const cancelReply = () => {
  replyingTo.value = null
  replyDraft.value = ''
}

// 6. 提交回复
const submitReply = async (finalRootId) => {
  if (!replyDraft.value.trim()) return

  try {
    const payload = {
      userId: currentUser.value.id,
      content: replyDraft.value.trim(),
      parentId: finalRootId,  // 数据库里存的 parent_id
      replyToUsername: replyingTo.value.username // 数据库里存的“回复给谁”
    }

    // 【关键修改】直接使用完整后端地址，绕过代理
    const res = await axios.post('http://localhost:3001/comments', payload)

    if (res.data.success) {
      // 将新回复加入到本地列表，computed 会自动将其渲染到对应的楼层里
      comments.value.push(res.data.data)
      cancelReply() // 关闭回复框
    } else {
      alert('回复失败: ' + res.data.msg)
    }
  } catch (err) {
    console.error(err)
    alert('回复请求失败')
  }
}

// 退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 页面加载时拉取数据
onMounted(fetchComments)
</script>

<style scoped>
/* 全局容器样式 */
.comments-page {
  max-width: 1100px;
  margin: 100px auto 60px;
  padding: 0 20px;
  color: #1a3d2e;
}

/* 顶部 Hero 区域 */
.hero {
  background: linear-gradient(135deg, #e8f5ef, #f6fff9);
  border: 1px solid rgba(111, 191, 154, 0.25);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: 0 10px 40px rgba(111, 191, 154, 0.15);
  margin-bottom: 24px;
}
.sub-title { color: #5a8a75; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }
.hero h1 { margin: 0 0 6px; }
.desc { color: #4f6d60; margin: 0; }

/* 用户状态卡片 */
.user-status {
  display: flex; align-items: center; gap: 12px;
  background: #fff; border-radius: 12px; padding: 10px 14px;
  border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}
.avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: #42b983; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
}

/* 卡片通用样式 */
.card {
  background: #fff; border-radius: 16px; padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.04); border: 1px solid #f0f0f0;
}
.mb-4 { margin-bottom: 24px; }
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; border-bottom: 1px solid #eee; padding-bottom: 12px;
}

/* 编辑器样式 */
.editor textarea {
  width: 100%; height: 100px; padding: 12px;
  border: 1px solid #ddd; border-radius: 8px;
  resize: vertical; font-family: inherit;
}
.editor-actions {
  display: flex; justify-content: space-between; align-items: center; margin-top: 8px;
}

/* 按钮样式 */
.primary {
  background: #42b983; color: white; border: none; padding: 8px 16px;
  border-radius: 4px; cursor: pointer; transition: 0.3s;
}
.primary:disabled { background: #ccc; cursor: not-allowed; }
.logout, .ghost {
  background: transparent; border: 1px solid #ddd; padding: 4px 10px;
  border-radius: 4px; cursor: pointer;
}

/* 评论列表样式 */
.comment-list { display: flex; flex-direction: column; gap: 24px; }
.comment-item { display: flex; gap: 16px; }
.comment-avatar {
  width: 40px; height: 40px; border-radius: 50%; background: #eee;
  color: #666; display: flex; align-items: center; justify-content: center;
  font-weight: 700; flex-shrink: 0;
}
.comment-body { flex: 1; }
.meta { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; font-size: 13px; }
.author { font-weight: 700; color: #333; }
.time { color: #999; }
.content-text { margin: 0 0 8px; line-height: 1.5; color: #444; }

/* 操作栏 */
.actions { display: flex; align-items: center; gap: 16px; }
.action-btn {
  background: none; border: none; color: #666; cursor: pointer; font-size: 13px;
  display: flex; align-items: center; gap: 4px; padding: 0;
}
.action-btn:hover { color: #42b983; }

/* 楼中楼（子评论）样式 */
.replies {
  margin-top: 12px; background: #f9f9f9; padding: 12px; border-radius: 8px;
}
.reply-item { display: flex; gap: 10px; margin-bottom: 12px; }
.reply-item:last-child { margin-bottom: 0; }
.reply-avatar {
  width: 24px; height: 24px; border-radius: 50%; background: #ddd;
  color: #666; display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; flex-shrink: 0;
}
.reply-content { flex: 1; font-size: 14px; }
.reply-tag { color: #666; margin-right: 4px; }
.at-name { color: #42b983; font-weight: 500; }

/* 回复输入框动画 */
.reply-editor {
  margin-top: 10px; background: #f0f0f0; padding: 10px;
  border-radius: 8px; animation: fadeIn 0.2s ease;
}
.reply-editor textarea {
  width: 100%; height: 60px; padding: 8px; border: 1px solid #ddd;
  border-radius: 4px; margin-bottom: 8px; font-size: 13px;
}
.reply-actions { display: flex; justify-content: flex-end; gap: 8px; }
.cancel-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; border: none; background: #eee; color: #666; }
.submit-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; border: none; background: #42b983; color: #fff; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Tabs */
.tabs button {
  background: none; border: none; padding: 0 0 8px; margin-right: 20px;
  font-weight: 600; color: #999; cursor: pointer; border-bottom: 2px solid transparent;
}
.tabs button.active { color: #42b983; border-bottom-color: #42b983; }
.badge { background: #e8f5ef; color: #42b983; font-size: 10px; padding: 2px 6px; border-radius: 4px; }
</style>