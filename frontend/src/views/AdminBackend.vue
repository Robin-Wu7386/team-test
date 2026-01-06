<template>
  <div class="admin-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="admin-logo">🌿 中医药智能平台 管理后台</span>
      </div>
      <nav class="sidebar-menu">
        <div class="menu-item" :class="{ active: activeMenu === 'user' }" @click="switchMenu('user')">
          <span class="menu-icon">👥</span>
          <span class="menu-text">用户管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'herb' }" @click="switchMenu('herb')">
          <span class="menu-icon">🌿</span>
          <span class="menu-text">药材管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'fangji' }" @click="switchMenu('fangji')">
          <span class="menu-icon">📜</span>
          <span class="menu-text">药方管理</span>
        </div>
        <div class="menu-item" :class="{ active: activeMenu === 'source' }" @click="switchMenu('source')">
          <span class="menu-icon">📚</span>
          <span class="menu-text">来源管理</span>
        </div>
      </nav>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </aside>
    <!-- 主内容区 -->
    <main class="main-content">
      <header class="content-header">
        <h1 class="page-title">
          {{
            activeMenu === 'user' ? '用户管理' :
            activeMenu === 'herb' ? '药材管理' :
            activeMenu === 'fangji' ? '药方管理' :
            '来源管理'
          }}
        </h1>
      </header>
      <!-- 1. 用户管理 -->
      <div v-show="activeMenu === 'user'" class="content-module">
        <div class="module-header">
          <h2>用户列表</h2>
        </div>
        <div class="search-bar">
          <input
            v-model="userSearch"
            type="text"
            placeholder="搜索用户名/手机号"
            class="search-input"
            @keyup.enter="resetUserPageAndFetch"
          >
          <button class="search-btn" @click="resetUserPageAndFetch">搜索</button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>用户名</th>
              <th>手机号</th>
              <th>邮箱</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in userList" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.phonenumber }}</td>
              <td>{{ user.email || '无邮箱' }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
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
              <td colspan="6" class="empty-text">暂无用户数据</td>
            </tr>
            <tr v-if="userLoading">
              <td colspan="6" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
        <!-- 分页组件 -->
        <div class="pagination-container" v-if="userTotal > 0">
          <el-pagination
            v-model:current-page="userPage"
            v-model:page-size="userPageSize"
            :total="userTotal"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleUserSizeChange"
            @current-change="handleUserPageChange"
          />
        </div>
      </div>
      <!-- 2. 药材管理 -->
      <div v-show="activeMenu === 'herb'" class="content-module">
        <div class="module-header">
          <h2>药材管理</h2>
          <button class="add-btn" @click="openHerbModal('add')">
            + 新增药材
          </button>
        </div>
        <div class="search-bar">
          <input
            v-model="herbSearch"
            type="text"
            placeholder="搜索药材名称或药材ID"
            class="search-input"
            @keyup.enter="getHerbList"
          >
          <button class="search-btn" @click="getHerbList">搜索</button>
        </div>
        <!-- 药材表格 -->
        <table class="data-table">
          <thead>
            <tr>
              <th width="80">ID</th>
              <th width="120">药材ID</th>
              <th>药材名称</th>
              <th>来源列表</th>
              <th width="200">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="herb in herbList" :key="herb.id">
              <td>{{ herb.id }}</td>
              <td>{{ herb.herb_id }}</td>
              <td>{{ herb.name }}</td>
              <td>{{ herb.source_list || '未注明' }}</td>
              <td class="operation">
                <button class="oper-btn view-btn" @click="openHerbDetail(herb.id)">
                  查看
                </button>
                <button class="oper-btn edit-btn" @click="openHerbModal('edit', herb)">
                  修改
                </button>
                <button class="oper-btn delete-btn" @click="deleteHerb(herb.id)">
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="herbList.length === 0 && !herbLoading">
              <td colspan="5" class="empty-text">暂无药材数据</td>
            </tr>
            <tr v-if="herbLoading">
              <td colspan="5" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
        <!-- 药材分页 -->
        <div class="pagination-container" v-if="herbTotal > 0">
          <el-pagination
            v-model:current-page="herbPage"
            v-model:page-size="herbPageSize"
            :total="herbTotal"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleHerbSizeChange"
            @current-change="handleHerbPageChange"
          />
        </div>
      </div>
      <!-- 3. 药方管理 -->
      <div v-show="activeMenu === 'fangji'" class="content-module">
        <div class="module-header">
          <h2>药方列表</h2>
          <button class="add-btn" @click="openFangjiModal('add')">+ 新增药方</button>
        </div>
        <div class="search-bar">
          <input
            v-model="fangjiSearch"
            type="text"
            placeholder="搜索药方名称"
            class="search-input"
            @keyup.enter="fetchFangjiList"
          >
          <button class="search-btn" @click="fetchFangjiList">搜索</button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>药方名称</th>
              <th>出处</th>
              <th>药方组成</th>
              <th>功能主治</th>
              <th>用法</th>
              <th>禁忌</th>
              <th width="150">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fangji in fangjiList" :key="fangji.id">
              <td>{{ fangji.id }}</td>
              <td>{{ fangji.name }}</td>
              <td>{{ fangji.excerpt || '未注明' }}</td>
              <td>{{ fangji.prescription || '未注明' }}</td>
              <td>{{ fangji.function || '未注明' }}</td>
              <td>{{ fangji.usage || '未注明' }}</td>
              <td>{{ fangji.caution || '无' }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openFangjiModal('edit', fangji)">编辑</button>
                <button class="oper-btn delete-btn" @click="handleFangjiDelete(fangji.id)">删除</button>
              </td>
            </tr>
            <tr v-if="fangjiList.length === 0 && !fangjiLoading">
              <td colspan="8" class="empty-text">暂无药方数据</td>
            </tr>
            <tr v-if="fangjiLoading">
              <td colspan="8" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination-container" v-if="fangjiTotal > 0">
          <el-pagination
            v-model:current-page="fangjiPage"
            v-model:page-size="fangjiPageSize"
            :total="fangjiTotal"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleFangjiSizeChange"
            @current-change="handleFangjiPageChange"
          />
        </div>
      </div>
      <!-- 4. 来源管理 -->
      <div v-show="activeMenu === 'source'" class="content-module">
        <div class="module-header">
          <h2>来源列表</h2>
          <button class="add-btn" @click="openSourceModal('add')">+ 新增来源</button>
        </div>
        <div class="search-bar">
          <input
            v-model="sourceSearch"
            type="text"
            placeholder="搜索来源名称"
            class="search-input"
            @keyup.enter="fetchSources"
          >
          <button class="search-btn" @click="fetchSources">搜索</button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>来源名称</th>
              <th width="150">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="source in sourceList" :key="source.id">
              <td>{{ source.id }}</td>
              <td>{{ source.name }}</td>
              <td class="operation">
                <button class="oper-btn edit-btn" @click="openSourceModal('edit', source)">编辑</button>
                <button class="oper-btn delete-btn" @click="handleSourceDelete(source.id)">删除</button>
              </td>
            </tr>
            <tr v-if="sourceList.length === 0 && !sourceLoading">
              <td colspan="3" class="empty-text">暂无来源数据</td>
            </tr>
            <tr v-if="sourceLoading">
              <td colspan="3" class="loading-text">加载中...</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination-container" v-if="sourceTotal > 0">
          <el-pagination
            v-model:current-page="sourcePage"
            v-model:page-size="sourcePageSize"
            :total="sourceTotal"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSourceSizeChange"
            @current-change="handleSourcePageChange"
          />
        </div>
      </div>
    </main>
    <!-- 药材详情弹窗 -->
    <el-dialog v-model="herbDetailVisible" title="药材详情" width="60%">
      <el-form :model="herbDetailForm" label-width="120px" disabled>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="ID">
              <el-input v-model="herbDetailForm.id" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="药材ID">
              <el-input v-model="herbDetailForm.herb_id" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="药材名称">
              <el-input v-model="herbDetailForm.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="来源列表">
              <el-input v-model="herbDetailForm.source_list" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="别名">
          <el-input v-model="herbDetailForm.alias" />
        </el-form-item>
        <el-form-item label="功能主治">
          <el-input
            v-model="herbDetailForm['功能主治']"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="原形态">
          <el-input
            v-model="herbDetailForm.original_form"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性味">
              <el-input v-model="herbDetailForm['性味']" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用法用量">
              <el-input v-model="herbDetailForm.usage_dosage" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="性味归经">
          <el-input v-model="herbDetailForm['性味归经']" />
        </el-form-item>
        <el-form-item label="归经">
          <el-input v-model="herbDetailForm['归经']" />
        </el-form-item>
        <el-form-item label="英文名">
          <el-input v-model="herbDetailForm['英文名']" />
        </el-form-item>
        <el-form-item label="化学成分">
          <el-input
            v-model="herbDetailForm['化学成分']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="药理作用">
          <el-input
            v-model="herbDetailForm['药理作用']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="临床应用">
          <el-input
            v-model="herbDetailForm['临床应用']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="毒性">
          <el-input v-model="herbDetailForm['毒性']" />
        </el-form-item>
        <el-form-item label="植物形态">
          <el-input
            v-model="herbDetailForm['植物形态']"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="动物形态">
          <el-input
            v-model="herbDetailForm['动物形态']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="药用部位">
          <el-input v-model="herbDetailForm['药用部位']" />
        </el-form-item>
        <el-form-item label="采收加工">
          <el-input
            v-model="herbDetailForm['采收加工']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="炮制">
          <el-input
            v-model="herbDetailForm['炮制']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="制剂">
          <el-input
            v-model="herbDetailForm['制剂']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="性状">
          <el-input
            v-model="herbDetailForm['性状']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="鉴别">
          <el-input
            v-model="herbDetailForm['鉴别']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="含量测定">
          <el-input
            v-model="herbDetailForm['含量测定']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="注意">
          <el-input
            v-model="herbDetailForm['注意']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="贮藏">
          <el-input v-model="herbDetailForm['贮藏']" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="herbDetailForm['备注']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="各家论述">
          <el-input
            v-model="herbDetailForm['各家论述']"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="相关药方">
          <el-input
            v-model="herbDetailForm['相关药方']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="复方">
          <el-input
            v-model="herbDetailForm['复方']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="拼音注音">
          <el-input v-model="herbDetailForm['拼音注音']" />
        </el-form-item>
        <el-form-item label="生境分布">
          <el-input
            v-model="herbDetailForm['生境分布']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="主要成分">
          <el-input
            v-model="herbDetailForm['主要成分']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="herbDetailForm['规格']" />
        </el-form-item>
        <el-form-item label="制法">
          <el-input
            v-model="herbDetailForm['制法']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="栽培">
          <el-input
            v-model="herbDetailForm['栽培']"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="herbDetailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 药材新增/编辑弹窗 -->
    <el-dialog v-model="herbModalVisible" :title="herbModalType === 'add' ? '新增药材' : '编辑药材'" width="700px">
      <el-form
        ref="herbFormRef"
        :model="herbForm"
        label-width="120px"
        :rules="herbRules"
      >
        <el-form-item label="药材ID" prop="herb_id">
          <el-input v-model="herbForm.herb_id" placeholder="请输入药材ID" />
        </el-form-item>
        <el-form-item label="药材名称" prop="name">
          <el-input v-model="herbForm.name" placeholder="请输入药材名称" />
        </el-form-item>
        <el-form-item label="来源列表" prop="source_list">
          <el-select
            v-model="herbForm.source_ids"
            multiple
            filterable
            placeholder="选择来源（可多选）"
            @change="handleSourceChange"
          >
            <el-option
              v-for="source in allSources"
              :key="source.id"
              :label="source.name"
              :value="source.id"
            />
          </el-select>
          <div class="source-tips">已选来源：{{ herbForm.source_list }}</div>
        </el-form-item>
        <el-form-item label="别名">
          <el-input v-model="herbForm.alias" placeholder="请输入别名，多个用逗号分隔" />
        </el-form-item>
        <el-form-item label="功能主治">
          <el-input v-model="herbForm['功能主治']" placeholder="请输入功能主治" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="原形态">
          <el-input v-model="herbForm.original_form" placeholder="请输入原形态" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="性味">
          <el-input v-model="herbForm['性味']" placeholder="请输入性味" />
        </el-form-item>
        <el-form-item label="用法用量">
          <el-input v-model="herbForm.usage_dosage" placeholder="请输入用法用量" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="性味归经">
          <el-input v-model="herbForm['性味归经']" placeholder="请输入性味归经" />
        </el-form-item>
        <el-form-item label="归经">
          <el-input v-model="herbForm['归经']" placeholder="请输入归经" />
        </el-form-item>
        <el-form-item label="英文名">
          <el-input v-model="herbForm['英文名']" placeholder="请输入英文名" />
        </el-form-item>
        <el-form-item label="化学成分">
          <el-input v-model="herbForm['化学成分']" placeholder="请输入化学成分" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="药理作用">
          <el-input v-model="herbForm['药理作用']" placeholder="请输入药理作用" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="临床应用">
          <el-input v-model="herbForm['临床应用']" placeholder="请输入临床应用" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="毒性">
          <el-input v-model="herbForm['毒性']" placeholder="请输入毒性" />
        </el-form-item>
        <el-form-item label="植物形态">
          <el-input v-model="herbForm['植物形态']" placeholder="请输入植物形态" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="动物形态">
          <el-input v-model="herbForm['动物形态']" placeholder="请输入动物形态" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="药用部位">
          <el-input v-model="herbForm['药用部位']" placeholder="请输入药用部位" />
        </el-form-item>
        <el-form-item label="采收加工">
          <el-input v-model="herbForm['采收加工']" placeholder="请输入采收加工" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="炮制">
          <el-input v-model="herbForm['炮制']" placeholder="请输入炮制" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="制剂">
          <el-input v-model="herbForm['制剂']" placeholder="请输入制剂" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="性状">
          <el-input v-model="herbForm['性状']" placeholder="请输入性状" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="鉴别">
          <el-input v-model="herbForm['鉴别']" placeholder="请输入鉴别" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="含量测定">
          <el-input v-model="herbForm['含量测定']" placeholder="请输入含量测定" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="注意">
          <el-input v-model="herbForm['注意']" placeholder="请输入注意事项" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="贮藏">
          <el-input v-model="herbForm['贮藏']" placeholder="请输入贮藏" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="herbForm['备注']" placeholder="请输入备注" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="各家论述">
          <el-input v-model="herbForm['各家论述']" placeholder="请输入各家论述" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="相关药方">
          <el-input v-model="herbForm['相关药方']" placeholder="请输入相关药方" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="复方">
          <el-input v-model="herbForm['复方']" placeholder="请输入复方" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="拼音注音">
          <el-input v-model="herbForm['拼音注音']" placeholder="请输入拼音注音" />
        </el-form-item>
        <el-form-item label="生境分布">
          <el-input v-model="herbForm['生境分布']" placeholder="请输入生境分布" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="主要成分">
          <el-input v-model="herbForm['主要成分']" placeholder="请输入主要成分" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="herbForm['规格']" placeholder="请输入规格" />
        </el-form-item>
        <el-form-item label="制法">
          <el-input v-model="herbForm['制法']" placeholder="请输入制法" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="栽培">
          <el-input v-model="herbForm['栽培']" placeholder="请输入栽培" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="herbModalVisible = false">取消</el-button>
          <el-button type="primary" @click="submitHerbForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 药方模态框 -->
    <el-dialog
      v-model="fangjiModalVisible"
      :title="fangjiModalType === 'add' ? '新增药方' : '编辑药方'"
      width="800px"
    >
      <el-form :model="fangjiForm" label-width="100px" class="modal-form" ref="fangjiFormRef">
        <el-form-item label="药方名称" required prop="name">
          <el-input v-model="fangjiForm.name" placeholder="如：槐枝八仙散"></el-input>
        </el-form-item>
        <el-form-item label="出处" prop="excerpt">
          <el-select
            v-model="fangjiForm.excerpt"
            filterable
            allow-create
            placeholder="选择或输入出处（如《御药院方》）"
            style="width: 100%"
          >
            <el-option
              v-for="source in allSources"
              :key="source.id"
              :label="source.name"
              :value="source.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="功能主治" prop="function">
          <el-input
            v-model="fangjiForm.function"
            placeholder="如：牙齿疼痛"
            type="textarea"
            :rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="药方组成" required prop="prescription">
          <div class="herb-selection-container">
            <div class="herb-selection-item" v-for="(herb, index) in fangjiForm.selectedHerbs" :key="herb.id">
              <div class="herb-info">
                <span class="herb-name">{{ herb.name }} ({{ herb.herb_id || '无ID' }})</span>
                <el-input
                  v-model="herb.dosage"
                  placeholder="用量（如：1两半、2钱半）"
                  class="dosage-input"
                  @input="updatePrescriptionText"
                  style="width: 150px"
                />
              </div>
              <el-button type="danger" size="small" @click="removeSelectedHerb(index)">删除</el-button>
            </div>
            <!-- 药材选择器，支持过滤 -->
            <div class="herb-selector">
              <el-select
                v-model="fangjiForm.selectedHerbId"
                filterable
                placeholder="输入药材名称或ID搜索"
                style="width: 100%"
                :filter-method="filterHerbs"
                @change="addSelectedHerb"
              >
                <el-option
                  v-for="herb in filteredHerbs"
                  :key="herb.id"
                  :label="`${herb.name} (${herb.herb_id || '无ID'})`"
                  :value="herb.id"
                >
                  <span style="float: left">{{ herb.name }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ herb.herb_id || '无ID' }}</span>
                </el-option>
              </el-select>
            </div>
          </div>
          <div class="form-hint">选择药材并输入用量，系统会自动生成药方组成文本</div>
          <el-input
            v-model="fangjiForm.prescription"
            placeholder="自动生成的药方组成（如：槐枝1两半、乳香2钱半）"
            type="textarea"
            :rows="3"
            class="mt-2"
            readonly
          ></el-input>
        </el-form-item>
        <el-form-item label="用法" prop="usage">
          <el-input
            v-model="fangjiForm.usage"
            placeholder="如：水煎服，每日1剂，分2次温服"
            type="textarea"
            :rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="禁忌" prop="caution">
          <el-input
            v-model="fangjiForm.caution"
            placeholder="如：忌甘甜之物"
            type="textarea"
            :rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="制备" prop="preparation">
          <el-input
            v-model="fangjiForm.preparation"
            placeholder="如：上除槐枝、乳香外，同为细末"
            type="textarea"
            :rows="2"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="fangjiModalVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="submitFangjiForm"
          :loading="fangjiSubmitting"
        >
          {{ fangjiModalType === 'add' ? '新增' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
    <!-- 来源模态框 -->
    <el-dialog
      v-model="sourceModalVisible"
      :title="sourceModalType === 'add' ? '新增来源' : '编辑来源'"
      width="500px"
    >
      <el-form :model="sourceForm" label-width="100px" class="modal-form" ref="sourceFormRef">
        <el-form-item label="来源名称" required prop="name">
          <el-input v-model="sourceForm.name" placeholder="如：《御药院方》《中华本草》"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="sourceModalVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="submitSourceForm"
          :loading="sourceSubmitting"
        >
          {{ sourceModalType === 'add' ? '新增' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElMessage,
  ElSelect,
  ElOption,
  ElPagination,
  ElMessageBox
} from 'element-plus'
import 'element-plus/dist/index.css'

const router = useRouter()

// 菜单状态：默认选中用户管理
const activeMenu = ref('user')

// 切换菜单时重置搜索和分页
const switchMenu = (menu) => {
  activeMenu.value = menu
  // 根据当前菜单调用对应的数据获取函数
  switch(menu) {
    case 'user':
      fetchUsers()
      break
    case 'herb':
      getHerbList()
      break
    case 'fangji':
      fetchFangjiList()
      break
    case 'source':
      fetchSources()
      break
  }
}

// ---------------------- 通用配置 ----------------------
const API_PREFIX = '/api/admin'
const ADMIN_TOKEN = 'admin_fixed_token_123456'
const HEADERS = {
  Authorization: `Bearer ${ADMIN_TOKEN}`
}

// 日期格式化函数
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取所有来源（用于选择）
const allSources = ref([])
const fetchAllSources = async () => {
  try {
    const res = await axios.get(`${API_PREFIX}/sources`, {
      headers: HEADERS,
      params: { page: 1, pageSize: 1000 }
    })
    if (res.data.success) {
      allSources.value = res.data.data || []
    }
  } catch (err) {
    console.error('获取来源列表失败：', err)
  }
}

// 获取所有药材（用于药方选择）
const allHerbs = ref([])
const fetchAllHerbs = async () => {
  try {
    const res = await axios.get(`${API_PREFIX}/herbs`, {
      headers: HEADERS,
      params: { page: 1, pageSize: 1000 }
    })
    if (res.data.success) {
      allHerbs.value = res.data.data || []
      // 初始化过滤列表
      filteredHerbs.value = allHerbs.value.slice(0, 20)
    }
  } catch (err) {
    console.error('获取药材列表失败：', err)
  }
}

// 添加药材过滤功能
const filteredHerbs = ref([])
const filterHerbs = (query) => {
  if (query) {
    filteredHerbs.value = allHerbs.value.filter(herb =>
      herb.name.toLowerCase().includes(query.toLowerCase()) ||
      (herb.herb_id && herb.herb_id.toLowerCase().includes(query.toLowerCase()))
    )
  } else {
    filteredHerbs.value = allHerbs.value.slice(0, 20)
  }
}

// ---------------------- 用户管理 ----------------------
const userList = ref([])
const userLoading = ref(false)
const userSearch = ref('')
const userPage = ref(1)
const userPageSize = ref(20)
const userTotal = ref(0)

const fetchUsers = async () => {
  userLoading.value = true
  try {
    const res = await axios.get(`${API_PREFIX}/users`, {
      params: {
        search: userSearch.value,
        page: userPage.value,
        pageSize: userPageSize.value
      },
      headers: HEADERS
    })
    if (res.data.success) {
      userList.value = res.data.data || []
      userTotal.value = res.data.total || 0
    } else {
      ElMessage.error('获取用户列表失败：' + res.data.msg)
      userList.value = []
      userTotal.value = 0
    }
  } catch (err) {
    console.error('用户列表接口请求失败：', err)
    ElMessage.error('获取用户列表失败：' + (err.response?.data?.msg || err.message))
    userList.value = []
    userTotal.value = 0
  } finally {
    userLoading.value = false
  }
}

const resetUserPageAndFetch = () => {
  userPage.value = 1
  fetchUsers()
}

const handleUserPageChange = (page) => {
  userPage.value = page
  fetchUsers()
}

const handleUserSizeChange = (size) => {
  userPageSize.value = size
  userPage.value = 1
  fetchUsers()
}

const handleUserDelete = async (userId) => {
  try {
    await ElMessageBox.confirm('确定删除该用户？删除后不可恢复！', '提示', { type: 'warning' })
    const res = await axios.put(`${API_PREFIX}/users/${userId}/delete`, {}, { headers: HEADERS })
    if (res.data.success) {
      ElMessage.success('用户删除成功')
      fetchUsers()
    } else {
      ElMessage.error('删除失败：' + res.data.msg)
    }
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败：' + (err.response?.data?.msg || err.message))
    }
  }
}

// ---------------------- 药材管理 ----------------------
const herbList = ref([])
const herbLoading = ref(false)
const herbSearch = ref('')
const herbPage = ref(1)
const herbPageSize = ref(20)
const herbTotal = ref(0)
const herbDetailVisible = ref(false)
const herbDetailForm = ref({
  id: '',
  herb_id: '',
  name: '',
  source_list: '',
  alias: '',
  function: '',
  original_form: '',
  taste: '',
  caution: '',
  habitat: '',
  usage_dosage: '',
  // Attributes中文字段
  '功能主治': '',
  '性味': '',
  '性味归经': '',
  '归经': '',
  '英文名': '',
  '化学成分': '',
  '药理作用': '',
  '临床应用': '',
  '毒性': '',
  '植物形态': '',
  '动物形态': '',
  '药用部位': '',
  '采收加工': '',
  '炮制': '',
  '制剂': '',
  '性状': '',
  '鉴别': '',
  '含量测定': '',
  '注意': '',
  '贮藏': '',
  '备注': '',
  '各家论述': '',
  '相关药方': '',
  '复方': '',
  '拼音注音': '',
  '生境分布': '',
  '主要成分': '',
  '规格': '',
  '制法': '',
  '栽培': '',
})

// 药材弹窗相关
const herbModalVisible = ref(false)
const herbModalType = ref('add')
const herbForm = ref({
  herb_id: '',
  name: '',
  source_ids: [],
  source_list: '',
  alias: '',
  function: '',
  original_form: '',
  taste: '',
  caution: '',
  habitat: '',
  usage_dosage: '',
  // Attributes中文字段
  '功能主治': '',
  '性味': '',
  '性味归经': '',
  '归经': '',
  '英文名': '',
  '化学成分': '',
  '药理作用': '',
  '临床应用': '',
  '毒性': '',
  '植物形态': '',
  '动物形态': '',
  '药用部位': '',
  '采收加工': '',
  '炮制': '',
  '制剂': '',
  '性状': '',
  '鉴别': '',
  '含量测定': '',
  '注意': '',
  '贮藏': '',
  '备注': '',
  '各家论述': '',
  '相关药方': '',
  '复方': '',
  '拼音注音': '',
  '生境分布': '',
  '主要成分': '',
  '规格': '',
  '制法': '',
  '栽培': '',
})

const herbRules = ref({
  herb_id: [{ required: true, message: '请输入药材ID', trigger: 'blur' }],
  name: [{ required: true, message: '请输入药材名称', trigger: 'blur' }],
})

// 获取药材列表
const getHerbList = async () => {
  herbLoading.value = true
  try {
    const res = await axios.get(`${API_PREFIX}/herbs`, {
      headers: HEADERS,
      params: {
        search: herbSearch.value,
        page: herbPage.value,
        pageSize: herbPageSize.value
      }
    })
    if (res.data.success) {
      herbList.value = res.data.data || []
      herbTotal.value = res.data.total || 0
    } else {
      ElMessage.error('获取药材列表失败：' + res.data.msg)
    }
  } catch (err) {
    console.error('获取药材列表失败：', err)
    ElMessage.error('获取药材列表失败：' + (err.response?.data?.msg || err.message))
  } finally {
    herbLoading.value = false
  }
}

// 打开药材详情
const openHerbDetail = async (id) => {
  try {
    const res = await axios.get(`${API_PREFIX}/herbs/${id}`, { headers: HEADERS })
    if (res.data.success) {
      herbDetailForm.value = res.data.data
      herbDetailVisible.value = true
    } else {
      ElMessage.error('获取药材详情失败：' + res.data.msg)
    }
  } catch (err) {
    console.error('获取药材详情失败：', err)
    ElMessage.error('获取药材详情失败：' + (err.response?.data?.msg || err.message))
  }
}

// 打开药材新增/编辑弹窗
// 打开药材新增/编辑弹窗
const openHerbModal = async (type, herb = {}) => {
  herbModalType.value = type
  herbModalVisible.value = true

  if (type === 'add') {
    // 新增时清空表单
    herbForm.value = {
      herb_id: '',
      name: '',
      source_ids: [],
      source_list: '',
      alias: '',
      function: '',
      original_form: '',
      taste: '',
      caution: '',
      habitat: '',
      usage_dosage: '',
      '功能主治': '',
      '性味': '',
      '性味归经': '',
      '归经': '',
      '英文名': '',
      '化学成分': '',
      '药理作用': '',
      '临床应用': '',
      '毒性': '',
      '植物形态': '',
      '动物形态': '',
      '药用部位': '',
      '采收加工': '',
      '炮制': '',
      '制剂': '',
      '性状': '',
      '鉴别': '',
      '含量测定': '',
      '注意': '',
      '贮藏': '',
      '备注': '',
      '各家论述': '',
      '相关药方': '',
      '复方': '',
      '拼音注音': '',
      '生境分布': '',
      '主要成分': '',
      '规格': '',
      '制法': '',
      '栽培': '',
    }
  } else {
    // 编辑时，先获取药材详情
    try {
      const res = await axios.get(`${API_PREFIX}/herbs/${herb.id}`, { headers: HEADERS })
      if (res.data.success) {
        const herbDetail = res.data.data

        // 处理来源选择
        const source_ids = []
        let source_names = []

        // 从source_list解析来源名称
        if (herbDetail.source_list) {
          source_names = herbDetail.source_list.split(',').map(s => s.trim())
          // 根据名称查找对应的id
          source_names.forEach(name => {
            const source = allSources.value.find(s => s.name === name)
            if (source) source_ids.push(source.id)
          })
        }

        herbForm.value = {
          id: herb.id,
          herb_id: herbDetail.herb_id || '',
          name: herbDetail.name || '',
          source_ids: source_ids,
          source_list: herbDetail.source_list || '',
          alias: herbDetail.alias || '',
          function: herbDetail.function || '',
          original_form: herbDetail.original_form || '',
          taste: herbDetail.taste || '',
          caution: herbDetail.caution || '',
          habitat: herbDetail.habitat || '',
          usage_dosage: herbDetail.usage_dosage || '',
          // Attributes中文字段
          '功能主治': herbDetail['功能主治'] || '',
          '性味': herbDetail['性味'] || '',
          '性味归经': herbDetail['性味归经'] || '',
          '归经': herbDetail['归经'] || '',
          '英文名': herbDetail['英文名'] || '',
          '化学成分': herbDetail['化学成分'] || '',
          '药理作用': herbDetail['药理作用'] || '',
          '临床应用': herbDetail['临床应用'] || '',
          '毒性': herbDetail['毒性'] || '',
          '植物形态': herbDetail['植物形态'] || '',
          '动物形态': herbDetail['动物形态'] || '',
          '药用部位': herbDetail['药用部位'] || '',
          '采收加工': herbDetail['采收加工'] || '',
          '炮制': herbDetail['炮制'] || '',
          '制剂': herbDetail['制剂'] || '',
          '性状': herbDetail['性状'] || '',
          '鉴别': herbDetail['鉴别'] || '',
          '含量测定': herbDetail['含量测定'] || '',
          '注意': herbDetail['注意'] || '',
          '贮藏': herbDetail['贮藏'] || '',
          '备注': herbDetail['备注'] || '',
          '各家论述': herbDetail['各家论述'] || '',
          '相关药方': herbDetail['相关药方'] || '',
          '复方': herbDetail['复方'] || '',
          '拼音注音': herbDetail['拼音注音'] || '',
          '生境分布': herbDetail['生境分布'] || '',
          '主要成分': herbDetail['主要成分'] || '',
          '规格': herbDetail['规格'] || '',
          '制法': herbDetail['制法'] || '',
          '栽培': herbDetail['栽培'] || '',
        }
      } else {
        ElMessage.error('获取药材详情失败：' + res.data.msg)
      }
    } catch (err) {
      console.error('获取药材详情失败：', err)
      ElMessage.error('获取药材详情失败：' + (err.response?.data?.msg || err.message))
    }
  }
}


// 来源选择变更
const handleSourceChange = () => {
  const selectedSources = allSources.value.filter(item => herbForm.value.source_ids.includes(item.id))
  herbForm.value.source_list = selectedSources.map(item => item.name).join(',')
}

// 提交药材表单
const submitHerbForm = async () => {
  try {
    // 准备数据
    const formData = {
      herb_id: herbForm.value.herb_id,
      name: herbForm.value.name,
      source_list: herbForm.value.source_list,
      alias: herbForm.value.alias,
      function: herbForm.value.function,
      original_form: herbForm.value.original_form,
      taste: herbForm.value.taste,
      caution: herbForm.value.caution,
      habitat: herbForm.value.habitat,
      usage_dosage: herbForm.value.usage_dosage,
      source_ids: herbForm.value.source_ids,
      '功能主治': herbForm.value['功能主治'],
      '性味': herbForm.value['性味'],
      '性味归经': herbForm.value['性味归经'],
      '归经': herbForm.value['归经'],
      '英文名': herbForm.value['英文名'],
      '化学成分': herbForm.value['化学成分'],
      '药理作用': herbForm.value['药理作用'],
      '临床应用': herbForm.value['临床应用'],
      '毒性': herbForm.value['毒性'],
      '植物形态': herbForm.value['植物形态'],
      '动物形态': herbForm.value['动物形态'],
      '药用部位': herbForm.value['药用部位'],
      '采收加工': herbForm.value['采收加工'],
      '炮制': herbForm.value['炮制'],
      '制剂': herbForm.value['制剂'],
      '性状': herbForm.value['性状'],
      '鉴别': herbForm.value['鉴别'],
      '含量测定': herbForm.value['含量测定'],
      '注意': herbForm.value['注意'],
      '贮藏': herbForm.value['贮藏'],
      '备注': herbForm.value['备注'],
      '各家论述': herbForm.value['各家论述'],
      '相关药方': herbForm.value['相关药方'],
      '复方': herbForm.value['复方'],
      '拼音注音': herbForm.value['拼音注音'],
      '生境分布': herbForm.value['生境分布'],
      '主要成分': herbForm.value['主要成分'],
      '规格': herbForm.value['规格'],
      '制法': herbForm.value['制法'],
      '栽培': herbForm.value['栽培'],
    }

    if (herbModalType.value === 'add') {
      const res = await axios.post(`${API_PREFIX}/herbs`, formData, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('新增药材成功')
        herbModalVisible.value = false
        getHerbList()
      } else {
        ElMessage.error('新增失败：' + res.data.msg)
      }
    } else {
      const res = await axios.put(`${API_PREFIX}/herbs/${herbForm.value.id}`, formData, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('编辑药材成功')
        herbModalVisible.value = false
        getHerbList()
      } else {
        ElMessage.error('编辑失败：' + res.data.msg)
      }
    }
  } catch (err) {
    console.error('提交药材表单失败：', err)
    ElMessage.error('操作失败：' + (err.response?.data?.msg || err.message))
  }
}

// 删除药材
const deleteHerb = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该药材？删除后不可恢复！', '提示', { type: 'warning' })
    const res = await axios.delete(`${API_PREFIX}/herbs/${id}`, { headers: HEADERS })
    if (res.data.success) {
      ElMessage.success('药材删除成功')
      getHerbList()
    } else {
      ElMessage.error('删除失败：' + res.data.msg)
    }
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败：' + (err.response?.data?.msg || err.message))
    }
  }
}

