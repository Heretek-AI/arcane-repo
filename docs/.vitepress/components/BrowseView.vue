<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vitepress'
import { getAllTemplates } from '../data/templates'
import type { TemplateData } from '../data/templates'
import FilterBar from './FilterBar.vue'
import TemplateGrid from './TemplateGrid.vue'

defineOptions({ name: 'BrowseView' })

const router = useRouter()
const route = useRoute()

// ── Data ──────────────────────────────────────────────
const allTemplates = getAllTemplates()

// ── Filter state ──────────────────────────────────────
const searchQuery = ref('')
const selectedTags = ref<string[]>([])
const sortBy = ref('name-asc')
const currentPage = ref(1)

// ── Compute available tags sorted by frequency ────────
const tagCounts = new Map<string, number>()
for (const t of allTemplates) {
  for (const tag of t.tags) {
    tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1)
  }
}
const availableTags = [...tagCounts.entries()]
  .sort((a, b) => b[1] - a[1])
  .map(([tag]) => tag)

// ── Filtering + sorting ───────────────────────────────
const filteredTemplates = computed(() => {
  let result = allTemplates

  // Search filter (name, description, id)
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    result = result.filter(
      (t) =>
        t.name.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.id.toLowerCase().includes(q)
    )
  }

  // Tag filter (OR logic)
  if (selectedTags.value.length > 0) {
    result = result.filter((t) =>
      selectedTags.value.some((tag) => t.tags.includes(tag))
    )
  }

  // Sort
  switch (sortBy.value) {
    case 'name-desc':
      result = [...result].sort((a, b) => b.name.localeCompare(a.name))
      break
    case 'category':
      result = [...result].sort((a, b) => {
        const catA = a.tags[0] || ''
        const catB = b.tags[0] || ''
        return catA.localeCompare(catB) || a.name.localeCompare(b.name)
      })
      break
    default: // name-asc
      result = [...result].sort((a, b) => a.name.localeCompare(b.name))
  }

  return result
})

// ── URL sync helpers ──────────────────────────────────
function readFiltersFromURL() {
  const q = route.query
  searchQuery.value = (q.q as string) || ''
  selectedTags.value = q.tags
    ? (q.tags as string).split(',').filter(Boolean)
    : []
  sortBy.value = (q.sort as string) || 'name-asc'
  currentPage.value = q.page ? parseInt(q.page as string, 10) || 1 : 1
}

function pushFiltersToURL(pageOverride?: number) {
  const query: Record<string, string> = {}
  if (searchQuery.value.trim()) query.q = searchQuery.value.trim()
  if (selectedTags.value.length > 0) query.tags = selectedTags.value.join(',')
  if (sortBy.value !== 'name-asc') query.sort = sortBy.value
  const p = pageOverride ?? currentPage.value
  if (p > 1) query.page = String(p)

  const target = router.route.path
  router.withoutScroll(() => {
    router.replace(target, query)
  })
}

// ── Initialize from URL on mount ──────────────────────
onMounted(() => {
  readFiltersFromURL()
})

// ── Sync back/forward navigation ──────────────────────
watch(
  () => route.query,
  () => {
    readFiltersFromURL()
  }
)

// ── Push URL on filter changes ────────────────────────
watch([searchQuery, selectedTags, sortBy], () => {
  currentPage.value = 1
  pushFiltersToURL(1)
})

// ── Push URL on page change ───────────────────────────
function onPageChange(page: number) {
  currentPage.value = page
  pushFiltersToURL(page)
}
</script>

<template>
  <div class="browse-view">
    <h1 class="browse-view__title">Browse Templates</h1>
    <p class="browse-view__subtitle">
      Search, filter, and sort across {{ allTemplates.length }} self-hosted Docker templates.
    </p>

    <FilterBar
      :searchQuery="searchQuery"
      :selectedTags="selectedTags"
      :sortBy="sortBy"
      :availableTags="availableTags"
      @update:searchQuery="searchQuery = $event"
      @update:selectedTags="selectedTags = $event"
      @update:sortBy="sortBy = $event"
    />

    <TemplateGrid
      :templates="filteredTemplates"
      :initialPage="currentPage"
      @update:currentPage="onPageChange"
    />
  </div>
</template>

<style scoped>
.browse-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 24px 48px;
}

.browse-view__title {
  font-size: 1.8em;
  margin: 0 0 4px;
}

.browse-view__subtitle {
  color: var(--vp-c-text-2);
  margin: 0 0 24px;
  font-size: 0.95em;
}
</style>
