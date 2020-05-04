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
          <CCol lg="6">
            <CTableWrapper 
              class="bg-dark"
              :items="transactionData"
              :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date']">
              <template #header>
                <CIcon name="cil-grid" /> Gainers
                <div class="card-header-actions">
                  <small class="text-muted">{{ transactionData.length }}</small>
                </div>
              </template>
            </CTableWrapper>
          </CCol>

          <CCol lg="6">
            <CTableWrapper
              striped
              caption="Striped Table" />
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
      transactionData: [],
      rawData: []
    };
  },
  methods: {
    updateDate(date) {
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);
      this.transactionData = [];
      this.rawData = [];

      axios.get('http://localhost:5000/api/gainers/' + cleanDate).then((response) => {
        response.data.forEach((item) => {
          axios.get('http://localhost:5000/api/gainers/ticker/' + item.transaction_id).then((ticker_detail) => {
            this.rawData.push(ticker_detail.data);
            // console.log(this.rawData);
            const temp = {
              'Ticker': ticker_detail.data.basic_info.ticker,
              'Last News Article': ticker_detail.data.news[0].date_of_article,
              'Percent Change': ticker_detail.data.basic_info.percent_change,
              'Earnings Date': ticker_detail.data.fund_anaylsis.earnings_date,
              'status': 'success'
            };
            console.log(temp);
            this.transactionData.push(temp);
          });
        });
      });
    }
  }
};
</script>
