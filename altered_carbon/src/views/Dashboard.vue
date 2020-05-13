<template>
  <div>
    <CRow>
      <CCol
        sm="6"
        lg="3">
        <CWidgetDropdown
          color="primary"
          header="9.823"
          text="Members online">
          <template #default>
            <CDropdown
              color="transparent p-0"
              placement="bottom-end">
              <template #toggler-content>
                <CIcon name="cil-settings" />
              </template>
              <CDropdownItem>Action</CDropdownItem>
              <CDropdownItem>Another action</CDropdownItem>
              <CDropdownItem>Something else here...</CDropdownItem>
              <CDropdownItem disabled>
                Disabled action
              </CDropdownItem>
            </CDropdown>
          </template>
          <template #footer>
            <CChartLineSimple
              pointed
              class="mt-3 mx-3"
              style="height:70px"
              :data-points="[65, 59, 84, 84, 51, 55, 40]"
              point-hover-background-color="primary"
              label="Members"
              labels="months" />
          </template>
        </CWidgetDropdown>
      </CCol>
      <CCol
        sm="6"
        lg="3">
        <CWidgetDropdown
          color="info"
          header="9.823"
          text="Members online">
          <template #default>
            <CDropdown
              color="transparent p-0"
              placement="bottom-end"
              :caret="false">
              <template #toggler-content>
                <CIcon name="cil-location-pin" />
              </template>
              <CDropdownItem>Action</CDropdownItem>
              <CDropdownItem>Another action</CDropdownItem>
              <CDropdownItem>Something else here...</CDropdownItem>
              <CDropdownItem disabled>
                Disabled action
              </CDropdownItem>
            </CDropdown>
          </template>
          <template #footer>
            <CChartLineSimple
              pointed
              class="mt-3 mx-3"
              style="height:70px"
              :data-points="[1, 18, 9, 17, 34, 22, 11]"
              point-hover-background-color="info"
              :options="{ elements: { line: { tension: 0.00001 }}}"
              label="Members"
              labels="months" />
          </template>
        </CWidgetDropdown>
      </CCol>
      <CCol
        sm="6"
        lg="3">
        <CWidgetDropdown
          color="warning"
          header="9.823"
          text="Members online">
          <template #default>
            <CDropdown
              color="transparent p-0"
              placement="bottom-end">
              <template #toggler-content>
                <CIcon name="cil-settings" />
              </template>
              <CDropdownItem>Action</CDropdownItem>
              <CDropdownItem>Another action</CDropdownItem>
              <CDropdownItem>Something else here...</CDropdownItem>
              <CDropdownItem disabled>
                Disabled action
              </CDropdownItem>
            </CDropdown>
          </template>
          <template #footer>
            <CChartLineSimple
              class="mt-3"
              style="height:70px"
              background-color="rgba(255,255,255,.2)"
              :data-points="[78, 81, 80, 45, 34, 12, 40]"
              :options="{ elements: { line: { borderWidth: 2.5 }}}"
              point-hover-background-color="warning"
              label="Members"
              labels="months" />
          </template>
        </CWidgetDropdown>
      </CCol>
      <CCol
        sm="6"
        lg="3">
        <CWidgetDropdown
          color="danger"
          header="9.823"
          text="Members online">
          <template #default>
            <CDropdown
              color="transparent p-0"
              placement="bottom-end">
              <template #toggler-content>
                <CIcon name="cil-settings" />
              </template>
              <CDropdownItem>Action</CDropdownItem>
              <CDropdownItem>Another action</CDropdownItem>
              <CDropdownItem>Something else here...</CDropdownItem>
              <CDropdownItem disabled>
                Disabled action
              </CDropdownItem>
            </CDropdown>
          </template>
          <template #footer>
            <CChartBarSimple
              class="mt-3 mx-3"
              style="height:70px"
              background-color="rgb(250, 152, 152)"
              label="Members"
              labels="months" />
          </template>
        </CWidgetDropdown>
      </CCol>
    </CRow>
    <CRow>
      <CCol md="12">
        <CCard class="bg-light text-white">
          <CCardHeader>
            Traffic &amp; Sales
          </CCardHeader>
          <CCardBody>
            <CRow>
              <CCol
                sm="12"
                lg="6">
                <CRow>
                  <CCol sm="6">
                    <CCallout color="info">
                      <small class="text-muted">New Clients</small><br>
                      <strong class="h4">9,123</strong>
                    </CCallout>
                  </CCol>
                  <CCol sm="6">
                    <CCallout color="danger">
                      <small class="text-muted">Recurring Clients</small><br>
                      <strong class="h4">22,643</strong>
                    </CCallout>
                  </CCol>
                </CRow>
                <hr class="mt-0">
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Monday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      color="info"
                      :value="34" />
                    <CProgress
                      class="progress-xs"
                      color="danger"
                      :value="78" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Tuesday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="56"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="94"
                      color="danger" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Wednesday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="12"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="67"
                      color="danger" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Thursday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="43"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="91"
                      color="danger" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Friday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="22"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="73"
                      color="danger" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Saturday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="53"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="82"
                      color="danger" />
                  </div>
                </div>
                <div class="progress-group mb-4">
                  <div class="progress-group-prepend">
                    <span class="progress-group-text">
                      Sunday
                    </span>
                  </div>
                  <div class="progress-group-bars">
                    <CProgress
                      class="progress-xs"
                      :value="9"
                      color="info" />
                    <CProgress
                      class="progress-xs"
                      :value="69"
                      color="danger" />
                  </div>
                </div>
                <div class="legend text-center">
                  <small>
                    <sup><CBadge
                      shape="pill"
                      color="info">&nbsp;</CBadge></sup>
                    New clients
                    &nbsp;&nbsp;
                    <sup><CBadge
                      shape="pill"
                      color="danger">&nbsp;</CBadge></sup>
                    Recurring clients
                  </small>
                </div>
              </CCol>
              <CCol
                sm="12"
                lg="6">
                <CRow>
                  <CCol sm="6">
                    <CCallout color="warning">
                      <small class="text-muted">Pageviews</small><br>
                      <strong class="h4">78,623</strong>
                    </CCallout>
                  </CCol>
                  <CCol sm="6">
                    <CCallout color="success">
                      <small class="text-muted">Organic</small><br>
                      <strong class="h4">49,123</strong>
                    </CCallout>
                  </CCol>
                </CRow>
                <hr class="mt-0">
                <ul class="horizontal-bars type-2">
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon
                        name="cil-user"
                        class="progress-group-icon" />
                      <span class="title">Male</span>
                      <span class="ml-auto font-weight-bold">43%</span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="43"
                        color="warning" />
                    </div>
                  </div>
                  <div class="progress-group mb-5">
                    <div class="progress-group-header">
                      <CIcon
                        name="cil-user-female"
                        class="progress-group-icon" />
                      <span class="title">Female</span>
                      <span class="ml-auto font-weight-bold">37%</span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="37"
                        color="warning" />
                    </div>
                  </div>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon
                        name="cil-globe-alt"
                        class="progress-group-icon" />
                      <span class="title">Organic Search</span>
                      <span class="ml-auto font-weight-bold">
                        191,235 <span class="text-muted small">(56%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="56"
                        color="success" />
                    </div>
                  </div>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon
                        name="cib-facebook"
                        height="17"
                        class="progress-group-icon" />
                      <span class="title">Facebook</span>
                      <span class="ml-auto font-weight-bold">
                        51,223 <span class="text-muted small">(15%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="15"
                        color="success" />
                    </div>
                  </div>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon
                        name="cib-twitter"
                        height="17"
                        class="progress-group-icon" />
                      <span class="title">Twitter</span>
                      <span class="ml-auto font-weight-bold">
                        37,564 <span class="text-muted small">(11%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="11"
                        color="success" />
                    </div>
                  </div>
                  <div class="progress-group">
                    <div class="progress-group-header">
                      <CIcon
                        name="cib-linkedin"
                        height="17"
                        class="progress-group-icon" />
                      <span class="title">LinkedIn</span>
                      <span class="ml-auto font-weight-bold">
                        27,319 <span class="text-muted small">&nbsp;(8%)</span>
                      </span>
                    </div>
                    <div class="progress-group-bars">
                      <CProgress
                        class="progress-xs"
                        :value="8"
                        color="success" />
                    </div>
                  </div>
                  <div class="divider text-center">
                    <CButton
                      color="link"
                      size="sm"
                      class="text-muted">
                      <CIcon name="cil-options" />
                    </CButton>
                  </div>
                </ul>
              </CCol>
            </CRow>
            <br>
            <CDataTable
              class="mb-0 table-outline"
              hover
              :items="tableItems"
              :fields="tableFields"
              head-color="light"
              no-sorting>
              <td
                slot="avatar"
                slot-scope="{item}"
                class="text-center">
                <div class="c-avatar">
                  <img
                    :src="item.avatar.url"
                    class="c-avatar-img"
                    alt="">
                  <span
                    class="c-avatar-status"
                    :class="`bg-${item.avatar.status || 'secondary'}`" />
                </div>
              </td>
              <td
                slot="user"
                slot-scope="{item}">
                <div>{{ item.user.name }}</div>
                <div class="small text-muted">
                  <span>
                    <template v-if="item.user.new">New</template>
                    <template v-else>Recurring</template>
                  </span> | Registered: {{ item.user.registered }}
                </div>
              </td>
              <td
                slot="country"
                slot-scope="{item}"
                class="text-center">
                <CIcon
                  :name="item.country.flag"
                  height="25" />
              </td>
              <td
                slot="usage"
                slot-scope="{item}">
                <div class="clearfix">
                  <div class="float-left">
                    <strong>{{ item.usage.value }}%</strong>
                  </div>
                  <div class="float-right">
                    <small class="text-muted">{{ item.usage.period }}</small>
                  </div>
                </div>
                <CProgress
                  v-model="item.usage.value"
                  class="progress-xs"
                  :color="color(item.usage.value)" />
              </td>
              <td
                slot="payment"
                slot-scope="{item}"
                class="text-center">
                <CIcon
                  :name="item.payment.icon"
                  height="25" />
              </td>
              <td
                slot="activity"
                slot-scope="{item}">
                <div class="small text-muted">
                  Last login
                </div>
                <strong>{{ item.activity }}</strong>
              </td>
            </CDataTable>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </div>
</template>

<script>
import axios from 'axios';

import { greenColors, redColors } from '../utils/colors';
import { largeFundAnaylsisLabels, mediumFundAnaylsisLabels, smallFundAnaylsisLabels } from '../utils/const';

export default {
  name: 'Dashboard',
  components: { 
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