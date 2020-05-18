<template>
  <CHeader
    fixed
    with-subheader
    class="bg-dark color-white">
    <CRow style="width: 99%;">
      <CCol lg="1">
        <div
          class="wrap"
          @click="toggleMenu">
          <div class="icon-wrapper">
            <div class="icon mt-3">
              <div
                :class="`bar one ${menuOpen ? 'active' : 'notActive'}`" />
              <div
                :class="`bar two ${menuOpen ? 'active' : 'notActive'}`" />
              <div
                :class="`bar three ${menuOpen ? 'active' : 'notActive'}`" />
            </div>
          </div>
        </div>
        <CHeaderBrand
          class="mx-auto d-lg-none"
          to="/">
          <CIcon
            name="logo"
            height="48"
            alt="Logo" />
        </CHeaderBrand>
      </CCol>
      <CCol lg="3">
        <CHeaderNav class="d-md-down-none mr-auto">
          <CHeaderNavItem
            v-if="!$store.state.loading"
            class="ml-4 px-0 pt-1">
            <CSwitch
              v-for="(item, index) in $store.state.immutatableGainersData"
              :key="`${index}`"
              class="mx-1"
              color="success"
              :checked.sync="item.table_info.Display"
              :label-on="item.basic_info.ticker"
              :label-off="item.basic_info.ticker"
              @update:checked="updateMutatableData('mutatableGainersData', index, item)" />
            <CHeaderNavLink />
          </CHeaderNavItem>
        </CHeaderNav>
      </CCol>
      <CCol
        class="text-center"
        lg="3">
        <CHeaderNav class="d-md-down-none mr-auto">
          <CHeaderNavItem class="mt-2 w-100">
            <datepicker
              :value="$store.state.currentSelectedDate"
              calendar-class="bg-light"
              input-class="date-input"
              class="ml-3"
              format="MM dd yyyy"
              placeholder="Pick a Date"
              @input="updateDate" />
            <small
              v-if="$store.state.currentSelectedDate"
              class="text-center text-info py-2 mb-2">
              {{ $store.state.currentSelectedDate | $formatDateForDisplay }}
            </small>
          </CHeaderNavItem>
        </CHeaderNav>
      </CCol>
      <CCol
        class="ml-auto"
        lg="3">
        <CHeaderNav class="d-md-down-none mr-auto">
          <CHeaderNavItem
            v-if="!$store.state.loading"
            class="px-0 pt-1">
            <CSwitch
              v-for="(item, index) in $store.state.immutatableLosersData"
              :key="`${index}`"
              class="mx-1"
              color="danger"
              :checked.sync="item.table_info.Display"
              :label-on="item.basic_info.ticker"
              :label-off="item.basic_info.ticker"
              @update:checked="updateMutatableData('mutatableLosersData', index, item)" />
            <CHeaderNavLink />
          </CHeaderNavItem>
        </CHeaderNav>
      </CCol>
      <CCol
        class="ml-auto"
        lg="1">
        <CHeaderNav class="d-md-down-none mr-auto">
          <CHeaderNavItem class="ml-auto">
            <CHeaderNavLink>
              <CIcon name="cil-list" />
            </CHeaderNavLink>
          </CHeaderNavItem>
          <TheHeaderDropdownAccnt />
        </CHeadernav>
      </CCol>
    </CRow>
  </CHeader>
</template>

<script>
import axios from 'axios';
import TheHeaderDropdownAccnt from './TheHeaderDropdownAccnt';
import datepicker from 'vuejs-datepicker';

import { greenColors, redColors } from '../utils/colors';

