<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { marked } from 'marked'
import {
  getTemplate,
  SECTION_META,
  SECTION_ORDER,
  type TemplateData,
} from '../data/templates'

const props = defineProps<{
  templateId: string
}>()

const template = computed<TemplateData | undefined>(() => getTemplate(props.templateId))

/** Sections present on this template, in canonical order */
const presentSections = computed(() => {
  if (!template.value) return []
  return SECTION_ORDER.filter(
    (key) => template.value!.sections[key] && template.value!.sections[key]!.trim()
  )
})

/** Collapsed state per section (all expanded by default) */
const collapsed = ref<Record<string, boolean>>({})

function toggleSection(key: string) {
  collapsed.value[key] = !collapsed.value[key]
}

/** Render markdown string to HTML */
function renderMd(md: string): string {
  return marked.parse(md, { async: false }) as string
}

/** Active section for scroll-spy navigation */
const activeSection = ref('')

function scrollToSection(key: string) {
  const el = document.getElementById(`section-${key}`)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeSection.value = key
  }
}

/** Scroll spy: update active section based on scroll position */
let scrollHandler: (() => void) | null = null

onMounted(() => {
  scrollHandler = () => {
    for (const key of presentSections.value) {
      const el = document.getElementById(`section-${key}`)
      if (el) {
        const rect = el.getBoundingClientRect()
        if (rect.top <= 120) {
          activeSection.value = key
        }
      }
    }
  }
  window.addEventListener('scroll', scrollHandler, { passive: true })
})

onUnmounted(() => {
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
  }
})

/** Format tag URL for category page */
function tagUrl(tag: string): string {
  return `/categories/${tag}`
}
</script>

<template>
  <div v-if="!template" class="template-not-found">
    <p>Template not found: <code>{{ templateId }}</code></p>
  </div>

  <div v-else class="template-detail">
    <!-- Header -->
    <header class="td-header">
      <h1>{{ template.name }}</h1>
      <p class="td-description">{{ template.description }}</p>

      <!-- Tags -->
      <div v-if="template.tags?.length" class="td-tags">
        <a
          v-for="tag in template.tags"
          :key="tag"
          :href="tagUrl(tag)"
          class="tag-badge"
        >{{ tag }}</a>
      </div>
    </header>

    <!-- Layout: sidebar + content -->
    <div class="td-layout">
      <!-- Section navigation sidebar -->
      <nav v-if="presentSections.length > 2" class="td-sidebar">
        <div class="td-sidebar-title">Sections</div>
        <ul>
          <li
            v-for="key in presentSections"
            :key="key"
            :class="{ active: activeSection === key }"
          >
            <a @click.prevent="scrollToSection(key)" href="#">
              <span class="section-icon">{{ SECTION_META[key]?.icon || '📄' }}</span>
              {{ SECTION_META[key]?.label || key }}
            </a>
          </li>
        </ul>
      </nav>

      <!-- Main content -->
      <div class="td-content">
        <!-- Metadata table -->
        <section class="td-metadata">
          <h2>Metadata</h2>
          <table>
            <tbody>
              <tr>
                <th>ID</th>
                <td><code>{{ template.id }}</code></td>
              </tr>
              <tr>
                <th>Version</th>
                <td>{{ template.version }}</td>
              </tr>
              <tr>
                <th>Author</th>
                <td>{{ template.author }}</td>
              </tr>
              <tr v-if="template.compose_url">
                <th>Compose File</th>
                <td>
                  <a :href="template.compose_url" target="_blank" rel="noopener">
                    docker-compose.yml
                  </a>
                </td>
              </tr>
              <tr v-if="template.env_url">
                <th>Env Template</th>
                <td>
                  <a :href="template.env_url" target="_blank" rel="noopener">
                    .env.example
                  </a>
                </td>
              </tr>
              <tr v-if="template.documentation_url">
                <th>Documentation</th>
                <td>
                  <a :href="template.documentation_url" target="_blank" rel="noopener">
                    README.md
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </section>

        <!-- Content sections -->
        <section
          v-for="key in presentSections"
          :key="key"
          :id="`section-${key}`"
          class="td-section"
        >
          <div
            class="td-section-header"
            @click="toggleSection(key)"
            role="button"
            :aria-expanded="!collapsed[key]"
          >
            <span class="section-icon">{{ SECTION_META[key]?.icon || '📄' }}</span>
            <h2>{{ SECTION_META[key]?.label || key }}</h2>
            <span class="collapse-indicator" :class="{ collapsed: collapsed[key] }">
              ▼
            </span>
          </div>
          <div v-show="!collapsed[key]" class="td-section-body markdown-body" v-html="renderMd(template.sections[key]!)">
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.template-not-found {
  padding: 48px 24px;
  text-align: center;
  color: var(--vp-c-text-2);
}

