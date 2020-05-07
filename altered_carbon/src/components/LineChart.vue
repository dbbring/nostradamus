<template>
  <CCard class="bg-light">
    <CCardHeader>
      <CIcon name="cil-drop" /> {{ title }}
    </CCardHeader>
    <CCardBody>
      <CChartLine
        :datasets="transformDataSet"
        :options="defaultOptions"
        :labels="labels" />
    </CCardBody>
  </CCard>
</template>

<script>
import { CChartLine } from '@coreui/vue-chartjs';

export default {
  name: 'LineChart',
  components: {
    CChartLine
  },
  props: {
    dataSet: {
      required: true,
      type: Array
    },
    options: {
      required: false,
      type: Object,
      default: () => {}
    },
    title: {
      required: true,
      type: String
    },
    labels: {
      required: true,
      type: Array
    }
  },
  computed: {
    transformDataSet() {
      const dataObj = [];
      this.dataSet.forEach((ticker_item) => {
        const pointData = [];
        this.labels.forEach((dataKey) => {
          pointData.push(ticker_item[dataKey]);
        });

        dataObj.push({
          label: ticker_item.ticker,
          backgroundColor: 'transparent',
          borderColor: ticker_item.color,
          pointHoverBackgroundColor: ticker_item.color,
          borderWidth: 1,
          data: pointData
        });
      });
      return dataObj;
    },
    defaultOptions() {
      if (!this.options) {
        return {
          responsive: true,
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              gridLines: {
                drawOnChartArea: false
              },
              ticks: {
                autoSkip: false
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }]
          },
          elements: {
            point: {
              radius: 2,
              hitRadius: 10,
              hoverRadius: 4,
              hoverBorderWidth: 3
            }
          }
        };
      }

      return this.options;
    }
  }
};
</script>
