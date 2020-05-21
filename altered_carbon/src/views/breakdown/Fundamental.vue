<template>
  <div>
    <transition name="fade">
      <img 
        v-if="$store.state.loading"
        id="loader"
        src="img/loader.svg">
      <CCard v-else>
        <CCardBody class="bg-light">
          <CRow>
            <CCol>
              <LineChart 
                :labels="lgFALabels"
                :data-set="filterData"
                title="Gainers Fundamental Anaylsis" />
            </CCol>
          </CRow>
          <CRow>
            <CCol>
              <LineChart 
                :labels="mdFALabels"
                :data-set="filterData"
                title="Gainers Fundamental Anaylsis" />
            </CCol>
          </CRow>
          <CRow>
            <CCol>
              <LineChart 
                :labels="smFALabels"
                :data-set="filterData"
                title="Gainers Fundamental Anaylsis" />
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </transition>
  </div>
</template>

<script>
import LineChart from '../../components/LineChart';
import chartMixin from '../../mixins/mixin';

import { largeFundAnaylsisLabels, mediumFundAnaylsisLabels, smallFundAnaylsisLabels } from '../../utils/const';

export default {
  name: 'Fundamental',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      lgFALabels: largeFundAnaylsisLabels,
      mdFALabels: mediumFundAnaylsisLabels,
      smFALabels: smallFundAnaylsisLabels
    };
  },
  computed: {
    filterData() {
      const data = [];
      this.dataset.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker
        };

        data.push({...tickerItem['fund_anaylsis'], ...additionalData});
      });

      return data;
    }
  }
};
</script>
