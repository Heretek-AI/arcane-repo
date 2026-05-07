<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, withBase } from 'vitepress'
import { marked } from 'marked'
import {
  getTemplate,
  SECTION_META,
  SECTION_ORDER,
  type TemplateData,
} from '../data/templates'

const route = useRoute()

/** Guard SSR — route.query may be undefined during prerender */
const isClient = ref(false)
onMounted(() => { isClient.value = true })

/** Parse template IDs from ?ids=a,b,c query param */
const selectedIds = computed<string[]>(() => {
  if (!isClient.value) return []
  const raw = route.query?.ids as string | undefined
  if (!raw) return []
  return raw
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
})

/** Resolve template data, tracking invalid IDs */
const templates = computed<{ valid: TemplateData[]; invalid: string[] }>(() => {
  const valid: TemplateData[] = []
  const invalid: string[] = []
  // Cap at 3
  const ids = selectedIds.value.slice(0, 3)
  for (const id of ids) {
    const t = getTemplate(id)
    if (t) valid.push(t)
    else invalid.push(id)
  }
  return { valid, invalid }
})

/** All section keys present across any compared template */
const activeSections = computed(() => {
  return SECTION_ORDER.filter((key) =>
    templates.value.valid.some(
      (t) => t.sections[key] && t.sections[key]!.trim()
    )
  )
})

/** Links row data: which templates have which links */
const linkRows = [
  { key: 'compose_url', label: 'Compose File', icon: '🐳' },
  { key: 'env_url', label: 'Env Template', icon: '📝' },
  { key: 'documentation_url', label: 'Documentation', icon: '📖' },
] as const

function renderMd(md: string): string {
  return marked.parse(md, { async: false }) as string
}

function templateDetailUrl(id: string): string {
  return withBase(`/templates/${id}.html`)
}
</script>

<template>
  <!-- Edge cases -->
  <div v-if="selectedIds.length === 0" class="compare-empty">
    <p class="compare-empty__icon">📊</p>
    <p class="compare-empty__title">No templates selected</p>
    <p class="compare-empty__desc">Select 2–3 templates from the browse page to compare them side by side.</p>
    <a :href="withBase('/browse.html')" class="compare-empty__link">Browse Templates →</a>
  </div>

  <div v-else-if="selectedIds.length === 1" class="compare-empty">
    <p class="compare-empty__icon">📊</p>
    <p class="compare-empty__title">Select at least 2 templates</p>
    <p class="compare-empty__desc">You need at least 2 templates to compare. Go back and select one more.</p>
    <a :href="withBase('/browse.html')" class="compare-empty__link">Browse Templates →</a>
  </div>

  <div v-else class="compare-view">
    <!-- Truncation notice -->
    <p v-if="selectedIds.length > 3" class="compare-notice">
      Showing first 3 of {{ selectedIds.length }} selected templates.
    </p>

    <!-- Invalid ID notices -->
    <div v-for="id in templates.invalid" :key="id" class="compare-invalid">
      Template <code>{{ id }}</code> was not found and has been skipped.
    </div>

    <!-- Comparison table -->
    <div class="compare-table-wrap">
      <table class="compare-table">
        <!-- Header row: template names -->
        <thead>
          <tr>
            <th class="compare-table__label"></th>
            <th v-for="t in templates.valid" :key="t.id" class="compare-table__header">
              <a :href="templateDetailUrl(t.id)" class="compare-table__name">{{ t.name }}</a>
            </th>
          </tr>
        </thead>

        <tbody>
          <!-- Description -->
          <tr>
            <th class="compare-table__label">Description</th>
            <td v-for="t in templates.valid" :key="t.id">
              <span class="compare-table__desc">{{ t.description || '—' }}</span>
            </td>
          </tr>

          <!-- Tags -->
          <tr>
            <th class="compare-table__label">Tags</th>
            <td v-for="t in templates.valid" :key="t.id">
              <div v-if="t.tags?.length" class="compare-table__tags">
                <span v-for="tag in t.tags" :key="tag" class="tag-badge">{{ tag }}</span>
              </div>
              <span v-else>—</span>
            </td>
          </tr>

          <!-- Version -->
          <tr>
            <th class="compare-table__label">Version</th>
            <td v-for="t in templates.valid" :key="t.id">
              {{ t.version || '—' }}
            </td>
          </tr>

          <!-- Author -->
          <tr>
            <th class="compare-table__label">Author</th>
            <td v-for="t in templates.valid" :key="t.id">
              {{ t.author || '—' }}
            </td>
          </tr>

          <!-- Link rows -->
          <tr v-for="link in linkRows" :key="link.key">
            <th class="compare-table__label">
              <span class="compare-table__label-icon">{{ link.icon }}</span>
              {{ link.label }}
            </th>
            <td v-for="t in templates.valid" :key="t.id">
              <a
                v-if="(t as any)[link.key]"
                :href="(t as any)[link.key]"
                target="_blank"
                rel="noopener"
                class="compare-table__link"
              >
                View ↗
              </a>
              <span v-else>—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- README sections -->
    <div v-if="activeSections.length > 0" class="compare-sections">
      <div
        v-for="sectionKey in activeSections"
        :key="sectionKey"
        class="compare-section"
      >
        <h2 class="compare-section__title">
          <span class="compare-section__icon">{{ SECTION_META[sectionKey]?.icon || '📄' }}</span>
          {{ SECTION_META[sectionKey]?.label || sectionKey }}
        </h2>
        <div class="compare-section__grid">
          <div
            v-for="t in templates.valid"
            :key="t.id"
            class="compare-section__card"
          >
            <div class="compare-section__card-header">{{ t.name }}</div>
            <div
              v-if="t.sections[sectionKey]?.trim()"
              class="compare-section__card-body markdown-body"
              v-html="renderMd(t.sections[sectionKey]!)"
            ></div>
            <div v-else class="compare-section__card-empty">—</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Empty / edge-case states ────────────────────── */
