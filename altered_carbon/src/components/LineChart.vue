<template>
  <CCard class="bg-light">
    <CCardHeader>
      <CIcon name="cil-drop" /> {{ title }}
    </CCardHeader>
    <CCardBody>
      <CChartLine
        :datasets="transformDataSet"
        :options="defaultOptions"
        :labels="labelProxy" />
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
      default: '',
      required: false,
      type: String
    },
    labels: {
      required: true,
      type: Array
    }
  },
  data() {
    return {
      labelProxy: this.labels
    };
  },
  computed: {
    transformDataSet() {
      const dataObj = [];

      if (Array.isArray(this.dataSet[0])) {
        return this.handleNestedArray();
      }

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
  },
  methods: {
    handleNestedArray() {
      const dataObj = [];
      const modLabels = [];

      this.dataSet.forEach((arrayItem) => {
        this.labels.forEach((_label) => {
          modLabels.push(`${arrayItem[0].date}-${_label}`);
        });
      });

      this.dataSet[0].forEach((item) => {
        this.labels.forEach((lbl) => { 
          dataObj.push({
            label: item.ticker,
            backgroundColor: 'transparent',
            borderColor: item.color,
            pointHoverBackgroundColor: item.color,
            borderWidth: 1,
            data: this.getPointData(item.ticker, lbl)
          });
        });
      });
      
      

      this.labelProxy = modLabels;
      return dataObj;
    },
    getPointData(ticker, key) {
      const results = [];

      this.dataSet.forEach((arrayItem) => {
        arrayItem.forEach((item) => {
          if (item.ticker === ticker) {
            results.push(item[key]);
          }
        });
      });

      return results;
    }
  }
};
</script>
