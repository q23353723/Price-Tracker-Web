<template>
  <div class="product-card glass-card-hover">
    <!-- 商品圖片 -->
    <div class="card-image">
      <img
        :src="subscription.product.image_url || ''"
        :alt="subscription.product.name"
        class="product-img"
        @error="(e) => e.target.style.display = 'none'"
      />
      <div class="img-fallback" :style="imgFallbackStyle">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="24" opacity="0.5">
          <rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
        </svg>
      </div>
    </div>

    <!-- 主要資訊 -->
    <div class="card-content">
      <div class="card-top">
        <div class="product-info">
          <a :href="subscription.product.url" target="_blank" rel="noopener" class="product-name">
            {{ subscription.product.name }}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="12" class="link-icon">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
          </a>
          <div class="product-meta">
            <span class="badge-gray">{{ notifyMethodLabel }}</span>
            <span :class="subscription.is_active ? 'badge-green' : 'badge-gray'" style="font-size: 11px;">
              {{ subscription.is_active ? '追蹤中' : '已停用' }}
            </span>
          </div>
        </div>

        <!-- 操作按鈕 -->
        <div class="card-actions">
          <button class="action-btn edit-btn" @click="$emit('edit', subscription)" title="編輯訂閱">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
              <path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>
              <path d="m15 5 4 4"/>
            </svg>
          </button>
          <button class="action-btn delete-btn" @click="$emit('delete', subscription.id)" title="停止追蹤">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16">
              <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 價格資訊 -->
      <div class="price-section">
        <div class="price-item">
          <div class="price-label">目標價格</div>
          <div class="price-target">NT$ {{ formatPrice(subscription.target_price) }}</div>
        </div>
        <div class="price-divider">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" opacity="0.4">
            <path d="M5 12h14"/>
          </svg>
        </div>
        <div class="price-item">
          <div class="price-label">目前價格</div>
          <div v-if="subscription.product.current_price" :class="['price-current', priceClass]">
            NT$ {{ formatPrice(subscription.product.current_price) }}
          </div>
          <div v-else class="price-loading">資料更新中...</div>
        </div>
        <div class="price-badge-area">
          <span v-if="subscription.product.current_price" :class="priceBadgeClass">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" width="10">
              <polyline v-if="isBelowTarget" points="18 15 12 9 6 15"/>
              <polyline v-else points="6 9 12 15 18 9"/>
            </svg>
            {{ priceDiffText }}
          </span>
        </div>
      </div>

      <!-- 最後更新時間 -->
      <div v-if="subscription.product.last_checked_at" class="last-checked">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
        </svg>
        更新於 {{ formatTime(subscription.product.last_checked_at) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  subscription: { type: Object, required: true }
})

defineEmits(['delete', 'edit'])

// 通知方式顯示文字
const notifyMethodLabel = computed(() => {
  const map = { EMAIL: 'Email', LINE: 'LINE', BOTH: 'Email + LINE' }
  return map[props.subscription.notify_method] || props.subscription.notify_method
})

// 價格格式化
const formatPrice = (price) => {
  return Number(price).toLocaleString('zh-TW', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

// 是否低於目標
const isBelowTarget = computed(() => {
  const cur = props.subscription.product.current_price
  const target = props.subscription.target_price
  return cur !== null && cur <= target
})

// 價格差異文字
const priceDiffText = computed(() => {
  const cur = props.subscription.product.current_price
  const target = props.subscription.target_price
  if (cur === null) return ''
  const diff = Math.abs(target - cur)
  const pct = Math.abs(((cur - target) / target) * 100).toFixed(1)
  if (cur <= target) return `-NT$${formatPrice(diff)} (${pct}%)`
  return `+NT$${formatPrice(diff)} (${pct}%)`
})

// 目前價格樣式
const priceClass = computed(() =>
  isBelowTarget.value ? 'price-below' : 'price-above'
)

// Badge 樣式
const priceBadgeClass = computed(() =>
  isBelowTarget.value ? 'badge-green' : 'badge-red'
)

// 圖片 Fallback 顏色（根據商品 id hash）
const imgFallbackStyle = computed(() => {
  const colors = ['#6366F1', '#818CF8', '#10B981', '#F59E0B', '#EC4899']
  const idx = props.subscription.id.charCodeAt(0) % colors.length
  return { background: `${colors[idx]}22` }
})

// 時間格式化
const formatTime = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diffMs = now - d
  const diffMins = Math.floor(diffMs / 60000)
  const diffHrs = Math.floor(diffMins / 60)
  if (diffMins < 1) return '剛剛'
  if (diffMins < 60) return `${diffMins} 分鐘前`
  if (diffHrs < 24) return `${diffHrs} 小時前`
  return d.toLocaleDateString('zh-TW')
}
</script>

<style scoped>
.product-card {
  display: flex;
  gap: 0;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: all 200ms ease;
  cursor: default;
}
.product-card:hover {
  border-color: rgba(99, 102, 241, 0.25);
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
}

/* ===== 商品圖 ===== */
.card-image {
  width: 100px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.03);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  inset: 0;
}
.img-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94A3B8;
  min-height: 90px;
}

/* ===== 主要內容 ===== */
.card-content {
  flex: 1;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.product-info { flex: 1; min-width: 0; }

.product-name {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: 'Fira Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: #E2E8F0;
  text-decoration: none;
  transition: color 200ms ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.product-name:hover { color: #818CF8; }
.link-icon { flex-shrink: 0; opacity: 0.5; }

.product-meta {
  display: flex;
  gap: 6px;
  margin-top: 6px;
  flex-wrap: wrap;
}

/* ===== 操作按鈕 ===== */
.card-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}
.action-btn {
  width: 32px; height: 32px;
  border-radius: 8px;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 200ms ease;
  background: transparent;
}
.edit-btn {
  color: #94A3B8;
  border-color: rgba(255,255,255,0.08);
}
.edit-btn:hover {
  color: #818CF8;
  background: rgba(99,102,241,0.1);
  border-color: rgba(99,102,241,0.3);
}
.delete-btn {
  color: #94A3B8;
  border-color: rgba(255,255,255,0.08);
}
.delete-btn:hover {
  color: #F87171;
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239,68,68,0.3);
}

/* ===== 價格區塊 ===== */
.price-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.price-item { }
.price-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748B;
  margin-bottom: 2px;
}
.price-target {
  font-family: 'Fira Code', monospace;
  font-size: 15px;
  font-weight: 600;
  color: #94A3B8;
}
.price-current {
  font-family: 'Fira Code', monospace;
  font-size: 17px;
  font-weight: 700;
}
.price-below { color: #34D399; }
.price-above { color: #F87171; }
.price-loading {
  font-size: 13px;
  color: #64748B;
  font-style: italic;
}
.price-divider { color: #334155; }
.price-badge-area { margin-left: auto; }

/* ===== 最後更新 ===== */
.last-checked {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #64748B;
}

/* ===== 響應式 ===== */
@media (max-width: 480px) {
  .card-image { width: 72px; }
  .price-section { flex-direction: column; align-items: flex-start; gap: 8px; }
}
</style>
