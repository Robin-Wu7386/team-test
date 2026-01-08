<!-- 文件路径：frontend/src/views/AdminUsers.vue -->
<template>
  <div class="admin-users">
    <h2>用户管理列表</h2>
    <button @click="fetchUsers" class="refresh-btn">刷新列表</button>

    <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; margin-top: 20px;">
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
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.phonenumber }}</td>
          <td>{{ user.email }}</td>
          <td>
            <button class="del-btn" @click="deleteUser(user.id)">禁用</button>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="5" style="text-align: center;">暂无数据或获取失败</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const users = ref([]);

// ！！！必须和 admin_server.js 里的 ADMIN_TOKEN 一模一样！！！
const ADMIN_TOKEN = 'admin_fixed_token_123456';

// 1. 获取用户列表
const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/admin/users', {
      headers: {
        // 重点：必须带上这个头，否则 node 后端会拒绝连接
        'Authorization': `Bearer ${ADMIN_TOKEN}`
      }
    });

    if (res.data.success) {
      users.value = res.data.data;
    } else {
      alert('获取失败: ' + res.data.msg);
    }
  } catch (error) {
    console.error(error);
    alert('连接管理员服务器失败，请检查 admin_server.js 是否启动');
  }
};

// 2. 禁用用户
const deleteUser = async (id) => {
  if (!confirm('确定要禁用该用户吗？')) return;

  try {
    const res = await axios.put(`/api/admin/users/${id}/delete`, {}, {
      headers: {
        'Authorization': `Bearer ${ADMIN_TOKEN}`
      }
    });

    if (res.data.success) {
      alert('操作成功');
      fetchUsers(); // 刷新
    } else {
      alert('操作失败: ' + res.data.msg);
    }
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.admin-users { padding: 40px; max-width: 1000px; margin: 0 auto; }
.refresh-btn { padding: 5px 15px; cursor: pointer; }
.del-btn { background: #ff4d4f; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; }
</style>