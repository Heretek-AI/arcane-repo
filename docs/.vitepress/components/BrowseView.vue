<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vitepress'
import { getAllTemplates } from '../data/templates'
import type { TemplateData } from '../data/templates'
import FilterBar from './FilterBar.vue'
import TemplateGrid from './TemplateGrid.vue'
import CompareBar from './CompareBar.vue'

defineOptions({ name: 'BrowseView' })

const router = useRouter()
const route = useRoute()

// ── Data ──────────────────────────────────────────────
const allTemplates = getAllTemplates()

// ── Template lookup map (shared with CompareBar) ──────
const templateMap = new Map<string, TemplateData>(
  allTemplates.map(t => [t.id, t])
)

// ── Compare state ─────────────────────────────────────
const selectedForCompare = ref<Set<string>>(new Set())

function toggleCompare(id: string) {
  const next = new Set(selectedForCompare.value)
  if (next.has(id)) {
    next.delete(id)
  } else if (next.size < 3) {
    next.add(id)
  }
  selectedForCompare.value = next
  pushFiltersToURL()
}

function removeCompare(id: string) {
  const next = new Set(selectedForCompare.value)
  next.delete(id)
  selectedForCompare.value = next
  pushFiltersToURL()
}

function clearCompare() {
  selectedForCompare.value = new Set()
  pushFiltersToURL()
}

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

  // Read compare param — validate IDs against known templates, enforce max 3
  const compareParam = q.compare as string | undefined
  if (compareParam) {
    const ids = compareParam.split(',').filter(id => templateMap.has(id))
    selectedForCompare.value = new Set(ids.slice(0, 3))
  } else {
    selectedForCompare.value = new Set()
  }
}

function pushFiltersToURL(pageOverride?: number) {
  const query: Record<string, string> = {}
  if (searchQuery.value.trim()) query.q = searchQuery.value.trim()
  if (selectedTags.value.length > 0) query.tags = selectedTags.value.join(',')
  if (sortBy.value !== 'name-asc') query.sort = sortBy.value
  if (selectedForCompare.value.size > 0) query.compare = [...selectedForCompare.value].join(',')
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
  <div class="browse-view" :class="{ 'browse-view--has-compare': selectedForCompare.size > 0 }">
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
      :selectedForCompare="selectedForCompare"
      @update:currentPage="onPageChange"
      @toggleCompare="toggleCompare"
    />

    <CompareBar
      :selectedIds="[...selectedForCompare]"
      :templateMap="templateMap"
      @remove="removeCompare"
      @clear="clearCompare"
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

.browse-view--has-compare {
  padding-bottom: 96px;
}
</style>
