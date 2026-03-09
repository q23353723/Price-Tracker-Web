<template>
  <div class="dashboard-layout">
    <!-- 側邊欄 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- 品牌 -->
      <div class="sidebar-brand">
        <div class="brand-icon-sm">
          <svg viewBox="0 0 40 40" fill="none" width="32" height="32">
            <rect width="40" height="40" rx="10" fill="url(#sb-grad)"/>
            <path d="M12 28L20 12L28 28M15.5 22H24.5" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="sb-grad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
                <stop stop-color="#6366F1"/><stop offset="1" stop-color="#818CF8"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span v-if="!sidebarCollapsed" class="brand-text">PriceTracker</span>
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
            <path v-if="!sidebarCollapsed" d="M15 18l-6-6 6-6"/>
            <path v-else d="M9 18l6-6-6-6"/>
          </svg>
        </button>
      </div>

      <!-- 導覽項目 -->
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item active-nav">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
            <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/>
            <rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
          <span v-if="!sidebarCollapsed">儀表板</span>
        </router-link>

        <router-link to="/settings" class="nav-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          <span v-if="!sidebarCollapsed">設定</span>
        </router-link>
      </nav>

      <!-- 底部登出 -->
      <div class="sidebar-footer">
        <button class="nav-item logout-btn" @click="logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          <span v-if="!sidebarCollapsed">登出</span>
        </button>
      </div>
    </aside>

    <!-- 主要內容 -->
    <main class="main-content">
      <!-- 頂部標題列 -->
      <div class="page-header">
        <div>
          <h1 class="page-title">追蹤中的商品</h1>
          <p class="page-subtitle">管理您訂閱的商品及目標價格通知</p>
        </div>
      </div>

      <!-- 統計卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon stat-icon-blue">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
          </div>
          <div>
            <div class="stat-value">{{ subscriptions.length }}</div>
            <div class="stat-label">追蹤中商品</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon stat-icon-green">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
            </svg>
          </div>
          <div>
            <div class="stat-value">{{ belowTargetCount }}</div>
            <div class="stat-label">已低於目標</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon stat-icon-indigo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
              <path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>
            </svg>
          </div>
          <div>
            <div class="stat-value">{{ activeCount }}</div>
            <div class="stat-label">啟用中</div>
          </div>
        </div>
      </div>

      <!-- 新增訂閱表單 -->
      <div class="section-card">
        <div class="section-header">
          <h2 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="18">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
            </svg>
            追蹤新商品
          </h2>
        </div>

        <form @submit.prevent="addSubscription" class="track-form">
          <div class="track-form-fields">
            <div class="form-group flex-2">
              <label class="form-label" for="url">商品 URL</label>
              <input type="url" id="url" v-model="newSub.product_url" required
                class="input-field" placeholder="https://www.pchome.com.tw/prod/..."/>
            </div>
            <div class="form-group">
              <label class="form-label" for="price">目標價格 (NT$)</label>
              <input type="number" step="0.01" id="price" v-model="newSub.target_price" required
                class="input-field" placeholder="9999"/>
            </div>
            <div class="form-group">
              <label class="form-label" for="method">通知方式</label>
              <select id="method" v-model="newSub.notify_method" class="input-field">
                <option value="EMAIL">Email</option>
                <option value="LINE">LINE</option>
                <option value="BOTH">兩者</option>
              </select>
            </div>
          </div>
          <button type="submit" class="btn-cta" :disabled="loading" style="padding: 10px 24px;">
            <span v-if="loading" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
              <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
            </svg>
            {{ loading ? '新增中...' : '開始追蹤' }}
          </button>
        </form>
      </div>

      <!-- 訂閱清單 -->
      <div class="subscriptions-section">
        <div class="section-header" style="margin-bottom: 12px;">
          <h2 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="18">
              <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
            </svg>
            訂閱列表
          </h2>
        </div>

        <!-- 空狀態 -->
        <div v-if="subscriptions.length === 0 && !loadingList" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
          </div>
          <p class="empty-title">尚未追蹤任何商品</p>
          <p class="empty-subtitle">在上方輸入商品連結，開始追蹤價格變動</p>
        </div>

        <!-- 載入中 -->
        <div v-else-if="loadingList" class="loading-state">
          <div class="spinner-lg"></div>
          <p>載入中...</p>
        </div>

        <!-- 訂閱卡片列表 -->
        <div v-else class="cards-list">
          <ProductCard
            v-for="sub in subscriptions"
            :key="sub.id"
            :subscription="sub"
            @delete="deleteSubscription"
            @edit="openEditModal"
          />
        </div>
      </div>
    </main>

    <!-- 編輯 Modal -->
    <EditSubscriptionModal
      v-if="editingSubscription"
      :subscription="editingSubscription"
      @close="editingSubscription = null"
      @saved="handleSaved"
    />

    <!-- Toast 通知 -->
    <div class="toast-container">
      <div v-for="toast in toasts" :key="toast.id"
        :class="['toast', toast.type === 'success' ? 'toast-success' : 'toast-error']">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ toast.message }}
      </div>
    </div>

    <!-- 自訂確認 Modal -->
    <div v-if="confirmModal.show" class="modal-backdrop" @click.self="confirmModal.show = false">
      <div class="modal-content">
        <h3 class="modal-title">確認刪除</h3>
        <p class="modal-body">確定要停止追蹤「{{ confirmModal.name }}」嗎？此操作無法復原。</p>
        <div class="modal-actions">
          <button class="btn-ghost" @click="confirmModal.show = false">取消</button>
          <button class="btn-danger" @click="confirmDelete" style="padding: 10px 20px;">確認刪除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import ProductCard from '../components/ProductCard.vue'
