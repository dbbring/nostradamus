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
            <CCol lg="12">
              <LineChart 
                :labels="lgFALabels"
                :data-set="groupData('fund_anaylsis', filterData)"
                title="Gainers Fundamental Anaylsis" />
            </CCol>
          </CRow>
          <CRow>
            <CCol lg="6">
              <LineChart 
                :labels="mdFALabels"
                :data-set="groupData('fund_anaylsis', filterData)"
                title="Gainers Fundamental Anaylsis" />
            </CCol>
            <CCol lg="6">
              <LineChart 
                :labels="smFALabels"
                :data-set="groupData('fund_anaylsis', filterData)"
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
  name: 'Charting',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      lgFALabels: largeFundAnaylsisLabels,
      mdFALabels: mediumFundAnaylsisLabels,
      smFALabels: smallFundAnaylsisLabels,
      Dataset: 'Gainers'
    };
  },
  computed: {
    filterData() {
      return this.filteredDataset(this.Dataset);
    }
  },
  methods: {
    groupData(key, tickerArray) {
      const data = [];

      tickerArray.forEach((tickerItem) => {
        const additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker
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