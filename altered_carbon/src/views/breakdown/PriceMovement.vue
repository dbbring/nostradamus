<template>
  <div>
    <transition name="fade">
      <img 
        v-if="$store.state.loading"
        id="loader"
        src="img/loader.svg">
      <div v-else>
        <CCard style="min-height:800px;">
          <CCardHeader class="bg-light">
            <CRow>
              <h2 class="text-white mx-auto">
                EOD Stats
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark">
            <CRow>
              <CCol>
                <CTabs 
                  fill>
                  <CTab
                    title="Percent Change"
                    active>
                    <LineChart 
                      :labels="[eodChartLabel[0]]"
                      :data-set="sortedData(filterData('eod'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                  <CTab title="Volume Change">
                    <LineChart 
                      :labels="[eodChartLabel[1]]"
                      :data-set="sortedData(filterData('eod'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                  <CTab title="Price Change">
                    <LineChart 
                      :labels="[eodChartLabel[2]]"
                      :data-set="sortedData(filterData('eod'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                </CTabs>
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
        <CCard style="min-height:800px;">
          <CCardHeader class="bg-light">
            <CRow>
              <h2 class="text-white mx-auto">
                Weekly Stats
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark">
            <CRow>
              <CCol>
                <CTabs 
                  fill>
                  <CTab
                    title="Percent Change"
                    active>
                    <LineChart 
                      :labels="[wkChartLabel[0]]"
                      :data-set="sortedData(filterData('weekly'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                  <CTab title="Volume Change">
                    <LineChart 
                      :labels="[wkChartLabel[1]]"
                      :data-set="sortedData(filterData('weekly'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                  <CTab title="Price Change">
                    <LineChart 
                      :labels="[wkChartLabel[2]]"
                      :data-set="sortedData(filterData('weekly'))"
                      title="Gainers Fundamental Anaylsis" />
                  </CTab>
                </CTabs>
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
        <CCard>
          <CCardBody 
            v-for="(eodArray, index) in sortedData(filterData('eod'))"
            :key="`${index}`"
            class="bg-dark">
            <CCardHeader class="bg-light text-center">
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
import LineChart from '../../components/LineChart';
import chartMixin from '../../mixins/mixin';

import { eodPriceActionLabels, wkPriceActionLabels, largeTechAnaylsisLabels, mediumTechAnaylsisLabels, smallTechAnaylsisLabels, chartAnaylsisLabels } from '../../utils/const';

export default {
  name: 'PriceMovement',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      chartLabels: chartAnaylsisLabels,
      priceActionLabels: eodPriceActionLabels,
      eodChartLabel: eodPriceActionLabels,
      wkChartLabel: wkPriceActionLabels,
      lgTALabels: largeTechAnaylsisLabels,
      mdTALabels: mediumTechAnaylsisLabels,
      smTALabels: smallTechAnaylsisLabels,
      Dataset: 'Both',
    };
  },
  methods: {
    filterData(key) {
      const data = [];
      const dataArray = this.filteredDataset(this.Dataset);

      dataArray.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker
        };

        tickerItem[key].forEach((item) => {
          data.push({...item, ...additionalData});
        });
      });

      data.sort((a,b) => {
        const firstDate = new Date(a.date);
        const secondDate = new Date(b.date);
        return firstDate - secondDate;
      });
      return data;
    },
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