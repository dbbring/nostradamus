import Vue from 'vue';
import moment from 'moment';

Vue.filter('$formatDateForSql', date => {
  return moment(date).format('YYYY-MM-DD');
});

Vue.filter('$formatDateForDisplay', date => {
  return moment(date).format('dddd, MMMM Do, YYYY');
});