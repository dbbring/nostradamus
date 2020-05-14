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
                      <CCol sm="6">
                        <CCallout color="success">
                          <small class="text-muted">Gainers</small><br>
                          <strong class="h4">{{ stats[0].total_items || 0 }}</strong>
                        </CCallout>
                      </CCol>
                      <CCol sm="6">
                        <CCallout color="danger">
                          <small class="text-muted">Losers</small><br>
                          <strong class="h4">{{ stats[1].total_items || 0 }}</strong>
                        </CCallout>
                      </CCol>
                    </CRow>
                    <hr class="mt-0">
                    <div
                      v-for="(dup) in stats[0].duplicate_items"
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
                          :value="toPercent( dup.count, topGainerOccurances)" />
                      </div>
                    </div>
                    <div
                      v-for="(dup) in stats[1].duplicate_items"
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
                          :value="toPercent( dup.count, topLoserOccurances)" />
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
                        <CCallout color="success">
                          <small class="text-muted">TBD</small><br>
                          <strong class="h4">0</strong>
                        </CCallout>
                      </CCol>
                    </CRow>
                    <hr class="mt-0">
                    <ul class="horizontal-bars type-2">
                      <div class="progress-group">
                        <div class="progress-group-header">
                          <CIcon
                            name="cil-user"
                            class="progress-group-icon" />
                          <span class="title">Male</span>
                          <span class="ml-auto font-weight-bold">43%</span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="43"
                            color="warning" />
                        </div>
                      </div>
                      <div class="progress-group mb-5">
                        <div class="progress-group-header">
                          <CIcon
                            name="cil-user-female"
                            class="progress-group-icon" />
                          <span class="title">Female</span>
                          <span class="ml-auto font-weight-bold">37%</span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="37"
                            color="warning" />
                        </div>
                      </div>
                      <div class="progress-group">
                        <div class="progress-group-header">
                          <CIcon
                            name="cil-globe-alt"
                            class="progress-group-icon" />
                          <span class="title">Organic Search</span>
                          <span class="ml-auto font-weight-bold">
                            191,235 <span class="text-muted small">(56%)</span>
                          </span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="56"
                            color="success" />
                        </div>
                      </div>
                      <div class="progress-group">
                        <div class="progress-group-header">
                          <CIcon
                            name="cib-facebook"
                            height="17"
                            class="progress-group-icon" />
                          <span class="title">Facebook</span>
                          <span class="ml-auto font-weight-bold">
                            51,223 <span class="text-muted small">(15%)</span>
                          </span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="15"
                            color="success" />
                        </div>
                      </div>
                      <div class="progress-group">
                        <div class="progress-group-header">
                          <CIcon
                            name="cib-twitter"
                            height="17"
                            class="progress-group-icon" />
                          <span class="title">Twitter</span>
                          <span class="ml-auto font-weight-bold">
                            37,564 <span class="text-muted small">(11%)</span>
                          </span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="11"
                            color="success" />
                        </div>
                      </div>
                      <div class="progress-group">
                        <div class="progress-group-header">
                          <CIcon
                            name="cib-linkedin"
                            height="17"
                            class="progress-group-icon" />
                          <span class="title">LinkedIn</span>
                          <span class="ml-auto font-weight-bold">
                            27,319 <span class="text-muted small">&nbsp;(8%)</span>
                          </span>
                        </div>
                        <div class="progress-group-bars">
                          <CProgress
                            class="progress-xs"
                            :value="8"
                            color="success" />
                        </div>
                      </div>
                      <div class="divider text-center">
                        <CButton
                          color="link"
                          size="sm"
                          class="text-muted">
                          <CIcon name="cil-options" />
                        </CButton>
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
  components: { 
  },
  mixins: [chartMixin],
  data() {
    return {
      loading: false,
      stats: [],
      totalItems: null,
      topGainerOccurances: 0,
      topLoserOccurances: 0,
    };
  },
  mounted() {
    this.loading = true;
    this.getStats().then(() => this.loading = false);
  },
  methods: {
    async getStats() {
      const response = await axios.get('http://localhost:5000/api/stats');
      this.stats = response.data;
      this.stats.forEach((stat) => {
        this.totalItems += stat.total_items;

        if (stat.api_endpoint == 'gainers') {
          stat.duplicate_items.forEach((dup) => {
            this.topGainerOccurances = (this.topGainerOccurances < dup.count) ? dup.count : this.topGainerOccurances;
          });
        }
        if (stat.api_endpoint == 'losers') {
          stat.duplicate_items.forEach((dup) => {
            this.topLoserOccurances = (this.topLoserOccurances < dup.count) ? dup.count : this.topLoserOccurances;
          });
        }
      });
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