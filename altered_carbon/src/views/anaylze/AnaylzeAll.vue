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
            <CCol
              lg="12"
              style="min-height: 400px;">
              <CCard
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Gainers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ gainersTableInfo.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark"
                    :items="gainersTableInfo"
                    :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date', 'Display']"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    clickable-rows
                    sorter
                    :sorter-value="{asc: false, column: 'Percent Change'}"
                    @row-clicked="toggleDisplay">
                    <template #Ticker="{item}">
                      <td @mouseover="hoverCellTicker = item.Ticker">
                        {{ item.Ticker }}
                      </td>
                    </template>
                    <template #Display="{item}">
                      <td>
                        <CSwitch
                          :checked="item.Display"
                          class="mx-1"
                          color="success"
                          variant="3d" />
                      </td>
                    </template>
                  </CDataTable>
                </CCardBody>
              </CCard>
            </CCol>
            <CCol
              lg="12"
              style="min-height: 400px;">
              <CCard
                class="bg-dark">
                <CCardHeader>
                  <CIcon name="cil-grid" /> Losers
                  <div class="card-header-actions">
                    <small class="text-muted">{{ losersTableInfo.length }}</small>
                  </div>
                </CCardHeader>
                <CCardBody>
                  <CDataTable
                    class="bg-dark border-dark text-white"
                    :items="losersTableInfo"
                    :fields="['Ticker', 'Last News Article', 'Percent Change', 'Earnings Date', 'Display']"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    clickable-rows
                    sorter
                    :sorter-value="{asc: true, column: 'Percent Change'}"
                    @row-clicked="toggleDisplay">
                    <template #Display="{item}">
                      <td>
                        <CSwitch
                          :checked="item.Display"
                          class="mx-1"
                          color="success"
                          variant="3d" />
                      </td>
                    </template>
                  </CDataTable>
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
export default {
  name: 'AnaylzeAll',
  computed: {
    gainersTableInfo() {
      return this.$store.state.immutatableGainersData.map(tickerItem => tickerItem.table_info);
    },
    losersTableInfo() {
      return this.$store.state.immutatableLosersData.map(tickerItem => tickerItem.table_info);
    }
  },
  methods: {
    toggleDisplay(tableItem) {
      tableItem.Display = !tableItem.Display;
      this.$store.commit('toggleChartDisplay', tableItem);
      return;
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