import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/css/main.css'
import App from './App.vue'
import router from './router'
import { useColorMode } from '@vueuse/core'

useColorMode({
    selector: 'html',
    attribute: 'class',
    modes: {
        light: 'light',
        dark: 'dark',
    },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
