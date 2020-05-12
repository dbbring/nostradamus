var chartMixin = {
  methods: {
    filteredDataset(Dataset) {
      let data = null;
      /* eslint-disable indent */
      switch (Dataset) {
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
  }
};

export default chartMixin;
