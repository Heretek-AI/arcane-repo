import data from './templates.data.json'

export interface TemplateSections {
  quickStart?: string
  architecture?: string
  configuration?: string
  troubleshooting?: string
  backup?: string
  links?: string
  prerequisites?: string
  apiEndpoints?: string
  serviceDetails?: string
  healthCheck?: string
  upstream?: string
  [key: string]: string | undefined
}

export interface TemplateData {
  id: string
  name: string
  description: string
  version: string
  author: string
  compose_url: string
  env_url: string
  documentation_url: string
  content_hash: string
  tags: string[]
  sections: TemplateSections
  intro: string
}

const templates: TemplateData[] = data as TemplateData[]

/** Map of template ID → template data for O(1) lookup */
const templateMap = new Map<string, TemplateData>(
  templates.map((t) => [t.id, t])
)

/** Get a template by ID */
export function getTemplate(id: string): TemplateData | undefined {
  return templateMap.get(id)
}

/** Get all templates */
export function getAllTemplates(): TemplateData[] {
  return templates
}

/** Section display names and icon hints for rendering order */
export const SECTION_META: Record<string, { label: string; icon: string }> = {
  quickStart: { label: 'Quick Start', icon: '🚀' },
  architecture: { label: 'Architecture', icon: '🏗️' },
  configuration: { label: 'Configuration', icon: '⚙️' },
  prerequisites: { label: 'Prerequisites', icon: '📋' },
  troubleshooting: { label: 'Troubleshooting', icon: '🔧' },
  backup: { label: 'Backup & Recovery', icon: '💾' },
  apiEndpoints: { label: 'API Endpoints', icon: '🔌' },
  serviceDetails: { label: 'Service Details', icon: '📦' },
  healthCheck: { label: 'Health Check', icon: '❤️' },
  upstream: { label: 'Upstream', icon: '⬆️' },
  links: { label: 'Links', icon: '🔗' },
}

/** Ordered section keys for consistent rendering */
export const SECTION_ORDER = Object.keys(SECTION_META)

export default templates
