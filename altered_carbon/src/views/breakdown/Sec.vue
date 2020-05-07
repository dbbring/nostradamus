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
            placeholder="Pick a Date"
            @input="updateDate" />
        </CRow>
      </CCardHeader>
      <CCardBody>
        <CRow class="text-center text-info py-2 mb-2">
          <CCol>
            <h2 v-if="$store.state.currentSelectedDate">
              {{ $store.state.currentSelectedDate | $formatDateForDisplay }}
            </h2>
          </CCol>
        </CRow>
        <CRow>
          <img 
            v-if="isLoading"
            id="loader"
            src="img/loader.svg">
          <CCol
            lg="12"
            style="min-height: 400px;">
            <transition name="fade">
              <CCard
                v-if="!isLoading"
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Gainers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ tableGainersData.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark"
                    :items="tableGainersData"
                    :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date', 'Display']"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    clickable-rows
                    sorter
                    :sorter-value="{asc: false, column: 'Percent Change'}"
                    @row-clicked="toggleDisplay">
                    <template #Ticker="{item}">
                      <td @mouseover="hoverCellTicker = item.Ticker">
                        {{ item.Ticker }}
                      </td>
                    </template>
                    <template #Display="{item}">
                      <td>
                        <CSwitch
                          :checked="item.Display"
                          class="mx-1"
                          color="success"
                          variant="3d" />
                      </td>
                    </template>
                  </CDataTable>
                </CCardBody>
              </CCard>
            </transition>
          </CCol>
          <CCol
            lg="12"
            style="min-height: 400px;">
            <transition name="fade">
              <CCard
                v-if="!isLoading"
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Losers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ tableLosersData.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark text-white"
                    :items="tableLosersData"
                    :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date', 'Display']"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    clickable-rows
                    sorter
                    :sorter-value="{asc: true, column: 'Percent Change'}"
                    @row-clicked="toggleDisplay">
                    <template #Ticker="{item}">
                      <td @mouseover="hoverCellTicker = item.Ticker">
                        {{ item.Ticker }}
                      </td>
                    </template>
                    <template #Display="{item}">
                      <td>
                        <CSwitch
                          :checked="item.Display"
                          class="mx-1"
                          color="success"
                          variant="3d" />
                      </td>
                    </template>
                  </CDataTable>
                </CCardBody>
              </CCard>
            </transition>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>
    
    <CCard v-if="!isLoading">
      <CCardBody class="bg-light">
        <CRow>
          <CCol lg="12">
            <LineChart 
              :labels="lgFALabels"
              :data-set="groupData('fund_anaylsis', gainersData)"
              title="Gainers Fundamental Anaylsis" />
          </CCol>
        </CRow>
        <CRow>
          <CCol lg="6">
            <LineChart 
              :labels="mdFALabels"
              :data-set="groupData('fund_anaylsis', gainersData)"
              title="Gainers Fundamental Anaylsis" />
          </CCol>
          <CCol lg="6">
            <LineChart 
              :labels="smFALabels"
              :data-set="groupData('fund_anaylsis', gainersData)"
              title="Gainers Fundamental Anaylsis" />
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>

    <CModal
      v-if="activeItem"
      color="primary"
      centered
      :show.sync="showModal">
      <div slot="header">
        <h5 class="modal-title text-center">
          {{ `News and SEC For ${activeItem.basic_info.ticker}` }}
        </h5>
      </div>
      News component goes here

      SEC componet goes here
      <div slot="footer">
        <CButton
          color="primary"
          @click="showModal = false">
          OK
        </CButton>
      </div>
    </CModal>
  </div>
</template>

<script>
import axios from 'axios';
import datepicker from 'vuejs-datepicker';
import LineChart from '../../components/LineChart';

import { greenColors, redColors } from '../../utils/colors';
import { largeFundAnaylsisLabels, mediumFundAnaylsisLabels, smallFundAnaylsisLabels } from '../../utils/const';

