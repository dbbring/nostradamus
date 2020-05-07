<template>
  <CSidebar 
    class="bg-dark"
    fixed 
    :minimize="minimize"
    :show="show"
    @update:show="(value) => $store.commit('set', ['sidebarShow', value])">
    <CSidebarBrand
      class="d-md-down-none"
      to="/"
      style="background-color: #010000;">
      <CImg
        class="c-sidebar-brand-full px-2" 
        src="img/logo.png"
        width="100%" />
    </CSidebarBrand>

    <CRenderFunction
      flat
      :content-to-render="$options.nav" />
    <CSidebarMinimizer
      class="d-md-down-none"
      @click.native="$store.commit('set', ['sidebarMinimize', !minimize])" />
  </CSidebar>
</template>

<script>
import nav from './_nav';

export default {
  name: 'TheSidebar',
  nav,
  computed: {
    show () {
      return this.$store.state.sidebarShow; 
    },
    minimize () {
      return this.$store.state.sidebarMinimize; 
    }
  }
};
</script>
