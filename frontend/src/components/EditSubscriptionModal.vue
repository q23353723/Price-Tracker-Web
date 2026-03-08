<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content animate-fade-in-up">
      <!-- 標題 -->
      <div class="modal-header">
        <h3 class="modal-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="18">
            <path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>
            <path d="m15 5 4 4"/>
          </svg>
          編輯訂閱設定
        </h3>
        <button class="close-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="18">
            <path d="M18 6 6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- 商品資訊預覽 -->
      <div class="product-preview">
        <div class="preview-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="20" opacity="0.6">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
        </div>
        <div class="preview-text">
          <div class="preview-name">{{ subscription.product.name }}</div>
          <div class="preview-url">{{ shortUrl }}</div>
        </div>
      </div>

      <!-- 目前值顯示 -->
      <div class="current-info">
        <div class="info-item">
          <span class="info-label">目前價格</span>
          <span class="info-value">
            {{ subscription.product.current_price ? 'NT$ ' + formatPrice(subscription.product.current_price) : '更新中...' }}
          </span>
        </div>
      </div>

      <!-- 表單 -->
      <form @submit.prevent="handleSave" class="edit-form">
        <!-- 目標價格 -->
        <div>
          <label class="form-label" for="edit-price">目標價格 (NT$)</label>
          <input
            id="edit-price"
            type="number"
            step="0.01"
            min="0"
            v-model="form.target_price"
            required
            class="input-field"
            placeholder="設定期望購買價格"
          />
          <p class="field-hint">當商品降至此價格以下時，系統將發送通知</p>
        </div>

        <!-- 通知方式 -->
        <div>
          <label class="form-label" for="edit-method">通知方式</label>
          <div class="method-options">
            <label v-for="opt in methodOptions" :key="opt.value" class="method-option" :class="{ selected: form.notify_method === opt.value }">
              <input type="radio" :value="opt.value" v-model="form.notify_method" class="radio-input"/>
              <span class="method-icon" v-html="opt.icon"></span>
              <span class="method-label">{{ opt.label }}</span>
            </label>
          </div>
        </div>

        <!-- 錯誤訊息 -->
        <div v-if="errorMsg" class="error-banner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ errorMsg }}
        </div>

        <!-- 按鈕 -->
        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="$emit('close')">取消</button>
          <button type="submit" class="btn-primary" :disabled="saving" style="padding: 10px 24px;">
            <span v-if="saving" class="spinner"></span>
            {{ saving ? '儲存中...' : '儲存變更' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api'

const props = defineProps({
  subscription: { type: Object, required: true }
})

const emit = defineEmits(['close', 'saved'])

const saving = ref(false)
const errorMsg = ref('')

const form = ref({
  target_price: props.subscription.target_price,
  notify_method: props.subscription.notify_method
})

const methodOptions = [
  {
    value: 'EMAIL',
    label: 'Email',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>`
  },
  {
    value: 'LINE',
    label: 'LINE',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor" width="16"><path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.105.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/></svg>`
  },
  {
    value: 'BOTH',
    label: '兩者都要',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>`
  }
]

const shortUrl = computed(() => {
  try {
    const u = new URL(props.subscription.product.url)
    return u.hostname + (u.pathname.length > 30 ? u.pathname.substring(0, 30) + '...' : u.pathname)
  } catch {
    return props.subscription.product.url.substring(0, 50)
  }
})

const formatPrice = (price) =>
  Number(price).toLocaleString('zh-TW', { minimumFractionDigits: 0, maximumFractionDigits: 0 })

const handleSave = async () => {
  saving.value = true
  errorMsg.value = ''
  try {
    await api.put(`/subscriptions/${props.subscription.id}`, {
      target_price: parseFloat(form.value.target_price),
      notify_method: form.value.notify_method
    })
    emit('saved')
  } catch (error) {
    errorMsg.value = error.response?.data?.detail || '儲存失敗，請稍後再試'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
/* ===== 標題 ===== */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.modal-title {
  font-family: 'Fira Code', monospace;
  font-size: 17px;
  font-weight: 700;
  color: #E2E8F0;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #94A3B8;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  transition: all 200ms ease;
}
.close-btn:hover { color: #E2E8F0; background: rgba(255,255,255,0.05); }

/* ===== 商品預覽 ===== */
.product-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 16px;
}
.preview-icon {
  color: #818CF8;
  flex-shrink: 0;
  display: flex;
}
.preview-name {
  font-size: 14px;
  font-weight: 600;
  color: #CBD5E1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.preview-url {
  font-size: 11px;
  color: #64748B;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.preview-text { min-width: 0; flex: 1; }

/* ===== 目前資訊 ===== */
.current-info {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}
.info-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.info-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748B;
}
.info-value {
  font-family: 'Fira Code', monospace;
  font-size: 16px;
  font-weight: 700;
  color: #E2E8F0;
}

/* ===== 表單 ===== */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-hint {
  font-size: 11px;
  color: #64748B;
  margin: 6px 0 0 0;
}

/* ===== 通知方式選項 ===== */
.method-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 6px;
}
.method-option {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #94A3B8;
  transition: all 200ms ease;
  user-select: none;
}
.method-option:hover { border-color: rgba(99,102,241,0.3); color: #E2E8F0; }
.method-option.selected {
  border-color: rgba(99,102,241,0.5);
  background: rgba(99,102,241,0.1);
  color: #818CF8;
}
.radio-input { display: none; }
.method-icon { display: flex; align-items: center; }

/* ===== 錯誤 ===== */
.error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  padding: 10px 14px;
  color: #F87171;
  font-size: 13px;
}

/* ===== 按鈕 ===== */
.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* ===== Spinner ===== */
.spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 700ms linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
