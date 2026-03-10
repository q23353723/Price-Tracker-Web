<template>
  <div class="auth-page">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <div class="auth-card animate-fade-in-up">
      <!-- 品牌 -->
      <div class="auth-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="40" height="40">
            <rect width="40" height="40" rx="12" fill="url(#brand-grad-r)"/>
            <path d="M20 14V8h-5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="8" y="14" width="24" height="18" rx="4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 23h4M32 23h4M25 21v3M15 21v3" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="brand-grad-r" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
                <stop stop-color="#6366F1"/><stop offset="1" stop-color="#818CF8"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div>
          <div class="brand-name">電商追蹤寶</div>
          <div class="brand-tagline">即時監控，智慧通知</div>
        </div>
      </div>

      <h1 class="auth-title">建立帳戶</h1>
      <p class="auth-subtitle">開始免費追蹤商品價格</p>

      <!-- 錯誤/成功訊息 -->
      <div v-if="errorMsg" class="error-banner">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>{{ errorMsg }}</span>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <!-- Email -->
        <div class="form-group">
          <label class="form-label" for="email">電子郵件</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
            <input id="email" type="email" autocomplete="email" required v-model="email"
              class="input-field input-with-icon" placeholder="you@example.com"/>
          </div>
        </div>

        <!-- 密碼 -->
        <div class="form-group">
          <label class="form-label" for="password">密碼</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input id="password" :type="showPassword ? 'text' : 'password'" autocomplete="new-password" required v-model="password"
              class="input-field input-with-icon input-with-toggle" placeholder="至少 8 個字元"/>
            <button type="button" class="toggle-password" @click="showPassword = !showPassword" tabindex="-1">
              <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
                <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- 確認密碼 -->
        <div class="form-group">
          <label class="form-label" for="confirm">確認密碼</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            <input id="confirm" type="password" autocomplete="new-password" required v-model="confirm"
              class="input-field input-with-icon" placeholder="再次輸入密碼"/>
          </div>
        </div>

        <button type="submit" class="btn-primary w-full mt-2" :disabled="loading" style="padding: 12px;">
          <span v-if="loading" class="spinner"></span>
          <span>{{ loading ? '註冊中...' : '建立帳戶' }}</span>
        </button>
      </form>

      <p class="auth-footer">
        已有帳戶？
        <router-link to="/login" class="auth-link">立即登入</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const email = ref('')
const password = ref('')
const confirm = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  errorMsg.value = ''
  if (password.value !== confirm.value) {
    errorMsg.value = '兩次輸入的密碼不一致'
    return
  }
  if (password.value.length < 8) {
    errorMsg.value = '密碼長度至少需要 8 個字元'
    return
  }

  loading.value = true
  try {
    await api.post('/register', { email: email.value, password: password.value })
    router.push('/login')
  } catch (error) {
    errorMsg.value = error.response?.data?.detail || '註冊失敗，請稍後再試。'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  animation: float 8s ease-in-out infinite;
  opacity: 0.4;
}
.orb-1 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(99,102,241,0.6), transparent);
  top: -100px; left: -100px;
  animation-delay: 0s;
}
.orb-2 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(16,185,129,0.4), transparent);
  bottom: -50px; right: -50px;
  animation-delay: -3s;
}
.orb-3 {
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(129,140,248,0.3), transparent);
  bottom: 30%; left: 20%;
  animation-delay: -5s;
}
.auth-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  position: relative;
  z-index: 1;
}
.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}
.brand-name {
  font-family: 'Fira Code', monospace;
  font-size: 18px;
  font-weight: 700;
  color: #E2E8F0;
  line-height: 1.2;
}
.brand-tagline {
  font-size: 12px;
  color: #94A3B8;
  margin-top: 2px;
}
.auth-title {
  font-family: 'Fira Code', monospace;
  font-size: 24px;
  font-weight: 700;
  color: #E2E8F0;
  margin: 0 0 6px 0;
  line-height: 1.3;
}
.auth-subtitle {
  font-size: 14px;
  color: #94A3B8;
  margin: 0 0 24px 0;
}
.error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  padding: 12px 14px;
  color: #F87171;
  font-size: 13px;
  margin-bottom: 20px;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-group { display: flex; flex-direction: column; }
.input-wrapper { position: relative; }
.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px; height: 16px;
  color: #94A3B8;
  pointer-events: none;
}
.input-with-icon { padding-left: 42px !important; }
.input-with-toggle { padding-right: 42px !important; }
.toggle-password {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94A3B8;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 200ms ease;
}
.toggle-password:hover { color: #E2E8F0; }
.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
.auth-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #94A3B8;
}
.auth-link {
  color: #818CF8;
  font-weight: 600;
  text-decoration: none;
  transition: color 200ms ease;
}
.auth-link:hover { color: #6366F1; }
.w-full { width: 100%; }
</style>