export default {
  name: 'Sec',
  components: { 
    LineChart,
    datepicker 
  },
  data() {
    return {
      activeItem: null,
      isLoading: false,
      tableGainersData: [],
      tableLosersData: [],
      gainersData: [],
      gainersRawData: [],
      losersData: [],
      losersRawData: [],
      hoverCellTicker: null,
      showModal: false,
      lgFALabels: largeFundAnaylsisLabels,
      mdFALabels: mediumFundAnaylsisLabels,
      smFALabels: smallFundAnaylsisLabels,
    };
  },
  methods: {
    groupData(key, tickerArray) {
      const data = [];

      tickerArray.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.color,
          ticker: tickerItem.basic_info.ticker
        };
        data.push({...tickerItem[key], ...additionalData});
      });

      return data;
    },
    setModalDataItem(item) {
      this.activeItem = null;

      if (item.category === 'Gainers') {
        this.activeItem = this.gainersData.filter(fullDataItem => fullDataItem.basic_info.ticker === item.Ticker);
      } else {
        this.activeItem = this.losersData.filter(fullDataItem => fullDataItem.basic_info.ticker === item.Ticker);
      }

      if (this.activeItem.length) {
        this.activeItem = this.activeItem[0];
      }
      return;
    },
    async updateDate(date) {
      this.isLoading = true;
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);

      this.tableGainersData = [];
      this.tableLosersData = [];
      this.gainersData = [];
      this.losersData = [];
      this.gainersRawData = [];
      this.losersRawData = [];
      
      await Promise.all([
        this.updateGainers(cleanDate),
        this.updateLosers(cleanDate)
      ]);
    
      this.isLoading = false;
    },
    async updateGainers(date) {
      let counter = 0;

      const transactionGainersItems = await axios.get('http://localhost:5000/api/gainers/' + date);

      await Promise.all(transactionGainersItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/gainers/ticker/' + trans_item.transaction_id);
        const additionalData = {
          'color': greenColors[counter],
          'category': 'Gainers'
        };

        const combinedData = {...additionalData, ...details.data};

        this.gainersData.push(combinedData);
        this.gainersRawData.push(combinedData);

        this.tableGainersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article || '',
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
          'Display': true,
          'id': details.data.basic_info.transaction_id,
          'category': 'Gainers',
          '_classes': `text-green-${counter}`,
        });

        counter++;
      }));
    },
    async updateLosers(date) {
      let counter = 0;

      const transactionLoserItems = await axios.get('http://localhost:5000/api/losers/' + date);

      await Promise.all(transactionLoserItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/losers/ticker/' + trans_item.transaction_id);
        
        this.losersData.push(details.data);
        this.losersRawData.push(details.data);


        this.tableLosersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article || '',
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
          'Display': true,
          'id': details.data.basic_info.transaction_id,
          'category': 'Losers',
          'color': redColors[counter],
          '_classes': `text-red-${counter}`,
        });

        counter++;
      }));
    },
    toggleDisplay(tableItem) {
      if (this.hoverCellTicker === tableItem.Ticker) {
        this.setModalDataItem(tableItem);
        this.showModal = true;
        this.hoverCellTicker = null;
        return;
      } 

      tableItem.Display = !tableItem.Display;
      
      if (tableItem.category === 'Gainers') {
        this.gainersData = this.toggleChartDisplay(tableItem, this.gainersData, this.gainersRawData);
      } else {
        this.losersData = this.toggleChartDisplay(tableItem, this.losersData, this.losersRawData);
      }
      return;
    },
    toggleChartDisplay(tableItem, mutatableArray, immutableArray) {
      if (tableItem.Display) {
        const addItem = immutableArray.filter(ticker_item => ticker_item.basic_info.ticker === tableItem.Ticker);

        if (addItem.length) {
          mutatableArray.push(addItem[0]);
        }
        return mutatableArray;
      }
      
      return mutatableArray.filter(ticker_item => ticker_item.basic_info.ticker !== tableItem.Ticker );
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