import EditSubscriptionModal from '../components/EditSubscriptionModal.vue'

const router = useRouter()
const subscriptions = ref([])
const loading = ref(false)
const loadingList = ref(true)
const sidebarCollapsed = ref(false)
const editingSubscription = ref(null)
const toasts = ref([])
const newSub = ref({ product_url: '', target_price: '', notify_method: 'EMAIL' })
const confirmModal = ref({ show: false, id: null, name: '' })

// 統計
const belowTargetCount = computed(() =>
  subscriptions.value.filter(s =>
    s.product.current_price !== null &&
    s.product.current_price <= s.target_price
  ).length
)
const activeCount = computed(() =>
  subscriptions.value.filter(s => s.is_active).length
)

// 顯示 Toast 通知
const showToast = (message, type = 'success') => {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3500)
}

// 取得訂閱列表
const fetchSubscriptions = async () => {
  loadingList.value = true
  try {
    const response = await api.get('/subscriptions/')
    subscriptions.value = response.data
  } catch (error) {
    if (error.response?.status === 401) logout()
    else showToast('無法載入訂閱列表', 'error')
  } finally {
    loadingList.value = false
  }
}

// 新增訂閱
const addSubscription = async () => {
  loading.value = true
  try {
    const payload = {
      product_url: newSub.value.product_url,
      target_price: parseFloat(newSub.value.target_price),
      notify_method: newSub.value.notify_method
    }
    await api.post('/subscriptions/', payload)
    newSub.value = { product_url: '', target_price: '', notify_method: 'EMAIL' }
    
    // 先抓取一次 (這時可能還沒爬完價格，但會先出現 loading / 未知價格的卡片)
    await fetchSubscriptions()
    showToast('商品已加入追蹤，正在背景抓取最新價格...')
    
    // 實作簡單輪詢機制：每 3 秒重新檢查一次，最多檢查 5 次 (約 15 秒)
    // 讓畫面能「自動」刷新出爬好的價格與圖片
    let attempts = 0
    const checkInterval = setInterval(async () => {
      attempts++
      await fetchSubscriptions()
      // 如果你願意，也可以在前端比對是否有資料已經更新。這邊簡單每 3 秒強刷一次即可。
      if (attempts >= 5) {
        clearInterval(checkInterval)
      }
    }, 3000)

  } catch (error) {
    showToast(error.response?.data?.detail || '新增失敗', 'error')
  } finally {
    loading.value = false
  }
}

// 開啟刪除確認
const deleteSubscription = (id) => {
  const sub = subscriptions.value.find(s => s.id === id)
  confirmModal.value = { show: true, id, name: sub?.product?.name || '此商品' }
}

// 確認刪除
const confirmDelete = async () => {
  const id = confirmModal.value.id
  confirmModal.value.show = false
  try {
    await api.delete(`/subscriptions/${id}`)
    await fetchSubscriptions()
    showToast('已停止追蹤')
  } catch (error) {
    showToast('刪除失敗', 'error')
  }
}

// 開啟編輯 Modal
const openEditModal = (sub) => {
  editingSubscription.value = sub
}

