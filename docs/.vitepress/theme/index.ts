import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import TemplateDetail from '../components/TemplateDetail.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('TemplateDetail', TemplateDetail)
  },
  Layout() {
    const { frontmatter } = useData()

    if (frontmatter.value.layout === 'template-detail') {
      return h(TemplateDetail, { templateId: frontmatter.value.templateId })
    }

    return h(DefaultTheme.Layout)
  },
}