// 药材分页相关
const handleHerbSizeChange = (size) => {
  herbPageSize.value = size
  herbPage.value = 1
  getHerbList()
}

const handleHerbPageChange = (page) => {
  herbPage.value = page
  getHerbList()
}

// ---------------------- 药方管理 ----------------------
const fangjiList = ref([])
const fangjiLoading = ref(false)
const fangjiSearch = ref('')
const fangjiPage = ref(1)
const fangjiPageSize = ref(20)
const fangjiTotal = ref(0)
const fangjiModalVisible = ref(false)
const fangjiModalType = ref('add')
const fangjiSubmitting = ref(false)

const fangjiForm = ref({
  id: '',
  name: '',
  excerpt: '',
  function: '',
  prescription: '',
  usage: '',
  caution: '',
  preparation: '',
  selectedHerbs: [],
  selectedHerbId: '',
})

// 获取药方列表
const fetchFangjiList = async () => {
  fangjiLoading.value = true
  try {
    const res = await axios.get(`${API_PREFIX}/fangji`, {
      headers: HEADERS,
      params: {
        search: fangjiSearch.value,
        page: fangjiPage.value,
        pageSize: fangjiPageSize.value
      }
    })
    if (res.data.success) {
      fangjiList.value = res.data.data || []
      fangjiTotal.value = res.data.total || 0
    } else {
      ElMessage.error('获取药方列表失败：' + res.data.msg)
    }
  } catch (err) {
    console.error('获取药方列表失败：', err)
    ElMessage.error('获取药方列表失败：' + (err.response?.data?.msg || err.message))
  } finally {
    fangjiLoading.value = false
  }
}

