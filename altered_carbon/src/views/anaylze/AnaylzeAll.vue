<template>
  <div>
    <CCard class="bg-light">
      <CCardHeader>
        <CRow>
          <h4 class="h4 ml-2 text-white text-center">
            Select Date:
          </h4>
          <datepicker
            :value="$store.state.currentSelectedDate"
            class="ml-3"
            @input="updateDate" />
        </CRow>
      </CCardHeader>
      <CCardBody>
        <CRow class="text-center text-info py-2 mb-2">
          <CCol>
            <h2>{{ $store.state.currentSelectedDate | $formatDateForDisplay }}</h2>
          </CCol>
        </CRow>
        <CRow>
          <img 
            v-if="isLoading"
            id="loader"
            src="img/loader.svg">
          <CCol
            lg="6"
            style="min-height: 400px;">
            <transition name="fade">
              <CTableWrapper 
                v-if="!isLoading"
                class="bg-dark"
                :items="transactionGainersData"
                :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date']">
                <template #header>
                  <CIcon name="cil-grid" /> Gainers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ transactionGainersData.length }}</small>
                  </div>
                </template>
              </CTableWrapper>
            </transition>
          </CCol>
          <CCol
            lg="6"
            style="min-height: 400px;">
            <transition name="fade">
              <CTableWrapper 
                v-if="!isLoading"
                class="bg-dark"
                :items="transactionLosersData"
                :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date']">
                <template #header>
                  <CIcon name="cil-grid" /> Losers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ transactionLosersData.length }}</small>
                  </div>
                </template>
              </CTableWrapper>
            </transition>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>
    <CCard>
      <CCardHeader>
        <CIcon name="cil-drop" /> Grays
      </CCardHeader>
      <CCardBody>
        <CRow>
          <ColorTheme color="bg-gray-100">
            <h6>Brand 100 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-200">
            <h6>Brand 200 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-300">
            <h6>Brand 300 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-400">
            <h6>Brand 400 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-500">
            <h6>Brand 500 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-600">
            <h6>Brand 600 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-700">
            <h6>Brand 700 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-800">
            <h6>Brand 800 Color</h6>
          </ColorTheme>
          <ColorTheme color="bg-gray-900">
            <h6>Brand 900 Color</h6>
          </ColorTheme>
        </CRow> 
      </CCardBody>
    </CCard>
  </div>
</template>

<script>
import axios from 'axios';
import ColorTheme from './ColorTheme';
import datepicker from 'vuejs-datepicker';
import CTableWrapper from '../../utils/Table.vue';

export default {
  name: 'AnaylzeAll',
  components: { 
    ColorTheme,
    CTableWrapper,
    datepicker 
  },
  data() {
    return {
      isLoading: false,
      transactionGainersData: [],
      transactionLosersData: [],
      rawData: [],
    };
  },
  methods: {
    async updateDate(date) {
      this.isLoading = true;
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);
      this.transactionGainersData = [];
      this.rawData = [];
      
      await Promise.all([
        this.updateGainers(cleanDate),
        this.updateLosers(cleanDate)
      ]);
    
      this.isLoading = false;
    },
    async updateGainers(date) {
      const transactionGainersItems = await axios.get('http://localhost:5000/api/gainers/' + date);

      await Promise.all(transactionGainersItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/gainers/ticker/' + trans_item.transaction_id);

        this.transactionGainersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article,
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date,
          'status': 'success'
        });
      }));
    },
    async updateLosers(date) {
      const transactionLoserItems = await axios.get('http://localhost:5000/api/losers/' + date);

      await Promise.all(transactionLoserItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/losers/ticker/' + trans_item.transaction_id);
        
        this.transactionLosersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article,
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date,
          'status': 'success'
        });
      }));
    }
  }
};
</script>

<style scoped>
#loader {
  transform: rotateZ(90deg);
  position: absolute;
  left: 100px;
  right: 0;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  height: 400px;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>