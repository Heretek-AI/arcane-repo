import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import TemplateDetail from '../components/TemplateDetail.vue'
import FilterBar from '../components/FilterBar.vue'
import TemplateGrid from '../components/TemplateGrid.vue'
import BrowseView from '../components/BrowseView.vue'
import CategoryView from '../components/CategoryView.vue'
import CompareBar from '../components/CompareBar.vue'
import CompareView from '../components/CompareView.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('TemplateDetail', TemplateDetail)
    app.component('FilterBar', FilterBar)
    app.component('TemplateGrid', TemplateGrid)
    app.component('BrowseView', BrowseView)
    app.component('CategoryView', CategoryView)
    app.component('CompareBar', CompareBar)
  },
  Layout() {
    const { frontmatter } = useData()

    if (frontmatter.value.layout === 'template-detail') {
      return h(TemplateDetail, { templateId: frontmatter.value.templateId })
    }

    if (frontmatter.value.layout === 'browse') {
      return h(BrowseView)
    }

    if (frontmatter.value.layout === 'category') {
      return h(CategoryView, { category: frontmatter.value.category })
    }

    if (frontmatter.value.layout === 'compare') {
      return h(CompareView)
    }

    return h(DefaultTheme.Layout)
  },
}