export default {
  name: 'TheHeader',
  components: {
    TheHeaderDropdownAccnt,
    datepicker
  },
  data() {
    return {
      menuOpen: true
    };
  },
  methods: {
    async updateDate(date) {
      const cleanDate = this.$options.filters.$formatDateForSql(date);
      this.$store.commit('setSelectedDate', date);
      this.$store.commit('clearData');
      this.$store.commit('set', ['loading', true]);
      
      await Promise.all([
        this.updateGainers(cleanDate),
        this.updateLosers(cleanDate)
      ]);
    
      this.$store.commit('set', ['loading', false]);
    },
    async updateGainers(date) {
      let counter = 0;

      const transactionGainersItems = await axios.get('http://localhost:5000/api/gainers/' + date);

      await Promise.all(transactionGainersItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/gainers/ticker/' + trans_item.transaction_id);
        const tableData = {
          table_info: {
            'category': 'Gainers',
            'color': greenColors[counter],
            '_classes': `text-green-${counter}`,
          }
        };

        this.$store.commit('addToDataArray', ['mutatableGainersData', { ...tableData, ...details.data}]);
        this.$store.commit('addToDataArray', ['immutatableGainersData', { ...tableData, ...details.data}]);

        counter++;
      }));
    },
    async updateLosers(date) {
      let counter = 0;

      const transactionLoserItems = await axios.get('http://localhost:5000/api/losers/' + date);

      await Promise.all(transactionLoserItems.data.map(async (trans_item) => {
        const details = await axios.get('http://localhost:5000/api/losers/ticker/' + trans_item.transaction_id);

        const tableData = {
          table_info: {
            'category': 'Losers',
            'color': redColors[counter],
            '_classes': `text-red-${counter}`,
          }
        };

        this.$store.commit('addToDataArray', ['mutatableLosersData', { ...tableData, ...details.data}]);
        this.$store.commit('addToDataArray', ['immutatableLosersData', { ...tableData, ...details.data}]);
        counter++;
      }));
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen;

      if (this.menuOpen) {
        this.$store.commit('toggleSidebarMobile');
        return;
      }
      
      this.$store.commit('toggleSidebarDesktop');
      return;
    },
    updateMutatableData(arrayAsStr, index, item) {
      if (item.table_info.Display) {
        this.$store.commit('addToDataArray', [arrayAsStr, item]);
      } else {
        this.$store.commit('removeFromDataArray', [arrayAsStr, item]);
      }
      return;
    }
  }
};
</script>

<style scoped>
.wrap {
  display:table; 
  width: 100%; 
  height: 100%;
  }

.icon-wrapper {
	display: table-cell;
	text-align: center;
	vertical-align: middle;
}

.icon {
  position: relative;
  width: 40px; 
  height: 50px;
  display:inline-block;
  cursor:pointer;
}

.bar {
  width: 40px; 
  height: 5px;
  background-color: #fff;
  margin: 5px 0;
  position:absolute;
}

.icon .bar.one {top: 0; left: 0; }
.icon .bar.two {top: 10px; left: 0; }
.icon .bar.three {top: 20px; left: 0; }

.icon .bar.one.active {
	animation: one 1s forwards
}
.icon .bar.two.active {
	animation: two 1s forwards
}
.icon .bar.three.active {
	animation: three 1s forwards
}

.icon .bar.one.notActive {animation: one-reverse 1s forwards;}
.icon .bar.two.notActive {animation: two-reverse 1s forwards;}
.icon .bar.three.notActive {animation: three-reverse 1s forwards;}

@keyframes one {
	0% {top:0;}
	30% {top:-5px}
	60% {top:10px}
	80% {transform: rotate(0)}
	100% {top:10px; transform: rotate(45deg);}
}

@keyframes one-reverse {
	0% {top:10px; transform: rotate(45deg);}
	30% {transform: rotate(0)}
	60% {top:10px}
	80% {top:-5px}
	100% {top:0;}
}

@keyframes two {
	0% {opacity:1;}
	80% {opacity:1;}
	100% {opacity:0;}
}


@keyframes two-reverse {
	0% {opacity:0;}
	80% {opacity:1;}
	100% {opacity:1;}
}

@keyframes three {
	0% {top: 20px; }
	30% {top: 25px; }
  60% {top: 10px; }
	80% {transform: rotate(0)}
	100% {top: 10px; transform: rotate(-45deg);}
}

@keyframes three-reverse {
	0% {top: 10px; transform: rotate(-45deg);}
	30% {transform: rotate(0); }
  60% {top: 10px; }
	80% {top: 25px;}
	100% {top: 20px; }
}

</style>