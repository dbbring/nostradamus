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
            lg="6"
            style="min-height: 400px;">
            <transition name="fade">
              <CCard
                v-if="!isLoading"
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Gainers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ transactionGainersData.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark"
                    :items="transactionGainersData"
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
            lg="6"
            style="min-height: 400px;">
            <transition name="fade">
              <CCard
                v-if="!isLoading"
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Losers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ transactionLosersData.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark text-white"
                    :items="transactionLosersData"
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
import ColorTheme from './ColorTheme';
import datepicker from 'vuejs-datepicker';
import { greenColors, redColors } from '../../utils/colors';

export default {
  name: 'AnaylzeAll',
  components: { 
    ColorTheme,
    datepicker 
  },
  data() {
    return {
      activeItem: null,
      isLoading: false,
      transactionGainersData: [],
      transactionLosersData: [],
      gainersData: [],
      losersData: [],
      hoverCellTicker: null,
      showModal: false
    };
  },
  methods: {
    async updateDate(date) {
      this.isLoading = true;
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);
      this.transactionGainersData = [];
      this.transactionLosersData = [];
      this.gainersData = [];
      this.losersData = [];
      
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

        this.gainersData.push(details.data);
        this.transactionGainersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article || '',
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
          'Display': true,
          'id': details.data.basic_info.transaction_id,
          'category': 'Gainers',
          'color': greenColors[counter],
          '_classes': 'text-white',
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
        this.transactionLosersData.push({
          'Ticker': details.data.basic_info.ticker,
          'Last News Article': details.data.news[0].date_of_article || '',
          'Percent Change': details.data.basic_info.percent_change,
          'Earnings Date': details.data.fund_anaylsis.earnings_date || '',
          'Display': true,
          'id': details.data.basic_info.transaction_id,
          'category': 'Losers',
          'color': redColors[counter],
          '_classes': 'text-white',
        });
        counter++;
      }));
    },
    debug(msg) {
      console.log(msg);
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
    toggleDisplay(item) {
      if (this.hoverCellTicker === item.Ticker) {
        this.setModalDataItem(item);
        this.showModal = true;
        this.hoverCellTicker = null;
        return;
      } 

      item.Display = !item.Display;
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