// 打开药方新增/编辑弹窗
const openFangjiModal = (type, fangji = {}) => {
  fangjiModalType.value = type
  fangjiModalVisible.value = true
  if (type === 'add') {
    fangjiForm.value = {
      id: '',
      name: '',
      excerpt: '',
      function: '',
      prescription: '',
      usage: '',
      caution: '',
      preparation: '',
      selectedHerbs: [],
      selectedHerbId: '',
    }
  } else {
    // 解析药方组成到选中药材
    const selectedHerbs = []
    if (fangji.prescription) {
      // 简单解析（实际可根据业务调整）
      const herbParts = fangji.prescription.split('、')
      herbParts.forEach(part => {
        const herbName = part.replace(/\d+[两钱分克]+/g, '').trim()
        const dosage = part.match(/\d+[两钱分克]+/g)?.[0] || ''
        const herb = allHerbs.value.find(h => h.name === herbName)
        if (herb) {
          selectedHerbs.push({
            ...herb,
            dosage
          })
        }
      })
    }
    fangjiForm.value = {
      ...fangji,
      selectedHerbs,
      selectedHerbId: '',
    }
  }
}

// 添加选中的药材到药方
const addSelectedHerb = () => {
  if (!fangjiForm.value.selectedHerbId) return
  const herb = allHerbs.value.find(h => h.id === fangjiForm.value.selectedHerbId)
  if (herb && !fangjiForm.value.selectedHerbs.some(h => h.id === herb.id)) {
    fangjiForm.value.selectedHerbs.push({
      ...herb,
      dosage: ''
    })
    updatePrescriptionText()
  }
  fangjiForm.value.selectedHerbId = ''
}

