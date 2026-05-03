import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Arcane Template Registry',
  description: 'Browse and search 785+ self-hosted Docker templates',
  base: '/arcane-repo/',
  ignoreDeadLinks: true,
  themeConfig: {
    search: {
      provider: 'local'
    },
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Browse', link: '/browse' },
      { text: 'Compare', link: '/compare' },
      { text: 'All Templates', link: '/templates/' },
      { text: 'GitHub', link: 'https://github.com/Heretek-AI/arcane-repo' }
    ],
    sidebar: {
      '/categories/': [
      // CATEGORIES_SIDEBAR_START
        {
          text: 'Categories',
          items: [
            { text: 'Overview', link: '/categories/' },
            { text: 'self-hosted (654)', link: '/categories/self-hosted' },
            { text: 'portainer (227)', link: '/categories/portainer' },
            { text: 'yunohost (221)', link: '/categories/yunohost' },
            { text: 'umbrel (119)', link: '/categories/umbrel' },
            { text: 'ai (97)', link: '/categories/ai' },
            { text: 'awesome-selfhosted (82)', link: '/categories/awesome-selfhosted' },
            { text: 'non-serviceable (38)', link: '/categories/non-serviceable' },
            { text: 'agents (22)', link: '/categories/agents' },
            { text: 'llm (18)', link: '/categories/llm' },
            { text: 'devops (16)', link: '/categories/devops' },
            { text: 'rag (15)', link: '/categories/rag' },
            { text: 'monitoring (15)', link: '/categories/monitoring' },
            { text: 'framework (12)', link: '/categories/framework' },
            { text: 'security (12)', link: '/categories/security' },
            { text: 'storage (12)', link: '/categories/storage' },
            { text: 'cms (11)', link: '/categories/cms' },
            { text: 'communication (9)', link: '/categories/communication' },
            { text: 'database (9)', link: '/categories/database' },
            { text: 'automation (9)', link: '/categories/automation' },
            { text: 'observability (9)', link: '/categories/observability' },
            { text: 'tools (8)', link: '/categories/tools' },
            { text: 'search (8)', link: '/categories/search' },
            { text: 'web (7)', link: '/categories/web' },
            { text: 'multi-service (7)', link: '/categories/multi-service' },
            { text: 'orchestration (7)', link: '/categories/orchestration' },
            { text: 'analytics (7)', link: '/categories/analytics' },
            { text: 'low-code (6)', link: '/categories/low-code' },
            { text: 'workflow (6)', link: '/categories/workflow' },
            { text: 'api (6)', link: '/categories/api' },
            { text: 'platform (5)', link: '/categories/platform' },
            { text: 'paas (5)', link: '/categories/paas' },
            { text: 'sql (5)', link: '/categories/sql' },
            { text: 'reference (5)', link: '/categories/reference' },
            { text: 'chat (5)', link: '/categories/chat' },
            { text: 'research (4)', link: '/categories/research' },
            { text: 'python (4)', link: '/categories/python' },
            { text: 'gateway (4)', link: '/categories/gateway' },
            { text: 'proxy (3)', link: '/categories/proxy' },
            { text: 'inference (3)', link: '/categories/inference' },
            { text: 'priority (2)', link: '/categories/priority' },
            { text: 'custom-build (1)', link: '/categories/custom-build' },
            { text: 'media (1)', link: '/categories/media' }
          ]
        }
      // CATEGORIES_SIDEBAR_END
      ],
      '/templates/': [
        {
          text: 'Templates',
          items: [
            { text: 'All Templates', link: '/templates/' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Heretek-AI/arcane-repo' }
    ]
  }
})
