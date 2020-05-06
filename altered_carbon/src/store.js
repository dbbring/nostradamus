import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const state = {
  sidebarShow: 'responsive',
  sidebarMinimize: false,
  loading: false,
  currentSelectedDate: null
};

const mutations = {
  toggleSidebarDesktop(state) {
    const sidebarOpened = [true, 'responsive'].includes(state.sidebarShow);
    state.sidebarShow = sidebarOpened ? false : 'responsive';
  },
  toggleSidebarMobile(state) {
    const sidebarClosed = [false, 'responsive'].includes(state.sidebarShow);
    state.sidebarShow = sidebarClosed ? true : 'responsive';
  },
  set(state, [variable, value]) {
    state[variable] = value;
  },
  toggleLoading(state, value) {
    state.loading = value;
  },
  setSelectedDate(state, newDate) {
    state.currentSelectedDate = newDate;
  }
};

export default new Vuex.Store({
  state,
  mutations
});