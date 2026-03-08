<template>
  <div class="dashboard-layout">
    <!-- 側邊欄（與 Dashboard 相同） -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-brand">
        <div class="brand-icon-sm">
          <svg viewBox="0 0 40 40" fill="none" width="32" height="32">
            <rect width="40" height="40" rx="10" fill="url(#sb-s-grad)"/>
            <path d="M12 28L20 12L28 28M15.5 22H24.5" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="sb-s-grad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
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

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
            <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/>
            <rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
          <span v-if="!sidebarCollapsed">儀表板</span>
        </router-link>
        <router-link to="/settings" class="nav-item active-nav">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20">
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          <span v-if="!sidebarCollapsed">設定</span>
        </router-link>
      </nav>

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
      <div class="page-header">
        <div>
          <h1 class="page-title">使用者設定</h1>
          <p class="page-subtitle">管理您的帳戶資訊與通知偏好設定</p>
        </div>
      </div>

      <!-- 載入中 -->
      <div v-if="loadingProfile" class="loading-state">
        <div class="spinner-lg"></div>
        <p>載入中...</p>
      </div>

      <div v-else>
        <!-- 帳戶資訊 -->
        <div class="settings-section">
          <div class="section-heading">
            <div class="section-icon section-icon-blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="18">
                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title-text">帳戶資訊</h2>
              <p class="section-desc">更新您的登入 Email 地址</p>
            </div>
          </div>

          <div class="form-card">
            <div class="form-field">
              <label class="form-label" for="email">電子郵件</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
                </svg>
                <input id="email" type="email" v-model="form.email"
                  class="input-field input-with-icon" placeholder="your@email.com"/>
              </div>
            </div>
          </div>
        </div>

        <!-- LINE Notify 設定 -->
        <div class="settings-section">
          <div class="section-heading">
            <div class="section-icon section-icon-green">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18">
                <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.105.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title-text">LINE 通知綁定</h2>
              <p class="section-desc">綁定 LINE 帳號以接收商品價格即時通知</p>
            </div>
          </div>

          <div class="form-card">
            <!-- LINE 狀態 (未綁定且未產生 OTP) -->
            <div v-if="!originalLineToken && !generatedOtp" class="line-bind-area">
              <p class="hint-text mb-3">您尚未綁定 LINE 通知。馬上產生限時驗證碼，與機器人對話輕鬆完成綁定！</p>
              <button type="button" class="btn-primary" @click="generateOtp" :disabled="generatingOtp" style="width: auto; padding: 10px 20px;">
                <span v-if="generatingOtp" class="spinner" style="margin-right: 8px;"></span>
                產生綁定驗證碼
              </button>
            </div>

            <!-- 顯示 OTP 驗證碼區 -->
            <div v-if="generatedOtp" class="otp-display-area">
              <h3 class="otp-title">您的專屬驗證碼</h3>
              <div class="otp-code">{{ generatedOtp }}</div>
              <p class="otp-timer">請在 {{ otpCountdown }} 內完成綁定</p>
              
              <div class="hint-box mt-4">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" style="flex-shrink:0; margin-top:2px;">
                  <circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>
                </svg>
                <div style="flex: 1;">
                  <span class="hint-text">快速綁定步驟 (手機與電腦皆適用)：</span><br>
                  
                  <div class="qr-code-container" style="margin-top: 12px; margin-bottom: 12px; text-align: center; background: white; padding: 10px; border-radius: 8px; display: inline-block;">
                    <qrcode-vue :value="deepLinkUrl" :size="150" level="M" />
                  </div>

                  <div style="margin-top: 8px;">
                    <a :href="deepLinkUrl" target="_blank" rel="noopener" class="btn-primary" style="display: inline-flex; width: auto; padding: 8px 16px; font-size: 13px; text-decoration: none; align-items: center; gap: 6px;">
                      <svg viewBox="0 0 24 24" fill="currentColor" width="16">
                        <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.105.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>
                      </svg>
                      手機版：一鍵開啟 LINE 綁定
                    </a>
                  </div>
                  <div style="margin-top: 8px; font-size: 12px; opacity: 0.8; line-height: 1.5;">
                    📱 <strong>如果您使用手機：</strong> 直接點擊上方按鈕跳轉至 LINE。<br>
                    💻 <strong>如果您使用電腦：</strong> 請拿起手機掃描左側條碼。<br>
                    系統會在對話框為您填妥 6 位數短碼，請直接送出即可。系統正在背景等待您完成綁定...
                  </div>
                </div>
              </div>
            </div>

            <!-- LINE 綁定狀態 (已綁定) -->
            <div class="line-status" v-if="originalLineToken">
              <div class="status-dot status-dot-green"></div>
              <span>LINE 已綁定 (可接收通知)</span>
              <button type="button" class="unlink-btn" @click="unlinkLine" :disabled="unlinking">
                {{ unlinking ? '處理中...' : '解除綁定' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 錯誤/成功訊息 -->
        <div v-if="feedbackMsg" :class="['feedback-banner', feedbackType === 'success' ? 'feedback-success' : 'feedback-error']">
          <svg v-if="feedbackType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ feedbackMsg }}
        </div>

        <!-- 儲存按鈕 -->
        <div class="save-area">
          <button class="btn-primary" @click="saveProfile" :disabled="saving" style="padding: 12px 32px;">
            <span v-if="saving" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>
            </svg>
            {{ saving ? '儲存中...' : '儲存設定' }}
          </button>
        </div>
      </div>
    </main>

    <!-- Toast -->
    <div class="toast-container">
      <div v-for="toast in toasts" :key="toast.id"
        :class="['toast', toast.type === 'success' ? 'toast-success' : 'toast-error']">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>
        </svg>
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import QrcodeVue from 'qrcode.vue'

// 請將此處預設替換為您的 LINE Bot Basic ID，例如 @123abcde
const LINE_BOT_ID = '@588tokwu' 

const router = useRouter()
const sidebarCollapsed = ref(false)
const loadingProfile = ref(true)
const saving = ref(false)
const generatingOtp = ref(false)
const unlinking = ref(false)
const feedbackMsg = ref('')
const feedbackType = ref('success')
const toasts = ref([])
const originalLineToken = ref('')
const generatedOtp = ref('')
const otpCountdown = ref('')
let timerInterval = null

const form = ref({ email: '' })

const showToast = (message, type = 'success') => {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => { toasts.value = toasts.value.filter(t => t.id !== id) }, 3500)
}

const deepLinkUrl = computed(() => {
  if (!generatedOtp.value) return '#'
  return `https://line.me/R/oaMessage/${LINE_BOT_ID}/?${generatedOtp.value}`
})

let pollingInterval = null

const startPolling = () => {
  if (pollingInterval) clearInterval(pollingInterval)
  pollingInterval = setInterval(async () => {
    try {
      const res = await api.get('/me')
      if (res.data.line_token) {
        // 後端已經把綁定結果寫入資料庫了
        clearInterval(pollingInterval)
        if (timerInterval) clearInterval(timerInterval)
        originalLineToken.value = res.data.line_token
        generatedOtp.value = ''
        showToast('恭喜！LINE 已成功綁定', 'success')
      }
    } catch(err) {
      console.warn('Polling error', err)
    }
  }, 2500) // 每 2.5 秒輪詢一次
}

const stopPolling = () => {
  if (pollingInterval) clearInterval(pollingInterval)
}

const startCountdown = (expiresAtStr) => {
  if (timerInterval) clearInterval(timerInterval)
  startPolling() // 開始計時的同時啟動輪詢
  
  const expires = new Date(expiresAtStr + 'Z').getTime() // FastAPI returns UTC string usually
  
  timerInterval = setInterval(() => {
    const now = new Date().getTime()
    const distance = expires - now
    if (distance <= 0) {
      clearInterval(timerInterval)
      stopPolling()
      otpCountdown.value = '已過期'
      generatedOtp.value = ''
    } else {
      const m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
      const s = Math.floor((distance % (1000 * 60)) / 1000)
      otpCountdown.value = `${m}分 ${s}秒`
    }
  }, 1000)
}

const generateOtp = async () => {
  generatingOtp.value = true
  try {
    const res = await api.post('/me/line-otp')
    generatedOtp.value = res.data.otp
    startCountdown(res.data.expires_at)
    showToast('驗證碼產生成功！請至 LINE 輸入')
  } catch (error) {
    showToast('產生驗證碼失敗', 'error')
  } finally {
    generatingOtp.value = false
  }
}

const unlinkLine = async () => {
  unlinking.value = true
  try {
    // 傳送空字串或 null 將會解除綁定
    await api.put('/me/profile', { line_token: '' })
    originalLineToken.value = ''
    form.value.line_token = ''
    showToast('已解除綁定')
  } catch(error) {
    showToast('解除綁定失敗', 'error')
  } finally {
    unlinking.value = false
  }
}

const fetchProfile = async () => {
  loadingProfile.value = true
  try {
    const res = await api.get('/me')
    form.value.email = res.data.email || ''
    originalLineToken.value = res.data.line_token || ''
    
    // 如果存在尚未過期的 OTP，自動恢復顯示
    if (res.data.line_otp && res.data.line_otp_expires_at) {
       const expires = new Date(res.data.line_otp_expires_at + 'Z').getTime()
       if (expires > new Date().getTime()) {
           generatedOtp.value = res.data.line_otp
           startCountdown(res.data.line_otp_expires_at)
       }
    }
  } catch (error) {
    if (error.response?.status === 401) logout()
    else showToast('無法載入個人資料', 'error')
  } finally {
    loadingProfile.value = false
  }
}

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
  stopPolling()
})

