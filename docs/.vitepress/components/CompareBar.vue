<script setup lang="ts">
import { useRouter, withBase } from 'vitepress'
import type { TemplateData } from '../data/templates'

defineOptions({ name: 'CompareBar' })

const props = withDefaults(
  defineProps<{
    selectedIds: string[]
    templateMap: Map<string, TemplateData>
    maxSelection?: number
  }>(),
  { maxSelection: 3 }
)

const emit = defineEmits<{
  remove: [id: string]
  clear: []
}>()

const router = useRouter()

function getTemplateName(id: string): string {
  return props.templateMap.get(id)?.name ?? id
}

function goToCompare() {
  const ids = props.selectedIds.join(',')
  router.go(`/compare.html?ids=${ids}`)
}

function onRemove(id: string) {
  emit('remove', id)
}
</script>

<template>
  <Transition name="compare-bar-slide">
    <div v-if="selectedIds.length > 0" class="compare-bar" role="region" aria-label="Template comparison">
      <div class="compare-bar__inner">
        <div class="compare-bar__chips">
          <span
            v-for="id in selectedIds"
            :key="id"
            class="compare-chip"
          >
            {{ getTemplateName(id) }}
            <button
              class="compare-chip__remove"
              :aria-label="`Remove ${getTemplateName(id)} from comparison`"
              @click="onRemove(id)"
            >
              ×
            </button>
          </span>
        </div>
        <div class="compare-bar__actions">
          <span class="compare-bar__count">{{ selectedIds.length }}/{{ maxSelection }}</span>
          <button class="compare-bar__clear" @click="emit('clear')">Clear</button>
          <button
            class="compare-bar__btn"
            :disabled="selectedIds.length < 2"
            @click="goToCompare"
          >
            Compare ({{ selectedIds.length }})
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>
