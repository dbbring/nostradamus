import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const state = {
  sidebarShow: 'responsive',
  sidebarMinimize: false,
  loading: false,
  currentSelectedDate: null,
  mutatableGainersData: [],
  immutatableGainersData: [],
  mutatableLosersData: [],
  immutatableLosersData: [],
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
  setSelectedDate(state, newDate) {
    state.currentSelectedDate = newDate;
  },
  addToDataArray(state, [array, data]) {
    state[array].push(data);
  },
  clearData(state) {
    state.mutatableGainersData = [];
    state.immutatableGainersData = [];
    state.mutatableLosersData = [];
    state.immutatableLosersData = [];
  },
  toggleChartDisplay(state, tableItem) {
    if (tableItem.category === 'Gainers') {

      if (tableItem.Display) {
        const addItem = state.immutatableGainersData.filter(ticker_item => ticker_item.basic_info.ticker === tableItem.Ticker);

        if (addItem.length) {
          state.mutatableGainersData.push(addItem[0]);
        }
        return;
      }
      state.mutatableGainersData = state.mutatableGainersData.filter(ticker_item => ticker_item.basic_info.ticker !== tableItem.Ticker);

    } else {

      if (tableItem.Display) {
        const addItem = state.immutatableLosersData.filter(ticker_item => ticker_item.basic_info.ticker === tableItem.Ticker);

        if (addItem.length) {
          state.mutatableLosersData.push(addItem[0]);
        }
        return;
      }
      state.mutatableLosersData = state.mutatableLosersData.filter(ticker_item => ticker_item.basic_info.ticker !== tableItem.Ticker);

    }
  }
};

export default new Vuex.Store({
  state,
  mutations
});