// 移除选中的药材
const removeSelectedHerb = (index) => {
  fangjiForm.value.selectedHerbs.splice(index, 1)
  updatePrescriptionText()
}

// 更新药方组成文本
const updatePrescriptionText = () => {
  const prescription = fangjiForm.value.selectedHerbs
    .filter(h => h.dosage)
    .map(h => `${h.name}${h.dosage}`)
    .join('、')
  fangjiForm.value.prescription = prescription
}

// 提交药方表单
const submitFangjiForm = async () => {
  fangjiSubmitting.value = true
  try {
    const herbIds = fangjiForm.value.selectedHerbs.map(herb => ({
      id: herb.id,
      dosage: herb.dosage
    }))

    const formData = {
      name: fangjiForm.value.name,
      excerpt: fangjiForm.value.excerpt,
      function: fangjiForm.value.function,
      prescription: fangjiForm.value.prescription,
      usage: fangjiForm.value.usage,
      caution: fangjiForm.value.caution,
      preparation: fangjiForm.value.preparation,
      herbIds: herbIds
    }

    if (fangjiModalType.value === 'add') {
      const res = await axios.post(`${API_PREFIX}/fangji`, formData, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('新增药方成功')
        fangjiModalVisible.value = false
        fetchFangjiList()
      } else {
        ElMessage.error('新增失败：' + res.data.msg)
      }
    } else {
      const res = await axios.put(`${API_PREFIX}/fangji/${fangjiForm.value.id}`, formData, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('编辑药方成功')
        fangjiModalVisible.value = false
        fetchFangjiList()
      } else {
        ElMessage.error('编辑失败：' + res.data.msg)
      }
    }
  } catch (err) {
    console.error('提交药方表单失败：', err)
    ElMessage.error('操作失败：' + (err.response?.data?.msg || err.message))
  } finally {
    fangjiSubmitting.value = false
  }
}

