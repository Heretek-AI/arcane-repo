<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { TemplateData } from '../data/templates'

const props = withDefaults(
  defineProps<{
    templates: TemplateData[]
    pageSize?: number
    initialPage?: number
  }>(),
  { pageSize: 24, initialPage: 1 }
)

const emit = defineEmits<{
  'update:currentPage': [page: number]
}>()

const currentPage = ref(props.initialPage)

// Reset to page 1 when the filtered list changes (but not on first mount)
const isFirstWatch = ref(true)
watch(
  () => props.templates,
  () => {
    if (isFirstWatch.value) {
      isFirstWatch.value = false
      return
    }
    currentPage.value = 1
    emit('update:currentPage', 1)
  }
)

const totalCount = computed(() => props.templates.length)

const totalPages = computed(() =>
  Math.max(1, Math.ceil(totalCount.value / props.pageSize))
)

const pagedTemplates = computed(() => {
  const start = (currentPage.value - 1) * props.pageSize
  return props.templates.slice(start, start + props.pageSize)
})

const showingStart = computed(() =>
  totalCount.value === 0 ? 0 : (currentPage.value - 1) * props.pageSize + 1
)

const showingEnd = computed(() =>
  Math.min(currentPage.value * props.pageSize, totalCount.value)
)

/** Visible page numbers — show up to 7 pages with ellipsis */
const visiblePages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  const pages: (number | string)[] = [1]
  const rangeStart = Math.max(2, current - 1)
  const rangeEnd = Math.min(total - 1, current + 1)
  if (rangeStart > 2) pages.push('...')
  for (let i = rangeStart; i <= rangeEnd; i++) pages.push(i)
  if (rangeEnd < total - 1) pages.push('...')
  pages.push(total)
  return pages
})

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    emit('update:currentPage', page)
  }
}
</script>

<template>
  <div class="template-grid-wrapper">
    <!-- Result count -->
    <p class="results-count" v-if="totalCount > 0">
      Showing <strong>{{ showingStart }}–{{ showingEnd }}</strong> of
      <strong>{{ totalCount }}</strong> templates
    </p>

    <!-- Empty state -->
    <div v-if="totalCount === 0" class="empty-state">
      <p>😕 No templates match your filters.</p>
      <p>Try removing some filters or changing your search.</p>
    </div>

    <!-- Card grid -->
    <div v-else class="template-grid">
      <a
        v-for="t in pagedTemplates"
        :key="t.id"
        :href="`/templates/${t.id}`"
        class="template-card"
      >
        <h3>{{ t.name }}</h3>
        <p class="template-card__desc">{{ t.description }}</p>
        <div class="template-card__tags">
          <span v-for="tag in t.tags" :key="tag" class="tag-badge">{{ tag }}</span>
        </div>
      </a>
    </div>

    <!-- Pagination -->
    <nav v-if="totalPages > 1" class="pagination" aria-label="Template pagination">
      <button
        class="pagination__btn"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        ← Prev
      </button>

      <template v-for="(page, i) in visiblePages" :key="i">
        <span v-if="typeof page === 'string'" class="pagination__ellipsis">…</span>
        <button
          v-else
          class="pagination__btn"
          :class="{ 'pagination__btn--active': page === currentPage }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>

      <button
        class="pagination__btn"
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        Next →
      </button>
    </nav>
  </div>
</template>
