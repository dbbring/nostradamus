<template>
  <CHeader
    fixed
    with-subheader
    class="bg-dark color-white">
    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="$store.commit('toggleSidebarMobile')" />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="$store.commit('toggleSidebarDesktop')" />
    <CHeaderBrand
      class="mx-auto d-lg-none"
      to="/">
      <CIcon
        name="logo"
        height="48"
        alt="Logo" />
    </CHeaderBrand>
    <CHeaderNav class="d-md-down-none mr-auto">
      <CHeaderNavItem class="px-3">
        <CHeaderNavLink to="/dashboard">
          Dashboard
        </CHeaderNavLink>
      </CHeaderNavItem>
      <CHeaderNavItem class="px-3">
        <CHeaderNavLink
          to="/users"
          exact>
          Users
        </CHeaderNavLink>
      </CHeaderNavItem>
      <CHeaderNavItem class="px-3">
        <CHeaderNavLink>
          Settings
        </CHeaderNavLink>
      </CHeaderNavItem>
      <CHeaderNavItem class="px-3 mt-2 ml-5 pl-5">
        <datepicker
          :value="$store.state.currentSelectedDate"
          calendar-class="bg-light"
          input-class="date-input"
          class="ml-3"
          format="MM dd yyyy"
          placeholder="Pick a Date"
          @input="updateDate" />
        <h2
          v-if="$store.state.currentSelectedDate"
          class="text-center text-info py-2 mb-2">
          {{ $store.state.currentSelectedDate | $formatDateForDisplay }}
        </h2>
      </CHeaderNavItem>
    </CHeaderNav>
    <CHeaderNav class="mr-4">
      <CHeaderNavItem class="d-md-down-none mx-2">
        <CHeaderNavLink>
          <CIcon name="cil-bell" />
        </CHeaderNavLink>
      </CHeaderNavItem>
      <CHeaderNavItem class="d-md-down-none mx-2">
        <CHeaderNavLink>
          <CIcon name="cil-list" />
        </CHeaderNavLink>
      </CHeaderNavItem>
      <TheHeaderDropdownAccnt />
    </CHeaderNav>
    <CSubheader class="px-3 bg-dark">
      <CBreadcrumbRouter class="border-0 mb-0 color-white" />
    </CSubheader>
  </CHeader>
</template>

<script>
import axios from 'axios';
import TheHeaderDropdownAccnt from './TheHeaderDropdownAccnt';
import datepicker from 'vuejs-datepicker';

import { greenColors, redColors } from '../utils/colors';

export default {
  name: 'TheHeader',
  components: {
    TheHeaderDropdownAccnt,
    datepicker
  },
  methods: {
    async updateDate(date) {
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);
      this.$store.commit('clearData');
      this.$store.commit('set', ['loading', true]);
      
      await Promise.all([
        this.updateGainers(cleanDate),
        this.updateLosers(cleanDate)
      ]);
    
      this.$store.commit('set', ['loading', false]);
    },
    async updateGainers(date) {
      let counter = 0;

      const transactionGainersItems = await axios.get('http://localhost:5000/api/gainers/' + date);

      await Promise.all(transactionGainersItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/gainers/ticker/' + trans_item.transaction_id);
        const tableData = {
          table_info: {
            'Ticker': details.data.basic_info.ticker,
            'Last News Article': details.data.news[0].date_of_article || '',
            'Percent Change': details.data.basic_info.percent_change,
            'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
            'Display': true,
            'id': details.data.basic_info.transaction_id,
            'category': 'Gainers',
            'color': greenColors[counter],
            '_classes': `text-green-${counter}`,
          }
        };

        this.$store.commit('addToDataArray', ['mutatableGainersData', { ...tableData, ...details.data}]);
        this.$store.commit('addToDataArray', ['immutatableGainersData', { ...tableData, ...details.data}]);

        counter++;
      }));
    },
    async updateLosers(date) {
      let counter = 0;

      const transactionLoserItems = await axios.get('http://localhost:5000/api/losers/' + date);

      await Promise.all(transactionLoserItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/losers/ticker/' + trans_item.transaction_id);

        const tableData = {
          table_info: {
            'Ticker': details.data.basic_info.ticker,
            'Last News Article': details.data.news[0].date_of_article || '',
            'Percent Change': details.data.basic_info.percent_change,
            'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
            'Display': true,
            'id': details.data.basic_info.transaction_id,
            'category': 'Losers',
            'color': redColors[counter],
            '_classes': `text-red-${counter}`,
          }
        };

        this.$store.commit('addToDataArray', ['mutatableLosersData', { ...tableData, ...details.data}]);
        this.$store.commit('addToDataArray', ['immutatableLosersData', { ...tableData, ...details.data}]);
        counter++;
      }));
    },
  }
};
</script>

<style scoped>
.date-input {
  width: 20rem;
}
</style>