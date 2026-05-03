import DefaultTheme from 'vitepress/theme'
import TemplateDetail from '../components/TemplateDetail.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('TemplateDetail', TemplateDetail)
  },
}
