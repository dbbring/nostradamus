<template>
  <div>
    <transition name="fade">
      <img 
        v-if="$store.state.loading"
        id="loader"
        src="img/loader.svg">
      <div v-else>
        <CCard
          v-if="noData"
          class="bg-light">
          <CCardHeader class="bg-light">
            <CRow>
              <h2 class="text-white mx-auto">
                No Data Tard. Hasnt Been 5 Days.
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark mx-auto p-5 m-5">
            <img src="img/giphy.gif">
          </CCardBody>
        </CCard>
        <CCard
          v-else
          style="min-height:800px;">
          <CCardHeader class="bg-light">
            <CRow>
              <h2 class="text-white mx-auto">
                Performance Over The Following Week
              </h2>
            </CRow>
          </CCardHeader>
          <CCardBody class="bg-dark">
            <LineChart 
              :labels="['percent_change']"
              :data-set="sortedData(filterData('future_prices'))"
              title="Gainers Fundamental Anaylsis" />
          </CCardBody>
        </CCard>
      </div>
    </transition>
  </div>
</template>

<script>
import LineChart from '../../components/LineChart';
import chartMixin from '../../mixins/mixin';

export default {
  name: 'FuturePriceAction',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      noData: false
    };
  },
  mounted() {
    let wkAgo = new Date();
    wkAgo.setDate(wkAgo.getDate() - 7);

    if (this.$store.state.currentSelectedDate > wkAgo) {
      this.noData = true;
    }
  },
  methods: {
    filterData(key) {
      const data = [];
      this.dataset.forEach((tickerItem) => {
        if (!tickerItem[key]) {
          return;
        }

        const additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker,
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
    }
  }
};
</script>
