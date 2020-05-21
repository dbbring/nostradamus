var chartMixin = {
  computed: {
    dataset() {
      let data = null;
      /* eslint-disable indent */
      switch (this.$store.state.dataset) {
        case 'Gainers':
          data = this.$store.state.mutatableGainersData;
          break;
        case 'Losers':
          data = this.$store.state.mutatableLosersData;
          break;
        case 'Both':
          data = this.$store.state.mutatableGainersData.concat(
            this.$store.state.mutatableLosersData);
      }

      return data;
    }
  },
  methods: {
    toPercent(initialValue, newValue) {
      const difference = (newValue === initialValue) ? initialValue : newValue - initialValue;
      return (difference / initialValue) * 100;
    },
    sortedData(filteredData) {
      const groupings = [];
      let individualGroup = [];
      let currentDate = '';

      filteredData.forEach((item) => {
        if (item.date !== currentDate) {
          if (individualGroup.length) {
            groupings.push(individualGroup);
            individualGroup = [];
          }
          currentDate = item.date;
        }
        individualGroup.push(item);
      });

      return groupings;
    }
  }
};

export default chartMixin;