// 儲存編輯
const handleSaved = async () => {
  editingSubscription.value = null
  await fetchSubscriptions()
  showToast('訂閱設定已更新')
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(fetchSubscriptions)
</script>

<style scoped>
/* ===== 整體佈局 ===== */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* ===== 側邊欄 ===== */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.04);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  transition: width 300ms ease;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}
.sidebar.collapsed { width: 64px; }

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
}
.brand-text {
  font-family: 'Fira Code', monospace;
  font-size: 15px;
  font-weight: 700;
  color: #E2E8F0;
  white-space: nowrap;
  flex: 1;
}
.collapse-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #94A3B8;
  padding: 4px;
  display: flex;
  border-radius: 6px;
  transition: all 200ms ease;
  flex-shrink: 0;
}
.collapse-btn:hover { color: #E2E8F0; background: rgba(255,255,255,0.05); }

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  color: #94A3B8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  transition: all 200ms ease;
  white-space: nowrap;
}
.nav-item:hover { color: #E2E8F0; background: rgba(255, 255, 255, 0.06); }
.nav-item.active-nav,
.nav-item.router-link-active {
  color: #818CF8;
  background: rgba(99, 102, 241, 0.12);
}

.sidebar-footer {
  padding: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.logout-btn { color: #94A3B8; }
.logout-btn:hover { color: #F87171; background: rgba(239, 68, 68, 0.08); }

/* ===== 主要內容 ===== */
.main-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  max-width: 1100px;
}

/* ===== 標題 ===== */
.page-header {
  margin-bottom: 24px;
}
.page-title {
  font-family: 'Fira Code', monospace;
  font-size: 26px;
  font-weight: 700;
  color: #E2E8F0;
  margin: 0 0 4px 0;
}
.page-subtitle {
  font-size: 14px;
  color: #94A3B8;
  margin: 0;
}

/* ===== 統計卡片 ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 200ms ease;
}
.stat-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.12);
}
.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-icon-blue { background: rgba(99, 102, 241, 0.15); color: #818CF8; }
.stat-icon-green { background: rgba(16, 185, 129, 0.15); color: #34D399; }
.stat-icon-indigo { background: rgba(168, 85, 247, 0.15); color: #C084FC; }
.stat-value {
  font-family: 'Fira Code', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #E2E8F0;
  line-height: 1;
}
.stat-label {
  font-size: 12px;
  color: #94A3B8;
  margin-top: 4px;
}

/* ===== Section 卡片 ===== */
.section-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}
.section-header { margin-bottom: 16px; }
.section-title {
  font-family: 'Fira Code', monospace;
  font-size: 15px;
  font-weight: 600;
  color: #E2E8F0;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== 追蹤表單 ===== */
.track-form {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
}
.track-form-fields {
  display: flex;
  gap: 12px;
  flex: 1;
  flex-wrap: wrap;
}
.form-group {
  display: flex;
  flex-direction: column;
  min-width: 140px;
}
.flex-2 { flex: 2; }

/* ===== 空狀態 ===== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}
.empty-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px; height: 80px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.08);
  color: #6366F1;
  margin-bottom: 16px;
}
.empty-title {
  font-family: 'Fira Code', monospace;
  font-size: 16px;
  font-weight: 600;
  color: #E2E8F0;
  margin: 0 0 8px 0;
}
.empty-subtitle {
  font-size: 14px;
  color: #94A3B8;
  margin: 0;
}

/* ===== 載入狀態 ===== */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px;
  color: #94A3B8;
  font-size: 14px;
}
.spinner-lg {
  width: 32px; height: 32px;
  border: 3px solid rgba(99, 102, 241, 0.2);
  border-top-color: #6366F1;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
}

/* ===== 卡片列表 ===== */
.cards-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ===== 確認 Modal ===== */
.modal-title {
  font-family: 'Fira Code', monospace;
  font-size: 18px;
  font-weight: 700;
  color: #E2E8F0;
  margin: 0 0 10px 0;
}
.modal-body {
  font-size: 14px;
  color: #94A3B8;
  margin: 0 0 24px 0;
  line-height: 1.6;
}
.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* ===== Spinner ===== */
.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
  flex-shrink: 0;
}

.subscriptions-section { }

@keyframes spin { to { transform: rotate(360deg); } }

/* ===== 響應式 ===== */
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .main-content { padding: 20px 16px; }
  .track-form { flex-direction: column; }
  .sidebar { width: 64px; }
  .brand-text, .nav-item span { display: none; }
}
@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr; }
}
</style>