const saveProfile = async () => {
  saving.value = true
  feedbackMsg.value = ''
  try {
    const payload = {}
    if (form.value.email) payload.email = form.value.email

    await api.put('/me/profile', payload)
    showToast('設定已成功儲存')
  } catch (error) {
    showToast(error.response?.data?.detail || '儲存失敗，請稍後再試', 'error')
  } finally {
    saving.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(fetchProfile)
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* 側邊欄 */
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
  background: none; border: none; cursor: pointer;
  color: #94A3B8; padding: 4px;
  display: flex; border-radius: 6px;
  transition: all 200ms ease; flex-shrink: 0;
}
.collapse-btn:hover { color: #E2E8F0; background: rgba(255,255,255,0.05); }
.sidebar-nav {
  flex: 1; padding: 12px 10px;
  display: flex; flex-direction: column; gap: 4px;
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 10px;
  color: #94A3B8; text-decoration: none;
  font-size: 14px; font-weight: 500;
  cursor: pointer; background: none; border: none;
  width: 100%; text-align: left;
  transition: all 200ms ease; white-space: nowrap;
}
.nav-item:hover { color: #E2E8F0; background: rgba(255,255,255,0.06); }
.nav-item.active-nav,
.nav-item.router-link-active {
  color: #818CF8;
  background: rgba(99, 102, 241, 0.12);
}
.sidebar-footer { padding: 10px; border-top: 1px solid rgba(255,255,255,0.06); }
.logout-btn { color: #94A3B8; }
.logout-btn:hover { color: #F87171; background: rgba(239,68,68,0.08); }

/* 主內容 */
.main-content {
  flex: 1; padding: 32px;
  overflow-y: auto; max-width: 760px;
}

.page-header { margin-bottom: 28px; }
.page-title {
  font-family: 'Fira Code', monospace;
  font-size: 26px; font-weight: 700;
  color: #E2E8F0; margin: 0 0 4px 0;
}
.page-subtitle { font-size: 14px; color: #94A3B8; margin: 0; }

/* 設定區塊 */
.settings-section { margin-bottom: 24px; }
.section-heading {
  display: flex; align-items: flex-start;
  gap: 14px; margin-bottom: 14px;
}
.section-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 2px;
}
.section-icon-blue { background: rgba(99,102,241,0.15); color: #818CF8; }
.section-icon-green { background: rgba(16,185,129,0.15); color: #34D399; }
.section-title-text {
  font-family: 'Fira Code', monospace;
  font-size: 15px; font-weight: 600;
  color: #E2E8F0; margin: 0 0 2px 0;
}
.section-desc { font-size: 13px; color: #94A3B8; margin: 0; }

.form-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 20px;
  display: flex; flex-direction: column; gap: 16px;
}
.form-field { display: flex; flex-direction: column; }

/* Input */
.input-wrapper { position: relative; }
.input-icon {
  position: absolute; left: 14px; top: 50%;
  transform: translateY(-50%);
  width: 16px; height: 16px;
  color: #94A3B8; pointer-events: none;
}
.input-with-icon { padding-left: 42px !important; }

/* 提示框 */
.hint-box {
  display: flex; gap: 8px; align-items: flex-start;
  background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: 10px; padding: 10px 12px;
  margin-top: 10px; color: #94A3B8; font-size: 12px;
  line-height: 1.6;
}
.hint-text { color: #94A3B8; }
.hint-link {
  color: #818CF8; font-weight: 600;
  text-decoration: none; display: inline-flex;
  align-items: center; gap: 3px; margin-left: 4px;
  transition: color 200ms ease;
}
.hint-link:hover { color: #6366F1; }

/* LINE 狀態 */
.line-status {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: #94A3B8;
}
.status-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
}
.status-dot-green { background: #34D399; box-shadow: 0 0 6px rgba(52,211,153,0.5); }
.unlink-btn {
  margin-left: auto; background: none; border: none;
  color: #F87171; font-size: 12px; cursor: pointer;
  text-decoration: underline; padding: 0;
  transition: color 200ms ease;
}
.unlink-btn:hover { color: #EF4444; }

/* 回饋訊息 */
.feedback-banner {
  display: flex; align-items: center; gap: 8px;
  border-radius: 10px; padding: 12px 14px;
  font-size: 13px; margin-bottom: 16px;
}
.feedback-success {
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.3);
  color: #34D399;
}
.feedback-error {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #F87171;
}

/* 儲存按鈕區 */
.save-area { display: flex; justify-content: flex-end; }

/* 載入 */
.loading-state {
  display: flex; flex-direction: column;
  align-items: center; gap: 12px;
  padding: 60px; color: #94A3B8; font-size: 14px;
}
.spinner-lg {
  width: 32px; height: 32px;
  border: 3px solid rgba(99,102,241,0.2);
  border-top-color: #6366F1;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
}

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .main-content { padding: 20px 16px; }
  .sidebar { width: 64px; }
  .brand-text, .nav-item span { display: none; }
}

.mb-3 { margin-bottom: 12px; }
.mt-4 { margin-top: 16px; }

.line-bind-area {
  display: flex; flex-direction: column; align-items: flex-start;
}

.otp-display-area {
  background: rgba(99,102,241,0.06);
  border: 1px dashed rgba(99,102,241,0.3);
  border-radius: 12px; padding: 20px;
  text-align: center;
}

.otp-title {
  color: #94A3B8; font-size: 14px; margin: 0 0 12px 0; font-weight: normal;
}

.otp-code {
  font-family: 'Fira Code', monospace;
  font-size: 36px; font-weight: 700; color: #E2E8F0;
  letter-spacing: 4px; margin-bottom: 8px;
  background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px;
  display: inline-block;
}

.otp-timer {
  color: #F87171; font-size: 13px; margin: 0; font-family: monospace;
}
</style>
