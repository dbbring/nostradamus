import 'core-js/stable';
import Vue from 'vue';
import App from './App';
import router from './router';
import CoreuiVue from '@coreui/vue';
import { iconsSet as icons } from './assets/icons/icons.js';
import store from './store';
import './utils/filters';

Vue.config.performance = true;
Vue.use(CoreuiVue);
Vue.prototype.$log = console.log.bind(console);

new Vue({
  el: '#app',
  router,
  store,
  icons,
  components: {
    App
  },
  template: '<App/>'
});
