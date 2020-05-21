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
                    v-for="(eodStatLabel, index) in eodChartLabel"
                    :key="index"
                    :title="formatTitle(eodStatLabel)">
                    <LineChart 
                      :labels="[eodStatLabel]"
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
                    v-for="(wkStatLabel, index) in wkChartLabel"
                    :key="index"
                    :title="formatTitle(wkStatLabel)">
                    <LineChart 
                      :labels="[wkStatLabel]"
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
            :key="index"
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
    };
  },
  methods: {
    filterData(key) {
      const data = [];

      this.dataset.forEach((tickerItem) => {
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
    formatTitle(titleStr) {
      let formatted = titleStr.charAt(0).toUpperCase() + titleStr.slice(1);
      formatted = formatted.replace(/_/gi, ' ');
      return formatted;
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