// 药方分页相关
const handleFangjiSizeChange = (size) => {
  fangjiPageSize.value = size
  fangjiPage.value = 1
  fetchFangjiList()
}

const handleFangjiPageChange = (page) => {
  fangjiPage.value = page
  fetchFangjiList()
}

// 删除药方
const handleFangjiDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该药方？删除后不可恢复！', '提示', { type: 'warning' })
    const res = await axios.delete(`${API_PREFIX}/fangji/${id}`, { headers: HEADERS })
    if (res.data.success) {
      ElMessage.success('药方删除成功')
      fetchFangjiList()
    } else {
      ElMessage.error('删除失败：' + res.data.msg)
    }
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败：' + (err.response?.data?.msg || err.message))
    }
  }
}

// ---------------------- 来源管理 ----------------------
const sourceList = ref([])
const sourceLoading = ref(false)
const sourceSearch = ref('')
const sourcePage = ref(1)
const sourcePageSize = ref(20)
const sourceTotal = ref(0)
const sourceModalVisible = ref(false)
const sourceModalType = ref('add')
const sourceSubmitting = ref(false)

const sourceForm = ref({
  id: '',
  name: '',
})

// 获取来源列表
const fetchSources = async () => {
  sourceLoading.value = true
  try {
    const res = await axios.get(`${API_PREFIX}/sources`, {
      headers: HEADERS,
      params: {
        search: sourceSearch.value,
        page: sourcePage.value,
        pageSize: sourcePageSize.value
      }
    })
    if (res.data.success) {
      sourceList.value = res.data.data || []
      sourceTotal.value = res.data.total || 0
    } else {
      ElMessage.error('获取来源列表失败：' + res.data.msg)
    }
  } catch (err) {
    console.error('获取来源列表失败：', err)
    ElMessage.error('获取来源列表失败：' + (err.response?.data?.msg || err.message))
  } finally {
    sourceLoading.value = false
  }
}

