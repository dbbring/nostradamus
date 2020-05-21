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
              lg="12">
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
                    :fields="tableLabels"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    sorter
                    :sorter-value="{asc: false, column: 'Percent Change'}" />
                </CCardBody>
              </CCard>
            </CCol>
            <CCol
              lg="12">
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
                    :fields="tableLabels"
                    :items-per-page="8"
                    border
                    pagination
                    hover
                    sorter
                    :sorter-value="{asc: true, column: 'Percent Change'}" />
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
import { tableInfoLabels } from '../../utils/const';

export default {
  name: 'AnaylzeAll',
  data() {
    return {
      tableLabels: tableInfoLabels
    };
  },
  computed: {
    gainersTableInfo() {
      return this.$store.state.mutatableGainersData.map((tickerItem) => {
        const additionalData = {
          'Ticker': tickerItem.basic_info.ticker,
          'Last News Article': tickerItem.news[0].date_of_article || '',
          'Percent Change': tickerItem.basic_info.percent_change,
          'Earnings Date': tickerItem.fund_anaylsis.earnings_date || '',
          'Date of IPO': (tickerItem.sec.date_of_ipo === null) ? '' : tickerItem.sec.date_of_ipo,
          'ADR': (tickerItem.sec.is_adr) ? 'Yes' : 'No',
        };
        return {...tickerItem.table_info, ...additionalData};
      });
    },
    losersTableInfo() {
      return this.$store.state.mutatableLosersData.map((tickerItem) => {
        const additionalData = {
          'Ticker': tickerItem.basic_info.ticker,
          'Last News Article': tickerItem.news[0].date_of_article || '',
          'Percent Change': tickerItem.basic_info.percent_change,
          'Earnings Date': tickerItem.fund_anaylsis.earnings_date || '',
          'Date of IPO': (tickerItem.sec.date_of_ipo === null) ? '' : tickerItem.sec.date_of_ipo,
          'ADR': (tickerItem.sec.is_adr) ? 'Yes' : 'No',
        };
        return {...tickerItem.table_info, ...additionalData};
      });
    }
  }
};
</script>
