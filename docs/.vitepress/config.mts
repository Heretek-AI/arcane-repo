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
            { text: 'self-hosted (683)', link: '/categories/self-hosted' },
            { text: 'portainer (227)', link: '/categories/portainer' },
            { text: 'yunohost (221)', link: '/categories/yunohost' },
            { text: 'umbrel (119)', link: '/categories/umbrel' },
            { text: 'ai (105)', link: '/categories/ai' },
            { text: 'awesome-selfhosted (82)', link: '/categories/awesome-selfhosted' },
            { text: 'non-serviceable (38)', link: '/categories/non-serviceable' },
            { text: 'llm (26)', link: '/categories/llm' },
            { text: 'devops (26)', link: '/categories/devops' },
            { text: 'agents (22)', link: '/categories/agents' },
            { text: 'monitoring (20)', link: '/categories/monitoring' },
            { text: 'tools (16)', link: '/categories/tools' },
            { text: 'rag (15)', link: '/categories/rag' },
            { text: 'database (13)', link: '/categories/database' },
            { text: 'framework (12)', link: '/categories/framework' },
            { text: 'security (12)', link: '/categories/security' },
            { text: 'communication (12)', link: '/categories/communication' },
            { text: 'storage (12)', link: '/categories/storage' },
            { text: 'cms (11)', link: '/categories/cms' },
            { text: 'automation (11)', link: '/categories/automation' },
            { text: 'infrastructure (10)', link: '/categories/infrastructure' },
            { text: 'identity (9)', link: '/categories/identity' },
            { text: 'authentication (9)', link: '/categories/authentication' },
            { text: 'observability (9)', link: '/categories/observability' },
            { text: 'search (8)', link: '/categories/search' },
            { text: 'business (7)', link: '/categories/business' },
            { text: 'e-commerce (7)', link: '/categories/e-commerce' },
            { text: 'web (7)', link: '/categories/web' },
            { text: 'multi-service (7)', link: '/categories/multi-service' },
            { text: 'orchestration (7)', link: '/categories/orchestration' },
            { text: 'analytics (7)', link: '/categories/analytics' },
            { text: 'low-code (6)', link: '/categories/low-code' },
            { text: 'workflow (6)', link: '/categories/workflow' },
            { text: 'api (6)', link: '/categories/api' },
            { text: 'platform (5)', link: '/categories/platform' },
            { text: 'productivity (5)', link: '/categories/productivity' },
            { text: 'paas (5)', link: '/categories/paas' },
            { text: 'sql (5)', link: '/categories/sql' },
            { text: 'reference (5)', link: '/categories/reference' },
            { text: 'media (5)', link: '/categories/media' },
            { text: 'chat (5)', link: '/categories/chat' },
            { text: 'research (4)', link: '/categories/research' },
            { text: 'python (4)', link: '/categories/python' },
            { text: 'gateway (4)', link: '/categories/gateway' },
            { text: 'proxy (3)', link: '/categories/proxy' },
            { text: 'entertainment (3)', link: '/categories/entertainment' },
            { text: 'inference (3)', link: '/categories/inference' },
            { text: 'collaboration (2)', link: '/categories/collaboration' },
            { text: 'bitcoin (2)', link: '/categories/bitcoin' },
            { text: 'iot (2)', link: '/categories/iot' },
            { text: 'priority (2)', link: '/categories/priority' },
            { text: 'custom-build (1)', link: '/categories/custom-build' }
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