// 打开来源新增/编辑弹窗
const openSourceModal = (type, source = {}) => {
  sourceModalType.value = type
  sourceModalVisible.value = true
  if (type === 'add') {
    sourceForm.value = { id: '', name: '' }
  } else {
    sourceForm.value = { ...source }
  }
}

// 提交来源表单
const submitSourceForm = async () => {
  sourceSubmitting.value = true
  try {
    if (sourceModalType.value === 'add') {
      const res = await axios.post(`${API_PREFIX}/sources`, sourceForm.value, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('新增来源成功')
        sourceModalVisible.value = false
        fetchSources()
        fetchAllSources() // 刷新下拉列表
      } else {
        ElMessage.error('新增失败：' + res.data.msg)
      }
    } else {
      const res = await axios.put(`${API_PREFIX}/sources/${sourceForm.value.id}`, sourceForm.value, { headers: HEADERS })
      if (res.data.success) {
        ElMessage.success('编辑来源成功')
        sourceModalVisible.value = false
        fetchSources()
        fetchAllSources() // 刷新下拉列表
      } else {
        ElMessage.error('编辑失败：' + res.data.msg)
      }
    }
  } catch (err) {
    console.error('提交来源表单失败：', err)
    ElMessage.error('操作失败：' + (err.response?.data?.msg || err.message))
  } finally {
    sourceSubmitting.value = false
  }
}

