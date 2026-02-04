<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { NCard, NDataTable, NButton, NIcon, NSpace, NTag, NPagination, NModal, NForm, NFormItem, NInput, NSelect, useMessage, useDialog } from 'naive-ui'
import type { DataTableColumns, FormInst, FormRules } from 'naive-ui'
import { AddOutline, TrashOutline, ShieldCheckmarkOutline } from '@vicons/ionicons5'
import { usersApi, type User } from '@/api'

const message = useMessage()
const dialog = useDialog()

const loading = ref(true)
const users = ref<User[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

// 新增用户相关
const showCreateModal = ref(false)
const createLoading = ref(false)
const createFormRef = ref<FormInst | null>(null)
const createForm = ref({
  username: '',
  email: '',
  password: '',
  role: 'user' as 'admin' | 'user'
})

const createRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度为 2-20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const roleOptions = [
  { label: '普通用户', value: 'user' },
  { label: '管理员', value: 'admin' }
]

const columns: DataTableColumns<User> = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '用户名', key: 'username' },
  { title: '邮箱', key: 'email' },
  {
    title: '角色',
    key: 'role',
    width: 100,
    render: (row) => h(NTag, { type: row.role === 'admin' ? 'warning' : 'default', size: 'small' }, {
      icon: () => row.role === 'admin' ? h(NIcon, null, { default: () => h(ShieldCheckmarkOutline) }) : null,
      default: () => row.role === 'admin' ? '管理员' : '用户'
    })
  },
  { title: '注册时间', key: 'created_at', width: 120, render: (row) => new Date(row.created_at).toLocaleDateString('zh-CN') },
  {
    title: '操作',
    key: 'actions',
    width: 220,
    render: (row) => h(NSpace, { wrap: false }, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true, onClick: () => handleToggleRole(row) }, { default: () => row.role === 'admin' ? '取消管理员' : '设为管理员' }),
        h(NButton, { size: 'small', quaternary: true, type: 'error', onClick: () => handleDelete(row) }, { icon: () => h(NIcon, null, { default: () => h(TrashOutline) }), default: () => '删除' })
      ]
    })
  }
]

onMounted(() => loadUsers())

async function loadUsers() {
  loading.value = true
  try {
    const res = await usersApi.getList({ page: page.value, page_size: pageSize.value })
    users.value = res.items
    total.value = res.total
  } catch (error) {
    message.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  createForm.value = {
    username: '',
    email: '',
    password: '',
    role: 'user'
  }
  showCreateModal.value = true
}

async function handleCreate() {
  try {
    await createFormRef.value?.validate()
    createLoading.value = true
    
    await usersApi.create({
      username: createForm.value.username,
      email: createForm.value.email,
      password: createForm.value.password,
      role: createForm.value.role
    })
    
    message.success('用户创建成功')
    showCreateModal.value = false
    loadUsers()
  } catch (error: any) {
    message.error(error?.detail || '创建失败')
  } finally {
    createLoading.value = false
  }
}

async function handleToggleRole(user: User) {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  const actionText = newRole === 'admin' ? '设为管理员' : '取消管理员权限'
  
  dialog.warning({
    title: '确认操作',
    content: `确定要将用户「${user.username}」${actionText}吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await usersApi.updateRole(user.id, newRole)
        message.success('操作成功')
        loadUsers()
      } catch (error) {
        message.error('操作失败')
      }
    }
  })
}

function handleDelete(user: User) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除用户「${user.username}」吗？此操作不可撤销。`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await usersApi.delete(user.id)
        message.success('删除成功')
        loadUsers()
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}

function handlePageChange(newPage: number) {
  page.value = newPage
  loadUsers()
}
</script>

<template>
  <NCard title="用户管理">
    <template #header-extra>
      <NButton type="primary" @click="openCreateModal">
        <template #icon>
          <NIcon><AddOutline /></NIcon>
        </template>
        新增用户
      </NButton>
    </template>

    <NDataTable :columns="columns" :data="users" :loading="loading" :bordered="false" />

    <div class="flex justify-end mt-4">
      <NPagination :page="page" :page-count="Math.ceil(total / pageSize)" @update:page="handlePageChange" />
    </div>
  </NCard>

  <!-- 新增用户弹窗 -->
  <NModal
    v-model:show="showCreateModal"
    preset="card"
    title="新增用户"
    style="width: 450px"
    :mask-closable="false"
  >
    <NForm ref="createFormRef" :model="createForm" :rules="createRules" label-placement="left" label-width="80">
      <NFormItem label="用户名" path="username">
        <NInput v-model:value="createForm.username" placeholder="请输入用户名" />
      </NFormItem>
      <NFormItem label="邮箱" path="email">
        <NInput v-model:value="createForm.email" placeholder="请输入邮箱" />
      </NFormItem>
      <NFormItem label="密码" path="password">
        <NInput v-model:value="createForm.password" type="password" placeholder="请输入密码" show-password-on="click" />
      </NFormItem>
      <NFormItem label="角色" path="role">
        <NSelect v-model:value="createForm.role" :options="roleOptions" placeholder="请选择角色" />
      </NFormItem>
    </NForm>

    <template #footer>
      <div class="flex justify-end gap-3">
        <NButton @click="showCreateModal = false">取消</NButton>
        <NButton type="primary" :loading="createLoading" @click="handleCreate">创建</NButton>
      </div>
    </template>
  </NModal>
</template>
