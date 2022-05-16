import { createApp } from 'vue'
import App from './App.vue'
import BaseModal from "./components/BaseComponents/BaseModal.vue"
import BaseButton from "./components/BaseComponents/BaseButton.vue"
import BaseSpinner from "./components/BaseComponents/BaseSpinner.vue"
import BaseSpinnerOverlay from "./components/BaseComponents/BaseSpinnerOverlay.vue"
import BaseSpinnerBar from "./components/BaseComponents/BaseSpinnerBar.vue"
import { createPinia } from 'pinia'
import { plugin, defaultConfig } from '@formkit/vue'
import { generateClasses } from '@formkit/tailwindcss'
import FormKitConfig  from "./assets/FormKitConfig"
import router from "./router/index"
import Notifications from '@kyvg/vue3-notification'

import './assets/css/index.css'



//createApp(App).mount("#app")
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(plugin, defaultConfig({
    config: {
        classes: generateClasses(FormKitConfig),
    },
}))
app.use(Notifications)
// Register Vue Components globally (no need to import these componenets anywhere)
app.component('BaseModal', BaseModal)
app.component('BaseButton', BaseButton)
app.component('BaseSpinner', BaseSpinner)
app.component('BaseSpinnerBar', BaseSpinnerBar)
app.component('BaseSpinnerOverlay', BaseSpinnerOverlay)
app.mount('#app')
