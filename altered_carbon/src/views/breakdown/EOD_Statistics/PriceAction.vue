<template>
  <div>
    <transition name="fade">
      <img 
        v-if="$store.state.loading"
        id="loader"
        src="img/loader.svg">
      <div v-else>
        <CCard>
          <CCardHeader class="bg-light text-center">
            <CRow>
              <CSwitch
                :checked.sync="eodPercentChangeDisplay"
                class="mx-1 ml-4"
                color="info"
                label-on="%"
                label-off="%"
                size="lg" />
              <CSwitch
                :checked.sync="eodVolumeDiffDisplay"
                class="mx-1"
                color="info"
                label-on="Vol"
                label-off="Vol"
                size="lg" />
              <CSwitch
                :checked.sync="eodPriceDiffDisplay"
                class="mx-1"
                color="info"
                label-on="$"
                label-off="$"
                size="lg" />
              <h2 class="text-white">
                EOD Stats
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark">
            <CRow>
              <CCol>
                <LineChart 
                  :labels="[eodChartLabel]"
                  :data-set="sortedData"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
        <CCard>
          <CCardHeader class="bg-light text-center">
            <CRow>
              <CSwitch
                :checked.sync="wkPercentChangeDisplay"
                class="mx-1 ml-4"
                color="info"
                label-on="%"
                label-off="%"
                size="lg" />
              <CSwitch
                :checked.sync="wkVolumeDiffDisplay"
                class="mx-1"
                color="info"
                label-on="Vol"
                label-off="Vol"
                size="lg" />
              <CSwitch
                :checked.sync="wkPriceDiffDisplay"
                class="mx-1"
                color="info"
                label-on="$"
                label-off="$"
                size="lg" />
              <h2 class="text-white">
                Weekly Stats
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark">
            <CRow>
              <CCol>
                <LineChart 
                  :labels="[wkChartLabel]"
                  :data-set="sortedData"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
        <CCard>
          <CCardBody 
            v-for="(eodArray, index) in sortedData"
            :key="`${index}`"
            class="bg-dark">
            <CCardHeader class="text-center">
              <h1 class="text-white">
                {{ eodArray[0].date | $formatDateForDisplay }}
              </h1>
            </CCardHeader> 
            <CRow>
              <CCol>
                <LineChart 
                  :labels="chartLabels"
                  :data-set="groupData('charting', eodArray)"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
            </CRow>
            <CRow>
              <CCol>
                <LineChart 
                  :labels="smTALabels"
                  :data-set="groupData('technical', eodArray)"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
            </CRow>
            <CRow>
              <CCol lg="6">
                <LineChart 
                  :labels="mdTALabels"
                  :data-set="groupData('technical', eodArray)"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
              <CCol lg="6">
                <LineChart 
                  :labels="lgTALabels"
                  :data-set="groupData('technical', eodArray)"
                  title="Gainers Fundamental Anaylsis" />
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
      </div>
    </transition>
  </div>
</template>

<script>
import LineChart from '../../../components/LineChart';
import chartMixin from '../../../mixins/mixin';

import { eodPriceActionLabels, wkPriceActionLabels, largeTechAnaylsisLabels, mediumTechAnaylsisLabels, smallTechAnaylsisLabels, chartAnaylsisLabels } from '../../../utils/const';

export default {
  name: 'PriceAction',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      chartLabels: chartAnaylsisLabels,
      priceActionLabels: eodPriceActionLabels,
      eodChartLabel: eodPriceActionLabels[0],
      wkChartLabel: wkPriceActionLabels[0],
      lgTALabels: largeTechAnaylsisLabels,
      mdTALabels: mediumTechAnaylsisLabels,
      smTALabels: smallTechAnaylsisLabels,
      Dataset: 'Gainers',
      eodPercentChangeDisplay: true,
      eodVolumeDiffDisplay: false,
      eodPriceDiffDisplay: false,
      wkPercentChangeDisplay: true,
      wkVolumeDiffDisplay: false,
      wkPriceDiffDisplay: false
    };
  },
  computed: {
    filterData() {
      const data = [];
      const dataArray = this.filteredDataset(this.Dataset);

      dataArray.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker,
          vol_diff_from_avg: 3.0,
          price_diff_open_to_low: 6
        };

        tickerItem['eod'].forEach((eodItem) => {
          data.push({...eodItem, ...additionalData});
        });
      });

      data.sort((a,b) => {
        const firstDate = new Date(a.date);
        const secondDate = new Date(b.date);
        return firstDate - secondDate;
      });
      return data;
    },
    sortedData() {
      const groupings = [];
      let individualGroup = [];
      let currentDate = '';
      
      this.filterData.forEach((eodItem) => {
        if (eodItem.date !== currentDate) {
          if (individualGroup.length) {
            groupings.push(individualGroup);
            individualGroup = [];
          }
          
          currentDate = eodItem.date;
        }
        
        individualGroup.push(eodItem);
      });

      return groupings;
    }
  },
  watch: {
    eodPercentChangeDisplay: function (val) {
      if (val) this.toggleOverallChart(0);
    },
    eodVolumeDiffDisplay: function (val) {
      if (val) this.toggleOverallChart(1);
    },
    eodPriceDiffDisplay: function (val) {
      if (val) this.toggleOverallChart(2);
    },
    wkPercentChangeDisplay: function (val) {
      if (val) this.toggleWkOverallChart(0);
    },
    wkVolumeDiffDisplay: function (val) {
      if (val) this.toggleWkOverallChart(1);
    },
    wkPriceDiffDisplay: function (val) {
      if (val) this.toggleWkOverallChart(2);
    }
  },
  methods: {
    groupData(key, array) {
      const data = [];

      array.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.color,
          ticker: tickerItem.ticker
        };
        data.push({...tickerItem[key], ...additionalData});
      });

      return data;
    },
    toggleOverallChart(constLabelIndex) {
      this.eodPercentChangeDisplay = false;
      this.eodVolumeDiffDisplay = false;
      this.eodPriceDiffDisplay = false;

      this.eodChartLabel = this.eodPriceActionLabels[constLabelIndex];

      switch(constLabelIndex) {
      case 0:
        this.eodPercentChangeDisplay = true;
        break;
      case 1:
        this.eodVolumeDiffDisplay = true;
        break;
      case 2:
        this.eodPriceDiffDisplay = true;
        break;
      }
    },
    toggleWkOverallChart(constLabelIndex) {
      this.wkPercentChangeDisplay = false;
      this.wkVolumeDiffDisplay = false;
      this.wkPriceDiffDisplay = false;

      this.wkChartLabel = this.wkPriceActionLabels[constLabelIndex];

      switch(constLabelIndex) {
      case 0:
        this.wkPercentChangeDisplay = true;
        break;
      case 1:
        this.wkVolumeDiffDisplay = true;
        break;
      case 2:
        this.wkPriceDiffDisplay = true;
        break;
      }
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