.template-detail {
  max-width: 100%;
}

/* Header */
.td-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.td-header h1 {
  margin: 0 0 8px;
  font-size: 2em;
}

.td-description {
  margin: 0 0 16px;
  color: var(--vp-c-text-2);
  font-size: 1.1em;
  line-height: 1.6;
}

.td-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* Layout */
.td-layout {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

/* Sidebar */
.td-sidebar {
  position: sticky;
  top: 80px;
  min-width: 200px;
  max-width: 240px;
  flex-shrink: 0;
  padding: 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
}

.td-sidebar-title {
  font-weight: 600;
  font-size: 0.85em;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--vp-c-text-2);
  margin-bottom: 12px;
}

.td-sidebar ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.td-sidebar li {
  margin: 0;
}

.td-sidebar li a {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: background 0.15s;
  cursor: pointer;
}

.td-sidebar li a:hover {
  background: var(--vp-c-brand-soft);
}

.td-sidebar li.active a {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

.section-icon {
  font-size: 0.9em;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

/* Content area */
.td-content {
  flex: 1;
  min-width: 0;
}

/* Metadata */
.td-metadata {
  margin-bottom: 32px;
}

.td-metadata h2 {
  font-size: 1.2em;
  margin: 0 0 12px;
}

.td-metadata table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}

.td-metadata th,
.td-metadata td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid var(--vp-c-divider);
}

.td-metadata th {
  font-weight: 600;
  color: var(--vp-c-text-2);
  white-space: nowrap;
  width: 140px;
}

.td-metadata a {
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.td-metadata a:hover {
  text-decoration: underline;
}

/* Sections */
.td-section {
  margin-bottom: 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
}

.td-section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  cursor: pointer;
  user-select: none;
  background: var(--vp-c-bg-soft);
  transition: background 0.15s;
}

.td-section-header:hover {
  background: var(--vp-c-bg-alt);
}

.td-section-header h2 {
  flex: 1;
  margin: 0;
  font-size: 1.1em;
}

.collapse-indicator {
  font-size: 0.75em;
  color: var(--vp-c-text-3);
  transition: transform 0.2s;
}

.collapse-indicator.collapsed {
  transform: rotate(-90deg);
}

.td-section-body {
  padding: 16px 20px;
}

/* Markdown content styling */
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 0.9em;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  padding: 8px 12px;
  border: 1px solid var(--vp-c-divider);
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--vp-c-bg-soft);
  font-weight: 600;
}

.markdown-body :deep(pre) {
  background: var(--vp-c-bg-soft);
  border-radius: 6px;
  padding: 12px 16px;
  overflow-x: auto;
  font-size: 0.85em;
  line-height: 1.6;
}

.markdown-body :deep(code) {
  font-family: var(--vp-font-family-mono);
  font-size: 0.9em;
}

.markdown-body :deep(p code) {
  background: var(--vp-c-bg-soft);
  padding: 2px 6px;
  border-radius: 3px;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
}

.markdown-body :deep(li) {
  margin: 4px 0;
  line-height: 1.6;
}

.markdown-body :deep(strong) {
  font-weight: 600;
}

.markdown-body :deep(a) {
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--vp-c-brand-1);
  margin: 12px 0;
  padding: 8px 16px;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border-radius: 0 4px 4px 0;
}

/* Responsive */
@media (max-width: 768px) {
  .td-layout {
    flex-direction: column;
  }

  .td-sidebar {
    position: static;
    min-width: 100%;
    max-width: 100%;
  }

  .td-metadata th {
    width: 100px;
  }
}
</style>
