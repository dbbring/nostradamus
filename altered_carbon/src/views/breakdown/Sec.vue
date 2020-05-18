<template>
  <div>
    <transition name="fade">
      <img 
        v-if="$store.state.loading"
        id="loader"
        src="img/loader.svg">
      <CCard
        v-else
        class="bg-light">
        <CCardBody>
          <CRow>
            <CCol>
              <CCard>
                <CCardBody class="bg-dark">
                  <LineChart 
                    :labels="chartLabels"
                    :data-set="filterData"
                    title="Gainers Fundamental Anaylsis" />
                </CCardBody>
              </CCard>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </transition>
  </div>
</template>

<script>
import LineChart from '../../components/LineChart';
import { secTableLabels, secLabels } from '../../utils/const';
import chartMixin from '../../mixins/mixin';

export default {
  name: 'Sec',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      Dataset: 'Both',
      tableLabels: secTableLabels,
      chartLabels: secLabels
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
          'CT Orders': (tickerItem.sec.ct_orders === null) ? '' : tickerItem.sec.ct_orders,
          '# of Mergers': tickerItem.sec.mergers.length,
          'Late Filings': (tickerItem.sec.late_filings === null) ? '' : tickerItem.sec.late_filings,
          '# of Employee Diluations': tickerItem.sec.stock_program.length,
          '# of Company Diluations': tickerItem.sec.secondary_offerings.length,
          'Total # of Diluations': (tickerItem.sec.stock_program.length + tickerItem.sec.secondary_offerings.length),
        };

        data.push(additionalData);
      });

      return data;
    }
  },
  methods: {
    fillChartData() {
      // count how many times diluated 
      // how many mergers
      // how many occurances of each form in item list
      // maybe have occraunaces in differnt chart with labels?
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