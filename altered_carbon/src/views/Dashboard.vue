<template>
  <div>
    <transition name="fade">
      <img 
        v-if="loading"
        id="loader"
        src="img/loader.svg">
      <div v-else>
        <CRow>
          <CCol
            sm="6"
            lg="3">
            <CWidgetDropdown
              color="primary"
              header="9.823"
              text="Members online">
              <template #default>
                <CDropdown
                  color="transparent p-0"
                  placement="bottom-end">
                  <template #toggler-content>
                    <CIcon name="cil-settings" />
                  </template>
                  <CDropdownItem>Action</CDropdownItem>
                  <CDropdownItem>Another action</CDropdownItem>
                  <CDropdownItem>Something else here...</CDropdownItem>
                  <CDropdownItem disabled>
                    Disabled action
                  </CDropdownItem>
                </CDropdown>
              </template>
              <template #footer />
            </CWidgetDropdown>
          </CCol>
          <CCol
            sm="6"
            lg="3">
            <CWidgetDropdown
              color="info"
              header="9.823"
              text="Members online">
              <template #default>
                <CDropdown
                  color="transparent p-0"
                  placement="bottom-end"
                  :caret="false">
                  <template #toggler-content>
                    <CIcon name="cil-location-pin" />
                  </template>
                  <CDropdownItem>Action</CDropdownItem>
                  <CDropdownItem>Another action</CDropdownItem>
                  <CDropdownItem>Something else here...</CDropdownItem>
                  <CDropdownItem disabled>
                    Disabled action
                  </CDropdownItem>
                </CDropdown>
              </template>
              <template #footer />
            </CWidgetDropdown>
          </CCol>
          <CCol
            sm="6"
            lg="3">
            <CWidgetDropdown
              color="warning"
              header="9.823"
              text="Members online">
              <template #default>
                <CDropdown
                  color="transparent p-0"
                  placement="bottom-end">
                  <template #toggler-content>
                    <CIcon name="cil-settings" />
                  </template>
                  <CDropdownItem>Action</CDropdownItem>
                  <CDropdownItem>Another action</CDropdownItem>
                  <CDropdownItem>Something else here...</CDropdownItem>
                  <CDropdownItem disabled>
                    Disabled action
                  </CDropdownItem>
                </CDropdown>
              </template>
              <template #footer />
            </CWidgetDropdown>
          </CCol>
          <CCol
            sm="6"
            lg="3">
            <CWidgetDropdown
              color="danger"
              header="9.823"
              text="Members online">
              <template #default>
                <CDropdown
                  color="transparent p-0"
                  placement="bottom-end">
                  <template #toggler-content>
                    <CIcon name="cil-settings" />
                  </template>
                  <CDropdownItem>Action</CDropdownItem>
                  <CDropdownItem>Another action</CDropdownItem>
                  <CDropdownItem>Something else here...</CDropdownItem>
                  <CDropdownItem disabled>
                    Disabled action
                  </CDropdownItem>
                </CDropdown>
              </template>
              <template #footer />
            </CWidgetDropdown>
          </CCol>
        </CRow>
        <CRow>
          <CCol md="12">
            <CCard class="bg-light text-white">
              <CCardHeader>
                Database Stats
              </CCardHeader>
              <CCardBody>
                <CRow>
                  <CCol
                    sm="12"
                    lg="6">
                    <CRow>
                      <CCol
                        class="mx-auto"
                        sm="6">
                        <CCallout color="success">
                          <small class="text-muted">Gainers</small><br>
                          <strong class="h4">{{ stats.data[0].total_items || 0 }}</strong>
                        </CCallout>
                      </CCol>
                    </CRow>
                    <hr class="mt-0">
                    <div
                      v-for="(dup) in stats.data[0].duplicate_items"
                      :key="dup.ticker"
                      class="progress-group mb-4">
                      <div
                        class="progress-group-prepend">
                        <span class="progress-group-text">
                          {{ `${dup.ticker} (${dup.count})` }}
                        </span>
                      </div>
                      <div class="progress-group-bars">
                        <CProgress
                          class="progress-xs"
                          color="success"
                          :value="toPercent(dup.count, topGainerOccurances)" />
                      </div>
                    </div>
                  </CCol>
                  <CCol
                    sm="12"
                    lg="6">
                    <CRow>
                      <CCol sm="6">
                        <CCallout color="warning">
                          <small class="text-muted">Total Tickers Availabe</small><br>
                          <strong class="h4">{{ totalItems }}</strong>
                        </CCallout>
                      </CCol>
                      <CCol sm="6">
                        <CCallout color="danger">
                          <small class="text-muted">Losers</small><br>
                          <strong class="h4">{{ stats.data[1].total_items || 0 }}</strong>
                        </CCallout>
                      </CCol>
                    </CRow>
                    <hr class="mt-0">
                    <ul class="horizontal-bars type-2">
                      <div
                        v-for="(dup) in stats.data[1].duplicate_items"
                        :key="dup.ticker"
                        class="progress-group mb-4">
                        <div
                          class="progress-group-prepend">
                          <span class="progress-group-text">
                            {{ `${dup.ticker} (${dup.count})` }}
                          </span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            color="danger"
                            :value="toPercent(dup.count, topLoserOccurances)" />
                        </div>
                      </div>
                    </ul>
                  </CCol>
                </CRow>
                <br>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';

import chartMixin from '../mixins/mixin';

export default {
  name: 'Dashboard',
  mixins: [chartMixin],
  data() {
    return {
      loading: true,
      stats: [],
      totalItems: null,
      topGainerOccurances: 0,
      topLoserOccurances: 0,
    };
  },
  mounted() {
    this.getStats();
  },
  methods: {
    async getStats() {
      this.loading = true;
      this.stats = await axios.get('http://localhost:5000/api/stats');
  
      this.stats.data[0].duplicate_items.forEach((dup) => {
        this.topGainerOccurances = (this.topGainerOccurances < dup.count) ? dup.count : this.topGainerOccurances;
      });

      this.stats.data[1].duplicate_items.forEach((dup) => {
        this.topLoserOccurances = (this.topLoserOccurances < dup.count) ? dup.count : this.topLoserOccurances;
      });

      this.loading = false;
    }
  }
};
</script>