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
            <CCol lg="12">
              <CCard>
                <CCardBody class="bg-dark">
                  <LineChart 
                    :labels="chartLabels"
                    :data-set="filterData"
                    title="Gainers Fundamental Anaylsis" />
                </CCardBody>
              </CCard>
            </CCol>
            <CCol lg="12">
              <CCard>
                <CCardBody class="bg-dark">
                  <LineChart 
                    :labels="sectorChartLabels"
                    :data-set="filterData"
                    title="Gainers Fundamental Anaylsis" />
                </CCardBody>
              </CCard>
            </CCol>
            <CCol>
              <CTabs 
                fill>
                <!-- use v for here to dynamically add tabs? -->
                <CTab
                  title="Vs DJI"
                  active>
                  <LineChart 
                    :labels="[peersAndSectorsLabels[0]]"
                    :data-set="sortedData(peersAndSectors)"
                    title="Gainers Fundamental Anaylsis" />
                </CTab>
                <CTab title="Vs Nasdaq">
                  <LineChart 
                    :labels="[peersAndSectorsLabels[1]]"
                    :data-set="sortedData(peersAndSectors)"
                    title="Gainers Fundamental Anaylsis" />
                </CTab>
                <CTab title="Vs SP">
                  <LineChart 
                    :labels="[peersAndSectorsLabels[2]]"
                    :data-set="sortedData(peersAndSectors)"
                    title="Gainers Fundamental Anaylsis" />
                </CTab>
              </CTabs>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </transition>
  </div>
</template>

<script>
import LineChart from '../../components/LineChart';
import { overviewLabels, overviewSectorHistoricLabels, overviewSectorLabels } from '../../utils/const';
import chartMixin from '../../mixins/mixin';

export default {
  name: 'Overview',
  components: { 
    LineChart
  },
  mixins: [chartMixin],
  data() {
    return {
      Dataset: 'Both',
      chartLabels: overviewLabels,
      sectorChartLabels: overviewSectorHistoricLabels,
      peersAndSectorsLabels: overviewSectorLabels,
      peersAndSectors: [],
    };
  },
  computed: {
    filterData() {
      // price performance over past 5 days vs peer performance over last 5 days 
      // corrlation between vix? do we need pearson corrlection endpoint?
      // price diff vs each indicie? which would include top level sector if not avail
      // ======
      // then show little widgets for each company (background the same green for each card) that hold all news titles which we can link out
      const data = [];
      const today = new Date();
      const dataArray = this.filteredDataset(this.Dataset);

      dataArray.forEach((tickerItem) => {
        this.peersAndSectors.concat(this.filterPeerAndSectorPerformance(tickerItem));
        const co_age = (tickerItem.sec.date_of_ipo) ? 
          ((today - new Date(tickerItem.sec.date_of_ipo)) / 31536000000).toFixed(0) : 
          -1;
        
        let additionalData = {
          color: tickerItem.table_info.color,
          ticker: tickerItem.basic_info.ticker,
          'Company Age': co_age,
          'Total News Articles': tickerItem.news.length
        };

        this.filterSectorHistoricPerformance(tickerItem).forEach((sectorObj) => {
          additionalData = {...additionalData, ...sectorObj};
        });


        data.push(additionalData);
      });

      return data;
    }
  },
  methods: {
    filterPeerAndSectorPerformance(tickerItem) {
      // if peer is above .80 cents
      // if peer around the same price? so like 1 to 10 bucks?
      // 10 -50? 50 ^
      // avg the peers out and show the ticker % change vs avg change
      // need LABELSSSS
      const sectors = tickerItem.sector_performance.map((sectorItem) => {
        const addData = {
          ticker: tickerItem.basic_info.ticker,
        };
        return {...sectorItem, ...addData};
      });

      sectors.sort((a,b) => {
        const firstDate = new Date(a.date);
        const secondDate = new Date(b.date);
        return firstDate - secondDate;
      });

      return sectors;
    },
    filterSectorHistoricPerformance(tickerItem) {
      const data = [];
      Object.keys(tickerItem.sector_historic_performance).forEach((sectorTimeInteveral) => {
        const label = 'sector_' + sectorTimeInteveral;

        Object.keys(tickerItem.sector_historic_performance[sectorTimeInteveral]).forEach((sector) => {
          let sect_change = tickerItem.sector_historic_performance[sectorTimeInteveral][sector];
          sect_change = parseFloat(sect_change.replace('%', ''));
          const tick_change = tickerItem.eod[1].percent_change;

          const sectorData = {
            // Sector change as a percentage of the total gained by ticker
            [label]: (sect_change * tick_change)
          };

          data.push(sectorData);
        });
      });

      return data;
    },
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