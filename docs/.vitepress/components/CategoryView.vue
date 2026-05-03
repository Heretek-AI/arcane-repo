<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vitepress'
import { getAllTemplates } from '../data/templates'
import type { TemplateData } from '../data/templates'
import FilterBar from './FilterBar.vue'
import TemplateGrid from './TemplateGrid.vue'
import CompareBar from './CompareBar.vue'

defineOptions({ name: 'CategoryView' })

const props = defineProps<{
  category: string
}>()

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
}

function removeCompare(id: string) {
  const next = new Set(selectedForCompare.value)
  next.delete(id)
  selectedForCompare.value = next
}

function clearCompare() {
  selectedForCompare.value = new Set()
}

// ── Filter state ──────────────────────────────────────
const searchQuery = ref('')
const selectedTags = ref<string[]>([props.category])
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

// ── Category-specific templates (for count display) ───
const categoryTemplates = computed(() =>
  allTemplates.filter((t) => t.tags.includes(props.category))
)

// ── Filtering + sorting (same as BrowseView) ──────────
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

  // Tag filter (OR logic) — always includes category, plus any user-selected tags
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
  // Tags: start with category tag, merge any URL tags
  const urlTags = q.tags
    ? (q.tags as string).split(',').filter(Boolean)
    : []
  const merged = new Set([props.category, ...urlTags])
  selectedTags.value = [...merged]
  sortBy.value = (q.sort as string) || 'name-asc'
  currentPage.value = q.page ? parseInt(q.page as string, 10) || 1 : 1
}

function pushFiltersToURL(pageOverride?: number) {
  const query: Record<string, string> = {}
  if (searchQuery.value.trim()) query.q = searchQuery.value.trim()
  // Serialize selected tags (always includes category)
  const tagsToSync = selectedTags.value.filter((t) => t !== props.category)
  if (tagsToSync.length > 0) query.tags = tagsToSync.join(',')
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
  <div class="category-view" :class="{ 'category-view--has-compare': selectedForCompare.size > 0 }">
    <a class="category-view__back" href="/browse">← Back to Browse</a>
    <h1 class="category-view__title">{{ category }}</h1>
    <p class="category-view__subtitle">
      {{ categoryTemplates.length }} templates tagged with "{{ category }}".
      Search, filter, and sort below.
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
.category-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 24px 48px;
}

.category-view__back {
  display: inline-block;
  font-size: 0.9em;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  margin-bottom: 12px;
}

.category-view__back:hover {
  text-decoration: underline;
}

.category-view__title {
  font-size: 1.8em;
  margin: 0 0 4px;
  text-transform: capitalize;
}

.category-view__subtitle {
  color: var(--vp-c-text-2);
  margin: 0 0 24px;
  font-size: 0.95em;
}

.category-view--has-compare {
  padding-bottom: 96px;
}
</style>
