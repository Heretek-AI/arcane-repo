<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  searchQuery: string
  selectedTags: string[]
  sortBy: string
  availableTags: string[]
}>()

const emit = defineEmits<{
  'update:searchQuery': [value: string]
  'update:selectedTags': [value: string[]]
  'update:sortBy': [value: string]
}>()

// --- Search with debounce ---
const localSearch = ref(props.searchQuery)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(
  () => props.searchQuery,
  (val) => {
    localSearch.value = val
  }
)

function onSearchInput(e: Event) {
  const val = (e.target as HTMLInputElement).value
  localSearch.value = val
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('update:searchQuery', val)
  }, 300)
}

// --- Tag chips ---
const showAllTags = ref(false)

const visibleTags = computed(() => {
  if (showAllTags.value) return props.availableTags
  return props.availableTags.slice(0, 15)
})

const hasMoreTags = computed(() => props.availableTags.length > 15)

function toggleTag(tag: string) {
  const idx = props.selectedTags.indexOf(tag)
  const next = [...props.selectedTags]
  if (idx === -1) {
    next.push(tag)
  } else {
    next.splice(idx, 1)
  }
  emit('update:selectedTags', next)
}

function isTagSelected(tag: string) {
  return props.selectedTags.includes(tag)
}

// --- Sort ---
function onSortChange(e: Event) {
  emit('update:sortBy', (e.target as HTMLSelectElement).value)
}
</script>

<template>
  <div class="filter-bar">
    <!-- Search -->
    <div class="filter-bar__search">
      <input
        type="text"
        class="search-input"
        placeholder="Search templates..."
        :value="localSearch"
        @input="onSearchInput"
      />
    </div>

    <!-- Sort + Tag row -->
    <div class="filter-bar__controls">
      <div class="filter-bar__tags">
        <button
          v-for="tag in visibleTags"
          :key="tag"
          class="tag-chip"
          :class="{ active: isTagSelected(tag) }"
          @click="toggleTag(tag)"
        >
          {{ tag }}
        </button>
        <button
          v-if="hasMoreTags"
          class="tag-chip tag-chip--toggle"
          @click="showAllTags = !showAllTags"
        >
          {{ showAllTags ? 'Show less' : `Show all (${availableTags.length})` }}
        </button>
      </div>

      <select class="sort-select" :value="sortBy" @change="onSortChange">
        <option value="name-asc">A → Z</option>
        <option value="name-desc">Z → A</option>
        <option value="category">By category</option>
      </select>
    </div>
  </div>
</template>