.compare-empty {
  text-align: center;
  padding: 80px 24px;
  max-width: 420px;
  margin: 0 auto;
}

.compare-empty__icon {
  font-size: 3em;
  margin: 0 0 12px;
}

.compare-empty__title {
  font-size: 1.4em;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--vp-c-text-1);
}

.compare-empty__desc {
  color: var(--vp-c-text-2);
  margin: 0 0 24px;
  line-height: 1.6;
}

.compare-empty__link {
  display: inline-block;
  padding: 10px 24px;
  border-radius: 8px;
  background: var(--vp-c-brand-1);
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s;
}

.compare-empty__link:hover {
  background: var(--vp-c-brand-2);
}

/* ── Notice banners ──────────────────────────────── */
.compare-notice,
.compare-invalid {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 0.9em;
  margin-bottom: 16px;
}

.compare-notice {
  background: var(--vp-c-yellow-soft, rgba(234, 179, 8, 0.14));
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-yellow, #eab308);
}

.compare-invalid {
  background: var(--vp-c-red-soft, rgba(239, 68, 68, 0.14));
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-red, #ef4444);
  margin-bottom: 8px;
}

.compare-invalid code {
  background: var(--vp-c-bg-soft);
  padding: 1px 6px;
  border-radius: 3px;
}

/* ── Comparison table ────────────────────────────── */
.compare-view {
  max-width: 100%;
}

.compare-table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 32px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
  min-width: 600px;
}

.compare-table th,
.compare-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--vp-c-divider);
  vertical-align: top;
}

.compare-table__label {
  position: sticky;
  left: 0;
  background: var(--vp-c-bg-soft);
  font-weight: 600;
  color: var(--vp-c-text-2);
  white-space: nowrap;
  min-width: 140px;
  width: 160px;
  z-index: 1;
}

.compare-table__label-icon {
  margin-right: 4px;
}

.compare-table__header {
  background: var(--vp-c-bg-soft);
  text-align: center;
}

.compare-table__name {
  font-size: 1.05em;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.compare-table__name:hover {
  text-decoration: underline;
}

.compare-table__desc {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
  color: var(--vp-c-text-1);
}

.compare-table__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.compare-table__link {
  color: var(--vp-c-brand-1);
  text-decoration: none;
  font-weight: 500;
}

.compare-table__link:hover {
  text-decoration: underline;
}

/* Alternating row colors for readability */
.compare-table tbody tr:nth-child(even) {
  background: var(--vp-c-bg-alt, rgba(0, 0, 0, 0.02));
}

.compare-table tbody tr:nth-child(even) .compare-table__label {
  background: var(--vp-c-bg-alt, rgba(0, 0, 0, 0.02));
}

/* ── Section comparisons ─────────────────────────── */
.compare-sections {
  margin-top: 16px;
}

.compare-section {
  margin-bottom: 32px;
}

.compare-section__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.3em;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.compare-section__icon {
  font-size: 0.9em;
}

.compare-section__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.compare-section__card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
}

.compare-section__card-header {
  padding: 10px 16px;
  background: var(--vp-c-bg-soft);
  font-weight: 600;
  font-size: 0.95em;
  border-bottom: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-1);
}

.compare-section__card-body {
  padding: 16px;
  max-height: 500px;
  overflow-y: auto;
}

.compare-section__card-empty {
  padding: 24px 16px;
  text-align: center;
  color: var(--vp-c-text-3);
  font-size: 0.9em;
}

/* ── Mobile: stack table to cards ────────────────── */
@media (max-width: 768px) {
  .compare-table-wrap {
    border: none;
    border-radius: 0;
  }

  .compare-table {
    min-width: unset;
  }

  .compare-table thead {
    display: none;
  }

  .compare-table,
  .compare-table tbody,
  .compare-table tr,
  .compare-table td,
  .compare-table th {
    display: block;
  }

  .compare-table tr {
    border: 1px solid var(--vp-c-divider);
    border-radius: 8px;
    margin-bottom: 12px;
    overflow: hidden;
  }

  .compare-table__label {
    position: static;
    width: 100%;
    min-width: unset;
    background: var(--vp-c-bg-soft);
    border-bottom: 1px solid var(--vp-c-divider);
  }

  .compare-table td {
    padding: 8px 16px;
    border-bottom: none;
  }

  .compare-table tbody tr:nth-child(even) {
    background: transparent;
  }

  .compare-section__grid {
    grid-template-columns: 1fr;
  }
}
</style>