// 来源分页相关
const handleSourceSizeChange = (size) => {
  sourcePageSize.value = size
  sourcePage.value = 1
  fetchSources()
}

const handleSourcePageChange = (page) => {
  sourcePage.value = page
  fetchSources()
}

// 删除来源
const handleSourceDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该来源？删除后不可恢复！', '提示', { type: 'warning' })
    const res = await axios.delete(`${API_PREFIX}/sources/${id}`, { headers: HEADERS })
    if (res.data.success) {
      ElMessage.success('来源删除成功')
      fetchSources()
      fetchAllSources() // 刷新下拉列表
    } else {
      ElMessage.error('删除失败：' + res.data.msg)
    }
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败：' + (err.response?.data?.msg || err.message))
    }
  }
}

// 退出登录
const handleLogout = () => {
  router.push('/login')
  ElMessage.success('退出登录成功')
}

// 页面挂载时初始化数据
onMounted(async () => {
  await fetchAllSources()
  await fetchAllHerbs()
  fetchUsers()
})
</script>

<style scoped>
.admin-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 侧边栏样式 - 优化颜色 */
.sidebar {
  width: 240px;
  background: linear-gradient(to bottom, #2c3e50, #34495e);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 24px 20px;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  background: rgba(0, 0, 0, 0.2);
}

.admin-logo {
  color: #1abc9c;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.sidebar-menu {
  flex: 1;
  padding: 20px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 14px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 4px 10px;
  border-radius: 8px;
}

.menu-item.active {
  background: linear-gradient(to right, #1abc9c, #16a085);
  box-shadow: 0 2px 8px rgba(26, 188, 156, 0.3);
  transform: translateX(4px);
}

.menu-item:hover:not(.active) {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.menu-icon {
  font-size: 20px;
  margin-right: 12px;
  width: 24px;
  text-align: center;
}

.menu-text {
  font-size: 15px;
  font-weight: 500;
}

.logout-btn {
  margin: 20px;
  padding: 10px;
  background: linear-gradient(to right, #e74c3c, #c0392b);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(231, 76, 60, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
}

/* 主内容区样式 */
.main-content {
  flex: 1;
  padding: 24px;
  background: #f8f9fa;
  overflow-y: auto;
}

.content-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  position: relative;
  padding-left: 16px;
}

.page-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 4px;
  background: linear-gradient(to bottom, #1abc9c, #3498db);
  border-radius: 2px;
}

/* 模块样式 */
.content-module {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f1f1;
}

.module-header h2 {
  font-size: 20px;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}

.add-btn {
  padding: 10px 20px;
  background: linear-gradient(to right, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(52, 152, 219, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
}

/* 搜索栏样式 */
.search-bar {
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e0e6ed;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  background: white;
}

.search-btn {
  padding: 12px 24px;
  background: linear-gradient(to right, #95a5a6, #7f8c8d);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 80px;
}

.search-btn:hover {
  background: linear-gradient(to right, #7f8c8d, #6c7a7d);
  transform: translateY(-1px);
}

/* 表格样式 */
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
  border-radius: 8px;
  overflow: hidden;
}

.data-table th,
.data-table td {
  padding: 16px;
  border: 1px solid #e9ecef;
  text-align: left;
}

.data-table th {
  background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #dee2e6;
}

.data-table tbody tr {
  transition: all 0.2s ease;
}

.data-table tbody tr:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
}

.empty-text,
.loading-text {
  text-align: center;
  color: #95a5a6;
  padding: 32px;
  font-style: italic;
}

.loading-text {
  color: #3498db;
}

/* 操作列样式 */
.operation {
  display: flex;
  gap: 8px;
}

.oper-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
  min-width: 60px;
}

.edit-btn {
  background: linear-gradient(to right, #f39c12, #e67e22);
  color: white;
}

.edit-btn:hover {
  background: linear-gradient(to right, #e67e22, #d35400);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(243, 156, 18, 0.3);
}

.delete-btn {
  background: linear-gradient(to right, #e74c3c, #c0392b);
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background: linear-gradient(to right, #c0392b, #a93226);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

.delete-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.view-btn {
  background: linear-gradient(to right, #1abc9c, #16a085);
  color: white;
}

.view-btn:hover {
  background: linear-gradient(to right, #16a085, #149174);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(26, 188, 156, 0.3);
}

/* 分页样式 */
.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

/* 弹窗相关样式 */
.modal-form {
  margin-top: 10px;
}

.herb-selection-container {
  margin-bottom: 10px;
}

.herb-selection-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid #e9ecef;
}

.herb-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.herb-name {
  font-weight: 500;
  color: #2c3e50;
}

.dosage-input {
  margin-left: 10px;
}

.form-hint {
  color: #95a5a6;
  font-size: 13px;
  margin-top: 8px;
}

.mt-2 {
  margin-top: 10px;
}

.source-tips {
  margin-top: 8px;
  font-size: 13px;
  color: #3498db;
  font-weight: 500;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .sidebar {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .admin-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
  }

  .main-content {
    padding: 16px;
  }

  .module-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .operation {
    flex-wrap: wrap;
  }
}
</style>