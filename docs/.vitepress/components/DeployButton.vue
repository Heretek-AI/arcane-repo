<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  /** URL to fetch raw content from (e.g. GitHub raw file URL) */
  url: string
  /** Button label shown before copy */
  label: string
}>()

const state = ref<'idle' | 'copying' | 'copied' | 'error'>('idle')
let resetTimer: ReturnType<typeof setTimeout> | null = null

async function copyToClipboard() {
  if (state.value === 'copying') return

  // Clear any pending reset
  if (resetTimer) {
    clearTimeout(resetTimer)
    resetTimer = null
  }

  state.value = 'copying'

  try {
    const resp = await fetch(props.url)
    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}`)
    }
    const text = await resp.text()
    await navigator.clipboard.writeText(text)
    state.value = 'copied'

    // Reset after 2 seconds
    resetTimer = setTimeout(() => {
      state.value = 'idle'
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
    state.value = 'error'
    resetTimer = setTimeout(() => {
      state.value = 'idle'
    }, 3000)
  }
}
</script>

<template>
  <button
    class="deploy-btn"
    :class="{
      'deploy-btn--copied': state === 'copied',
      'deploy-btn--error': state === 'error',
      'deploy-btn--busy': state === 'copying',
    }"
    :disabled="state === 'copying'"
    :title="state === 'copied' ? 'Copied!' : state === 'error' ? 'Failed to copy' : `Copy ${label}`"
    @click="copyToClipboard"
  >
    <span class="deploy-btn__icon" aria-hidden="true">
      <template v-if="state === 'copied'">✓</template>
      <template v-else-if="state === 'error'">✕</template>
      <template v-else>📋</template>
    </span>
    <span class="deploy-btn__text">
      <template v-if="state === 'copying'">Copying…</template>
      <template v-else-if="state === 'copied'">Copied!</template>
      <template v-else-if="state === 'error'">Failed</template>
      <template v-else>Copy {{ label }}</template>
    </span>
  </button>
</template>

<style scoped>
.deploy-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  font-size: 0.8em;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  vertical-align: middle;
}

.deploy-btn:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.deploy-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}

.deploy-btn--copied {
  border-color: #22c55e;
  color: #22c55e;
  background: rgba(34, 197, 94, 0.08);
}

.deploy-btn--error {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.08);
}

.deploy-btn__icon {
  font-size: 0.95em;
  line-height: 1;
}

.deploy-btn__text {
  line-height: 1;
}
</style>
